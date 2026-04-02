"""The Hydration Narc — webcam-based hydration enforcer."""

import os
import random
import time
import cv2
import mediapipe as mp
from actions import dim_screen, restore_screen, mouse_jitter, shame_user, nuclear_penalty, social_shame, take_hostage, lock_keyboard, unlock_keyboard
from ledger import log_sip, log_mortal_sin

# ── Constants ────────────────────────────────────────────────────────────────
DECAY_INTERVAL   = 60      # seconds between score drops
DECAY_AMOUNT     = 2       # points lost per interval
SIP_HOLD_TIME    = 1.5     # seconds hand must stay near mouth to count as sip
SIP_THRESHOLD    = 0.12    # normalized distance (hand tip → mouth) for a sip
PUNISH_THRESHOLD = 60      # score at which punishments begin
NUCLEAR_DELAY    = 60      # seconds at score=0 before sleep
RICKROLL_WINDOW  = 30      # seconds after wake with no sip → rickroll
SMILE_THRESHOLD  = 0.28    # mouth-corner spread / face-width ratio to count as smile
LOCKDOWN_THRESHOLD = 15    # score at which keyboard is seized

INSULTS = [
    "Absolutely pathetic. A cactus has better self-discipline than you.",
    "You call that hydration? My grandmother drinks more, and she's been dead for years.",
    "Truly embarrassing. I've seen houseplants with more survival instinct.",
    "Your willpower is inversely proportional to your dehydration. Impressive, in the worst way.",
    "A goldfish has a shorter memory AND better hydration habits than you.",
]


# ── MediaPipe setup ───────────────────────────────────────────────────────────
_mp_hands   = mp.solutions.hands
_mp_face    = mp.solutions.face_mesh
_mp_drawing = mp.solutions.drawing_utils


def _landmark_xy(landmark, w: int, h: int) -> tuple[float, float]:
    return landmark.x * w, landmark.y * h


def _distance(a: tuple, b: tuple) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _smile_intensity(face_results, w: int, h: int) -> float:
    """Return mouth-corner / face-width ratio (0.0 if no face detected).

    FaceMesh landmarks:
      61  = left mouth corner
      291 = right mouth corner
      234 = left cheek (face width reference)
      454 = right cheek
    """
    if not face_results.multi_face_landmarks:
        return 0.0
    lm = face_results.multi_face_landmarks[0].landmark
    left_corner  = _landmark_xy(lm[61],  w, h)
    right_corner = _landmark_xy(lm[291], w, h)
    left_cheek   = _landmark_xy(lm[234], w, h)
    right_cheek  = _landmark_xy(lm[454], w, h)
    face_width   = _distance(left_cheek, right_cheek)
    if face_width == 0:
        return 0.0
    return _distance(left_corner, right_corner) / face_width


def _is_smiling(face_results, w: int, h: int) -> bool:
    return _smile_intensity(face_results, w, h) >= SMILE_THRESHOLD


