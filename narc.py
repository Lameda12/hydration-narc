"""Hydration Narc — MediaPipe Tasks (face + hands), decay, sip, threat automation."""

from __future__ import annotations

import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from actions import (
    hide_hostage_apps,
    nuclear_sleep,
    play_sound_if_exists,
    post_drought_slack,
    rickroll_full_volume,
    warn_observed_daniel,
)
from ledger import log_mortal_sin, log_sip

# ── Tuning ───────────────────────────────────────────────────────────────────
DECAY_INTERVAL_SEC = 60
DECAY_AMOUNT = 2
SIP_HOLD_TIME = 1.5
SIP_THRESHOLD = 0.12
SMILE_THRESHOLD = 0.28
NUCLEAR_DELAY_SEC = 60
WAKE_GAP_SEC = 15.0

THREAT_OBSERVED = 75
THREAT_HOSTAGE = 30

_FACE_TASK_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/latest/face_landmarker.task"
)
_HAND_TASK_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)


def _task_cache_dir() -> Path:
    p = Path.home() / "Library" / "Caches" / "HydrationNarc"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _ensure_task_model(filename: str, url: str) -> str:
    path = _task_cache_dir() / filename
    if path.is_file() and path.stat().st_size > 0:
        return str(path)
    tmp = path.with_suffix(path.suffix + ".part")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(path)
    return str(path)


def _landmark_xy(landmark, w: int, h: int) -> tuple[float, float]:
    return landmark.x * w, landmark.y * h


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _smile_spread_ratio(face_landmarks, w: int, h: int) -> float:
    """Mouth-corner distance / face width (Face Landmarker topology)."""
    if not face_landmarks:
        return 0.0
    lm = face_landmarks[0]
    left_corner = _landmark_xy(lm[61], w, h)
    right_corner = _landmark_xy(lm[291], w, h)
    left_cheek = _landmark_xy(lm[234], w, h)
    right_cheek = _landmark_xy(lm[454], w, h)
    face_width = _distance(left_cheek, right_cheek)
    if face_width == 0:
        return 0.0
    return _distance(left_corner, right_corner) / face_width


def _is_hand_near_mouth(
    hand_landmarks_list,
    face_landmarks,
    w: int,
    h: int,
) -> bool:
    if not hand_landmarks_list or not face_landmarks:
        return False
    face_lm = face_landmarks[0]
    mouth = (
        (face_lm[13].x + face_lm[14].x) / 2 * w,
        (face_lm[13].y + face_lm[14].y) / 2 * h,
    )
    for hand_lm in hand_landmarks_list:
        index_tip = _landmark_xy(hand_lm[8], w, h)
        dist = _distance(index_tip, mouth) / ((w + h) / 2)
        if dist < SIP_THRESHOLD:
            return True
    return False


class SipDetector:
    def __init__(self) -> None:
        self._sip_start: float | None = None

    def update(self, near_mouth: bool) -> bool:
        now = time.time()
        if near_mouth:
            if self._sip_start is None:
                self._sip_start = now
            elif now - self._sip_start >= SIP_HOLD_TIME:
                self._sip_start = None
                return True
        else:
            self._sip_start = None
        return False