# ── Health score ──────────────────────────────────────────────────────────────
class HealthScore:
    def __init__(self):
        self.score                      = 100
        self._last_decay                = time.time()
        self._warned_75                 = False
        self._warned_40                 = False
        self._zero_since: float | None  = None
        self._social_shamed             = False
        self._nuked                     = False
        self._woke_at: float | None     = None   # time machine woke after nuke
        self._rickrolled                = False

    def tick(self) -> int:
        now = time.time()
        if now - self._last_decay >= DECAY_INTERVAL:
            self.score       = max(0, self.score - DECAY_AMOUNT)
            self._last_decay = now
            self._check_warnings()

        # Keyboard lockdown at critical health
        if self.score <= LOCKDOWN_THRESHOLD:
            lock_keyboard()

        # Track time spent at zero → social shame → nuclear
        if self.score == 0:
            if self._zero_since is None:
                self._zero_since = now
                if not self._social_shamed:
                    shame_user(
                        "Im telling your coworkers youre dying of thirst. Goodnight."
                    )
                    social_shame()
                    self._social_shamed = True
            elif not self._nuked and (now - self._zero_since) >= NUCLEAR_DELAY:
                self._nuked   = True
                self._woke_at = None
                log_mortal_sin()
                nuclear_penalty()
                # After sleep returns (machine woke), start the rickroll clock
                self._woke_at = time.time()
        else:
            self._zero_since    = None
            self._social_shamed = False
            self._nuked         = False

        # Post-nuclear rickroll window
        if self._woke_at and not self._rickrolled:
            if now - self._woke_at >= RICKROLL_WINDOW:
                self._rickrolled = True
                os.system("open 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")

        return self.score

    def _check_warnings(self):
        if not self._warned_75 and self.score <= 75:
            shame_user("I see you getting thirsty. Dont make me dim the lights.")
            self._warned_75 = True
        if not self._warned_40 and self.score <= 40:
            shame_user("This is your final warning. Drink now or lose your mouse.")
            self._warned_40 = True

    def reset(self, smile_intensity: float) -> None:
        full   = smile_intensity >= SMILE_THRESHOLD
        target = 100 if full else max(self.score, 50)
        if not full and self.score < 50:
            shame_user("You look miserable. Smile while you drink or it doesnt count.")
        log_sip(smile_intensity, full)
        unlock_keyboard()
        self.score           = target
        self._warned_75      = False
        self._warned_40      = False
        self._zero_since     = None
        self._social_shamed  = False
        self._nuked          = False
        self._woke_at        = None
        self._rickrolled     = False
        print(f"[narc] Sip registered — health {'reset to 100' if full else f'recovered to {target} (grumpy penalty)'}.")

    def apply_punishment(self):
        if self.score <= PUNISH_THRESHOLD:
            print(f"[narc] Score {self.score} — punishing!")
            shame_user(random.choice(INSULTS))
            take_hostage(self.score)
            dim_screen(brightness=0.2)
            mouse_jitter()
            time.sleep(0.5)
            restore_screen()


# ── Sip detection ─────────────────────────────────────────────────────────────
class SipDetector:
    def __init__(self):
        self._sip_start: float | None = None

    def update(self, near_mouth: bool) -> bool:
        """Return True when a confirmed sip completes."""
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


# ── Frame processing ──────────────────────────────────────────────────────────
def _is_hand_near_mouth(
    hand_results,
    face_results,
    w: int,
    h: int,
) -> bool:
    if not hand_results.multi_hand_landmarks or not face_results.multi_face_landmarks:
        return False

    # Mouth center: landmarks 13 (upper lip) and 14 (lower lip)
    face_lm = face_results.multi_face_landmarks[0].landmark
    mouth = (
        (face_lm[13].x + face_lm[14].x) / 2 * w,
        (face_lm[13].y + face_lm[14].y) / 2 * h,
    )

    for hand_lm in hand_results.multi_hand_landmarks:
        index_tip = _landmark_xy(hand_lm.landmark[8], w, h)
        dist = _distance(index_tip, mouth) / ((w + h) / 2)  # normalize
        if dist < SIP_THRESHOLD:
            return True
    return False


# ── Main loop ─────────────────────────────────────────────────────────────────
def run():
    cap    = cv2.VideoCapture(0)
    health = HealthScore()
    sip    = SipDetector()

    with (
        _mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.6) as hands,
        _mp_face.FaceMesh(max_num_faces=1, min_detection_confidence=0.6) as face_mesh,
    ):
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w  = frame.shape[:2]

            hand_res = hands.process(rgb)
            face_res = face_mesh.process(rgb)

            near      = _is_hand_near_mouth(hand_res, face_res, w, h)
            intensity = _smile_intensity(face_res, w, h)
            smiling   = intensity >= SMILE_THRESHOLD

            if sip.update(near):
                os.system("afplay /System/Library/Sounds/Glass.aiff &")
                health.reset(smile_intensity=intensity)

            score = health.tick()
            health.apply_punishment()

            # HUD
            color = (0, 200, 0) if score > 60 else (0, 100, 255)
            cv2.putText(frame, f"Health: {score}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
            cv2.putText(frame, f"Smile: {intensity:.2f}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            if score <= LOCKDOWN_THRESHOLD:
                cv2.putText(frame, "KEYBOARD LOCKED", (20, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if near:
                label = "SIP + SMILE :)" if smiling else "SIP (no smile — 50% recovery)"
                cv2.putText(frame, label, (20, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.imshow("Hydration Narc", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