class HealthScore:
    def __init__(self) -> None:
        self.score = 100
        self._last_decay = time.time()
        self._warned_observed = False
        self._hostage_armed = False
        self._slack_at_zero_done = False
        self._zero_since: float | None = None
        self._nuked = False
        self._pending_wake_rickroll = False
        self._rickroll_played = False

    def _reset_threat_latches(self) -> None:
        self._warned_observed = False
        self._hostage_armed = False
        self._slack_at_zero_done = False
        self._zero_since = None
        self._nuked = False
        self._pending_wake_rickroll = False
        self._rickroll_played = False

    def apply_full_compliance(self, smile_ratio: float) -> None:
        log_sip(smile_ratio, True)
        self.score = 100
        self._last_decay = time.time()
        self._reset_threat_latches()
        print("[narc] Full compliance — smile OK — health reset to 100.")

    def tick(self, loop_now: float, loop_gap_sec: float) -> int:
        if (
            self._pending_wake_rickroll
            and not self._rickroll_played
            and loop_gap_sec >= WAKE_GAP_SEC
        ):
            self._rickroll_played = True
            self._pending_wake_rickroll = False
            rickroll_full_volume()

        if loop_now - self._last_decay >= DECAY_INTERVAL_SEC:
            self.score = max(0, self.score - DECAY_AMOUNT)
            self._last_decay = loop_now
            self._on_decay_level()

        if self.score > THREAT_OBSERVED:
            self._warned_observed = False
        if self.score > THREAT_HOSTAGE:
            self._hostage_armed = False
        if self.score > 0:
            self._slack_at_zero_done = False
            self._zero_since = None
            self._nuked = False

        if self.score == 0:
            if self._zero_since is None:
                self._zero_since = loop_now
            if not self._slack_at_zero_done:
                post_drought_slack()
                play_sound_if_exists("shame_zero.mp3")
                self._slack_at_zero_done = True
            if (
                not self._nuked
                and self._zero_since is not None
                and (loop_now - self._zero_since) >= NUCLEAR_DELAY_SEC
            ):
                self._nuked = True
                log_mortal_sin()
                warn_observed_daniel("You chose this. Goodnight.")
                self._pending_wake_rickroll = True
                self._rickroll_played = False
                nuclear_sleep()

        return self.score

    def _on_decay_level(self) -> None:
        if self.score <= THREAT_OBSERVED and not self._warned_observed:
            warn_observed_daniel("I see you getting thirsty. Drink water.")
            play_sound_if_exists("observed.mp3")
            self._warned_observed = True
        if self.score <= THREAT_HOSTAGE and not self._hostage_armed:
            hide_hostage_apps()
            play_sound_if_exists("hostage.mp3")
            warn_observed_daniel("Productivity apps are grounded until you hydrate.")
            self._hostage_armed = True


def run() -> None:
    face_path = _ensure_task_model("face_landmarker.task", _FACE_TASK_URL)
    hand_path = _ensure_task_model("hand_landmarker.task", _HAND_TASK_URL)

    base_face = python.BaseOptions(model_asset_path=face_path)
    base_hand = python.BaseOptions(model_asset_path=hand_path)

    face_options = vision.FaceLandmarkerOptions(
        base_options=base_face,
        running_mode=vision.RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.6,
        min_face_presence_confidence=0.6,
        min_tracking_confidence=0.6,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
    )
    hand_options = vision.HandLandmarkerOptions(
        base_options=base_hand,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    cap = cv2.VideoCapture(0)
    health = HealthScore()
    sip = SipDetector()
    last_loop_t = time.time()
    frame_ms = 0

    with vision.FaceLandmarker.create_from_options(face_options) as face_lm:
        with vision.HandLandmarker.create_from_options(hand_options) as hand_lm:
            while cap.isOpened():
                now = time.time()
                gap = now - last_loop_t
                last_loop_t = now

                ok, frame = cap.read()
                if not ok:
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame.shape[:2]

                frame_ms += 33
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

                face_res = face_lm.detect_for_video(mp_image, frame_ms)
                hand_res = hand_lm.detect_for_video(mp_image, frame_ms)

                faces = face_res.face_landmarks
                hands = hand_res.hand_landmarks

                near = _is_hand_near_mouth(hands, faces, w, h)
                smile_ratio = _smile_spread_ratio(faces, w, h)

                if sip.update(near):
                    if smile_ratio >= SMILE_THRESHOLD:
                        play_sound_if_exists("sip_success.mp3")
                        health.apply_full_compliance(smile_ratio)
                    else:
                        warn_observed_daniel(
                            "That is not full compliance. Smile while you drink — "
                            "spread at least point two eight."
                        )
                        play_sound_if_exists("sip_fail.mp3")
                        log_sip(smile_ratio, False)

                score = health.tick(now, gap)

                color = (0, 200, 0) if score > THREAT_OBSERVED else (0, 165, 255)
                if score <= THREAT_HOSTAGE:
                    color = (0, 140, 255)
                if score == 0:
                    color = (0, 0, 255)

                cv2.putText(
                    frame,
                    f"Health: {score}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    color,
                    2,
                )
                cv2.putText(
                    frame,
                    f"Smile S: {smile_ratio:.2f} (need >= {SMILE_THRESHOLD})",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (200, 200, 200),
                    1,
                )
                if near:
                    msg = (
                        "SIP — smile for compliance"
                        if smile_ratio < SMILE_THRESHOLD
                        else "SIP + SMILE OK"
                    )
                    cv2.putText(
                        frame,
                        msg,
                        (20, 115),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 255, 255),
                        2,
                    )

                cv2.imshow("Hydration Narc", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
