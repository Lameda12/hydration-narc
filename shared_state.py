"""Thread-safe shared state between narc background thread and menu bar main thread."""

from __future__ import annotations

import threading
import time
from datetime import datetime, timezone


class NarcState:
    """Atomic snapshot of narc daemon state, written by narc thread, read by menu bar."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.health_score = 100
        self.today_sip_count = 0
        self.today_compliance_count = 0
        self.last_sip_time: float | None = None
        self.monitoring_active = True
        self.shutdown_requested = False
        # Camera debug data
        self.smile_ratio = 0.0
        self.hand_near_mouth = False
        self.face_detected = False
        # Camera frame for preview window
        self.last_frame: bytes | None = None

    def update_score(self, score: int) -> None:
        """Called by narc thread when health score changes."""
        with self._lock:
            self.health_score = max(0, min(100, score))

    def update_sip(self, full_compliance: bool) -> None:
        """Called by narc thread when a sip is logged."""
        with self._lock:
            self.today_sip_count += 1
            if full_compliance:
                self.today_compliance_count += 1
            self.last_sip_time = time.time()

    def request_shutdown(self) -> None:
        """Called by menu bar to ask narc loop to exit cleanly."""
        with self._lock:
            self.shutdown_requested = True
            self.monitoring_active = False

    def clear_shutdown(self) -> None:
        """Called by menu bar before restarting the narc thread."""
        with self._lock:
            self.shutdown_requested = False
            self.monitoring_active = True

    def update_camera_debug(self, smile_ratio: float, hand_near_mouth: bool, face_detected: bool) -> None:
        """Called by narc thread to update camera detection state."""
        with self._lock:
            self.smile_ratio = smile_ratio
            self.hand_near_mouth = hand_near_mouth
            self.face_detected = face_detected

    def update_frame(self, frame_bytes: bytes | None) -> None:
        """Called by narc thread to push JPEG frame bytes for camera preview."""
        with self._lock:
            self.last_frame = frame_bytes

    def get_snapshot(self) -> dict:
        """Return an atomic copy of all state fields."""
        with self._lock:
            return {
                "health_score": self.health_score,
                "today_sip_count": self.today_sip_count,
                "today_compliance_count": self.today_compliance_count,
                "last_sip_time": self.last_sip_time,
                "monitoring_active": self.monitoring_active,
                "shutdown_requested": self.shutdown_requested,
                "smile_ratio": self.smile_ratio,
                "hand_near_mouth": self.hand_near_mouth,
                "face_detected": self.face_detected,
                "last_frame": self.last_frame,
            }

    def reset_today_counts(self) -> None:
        """Reset sip counts at day boundary (called by narc)."""
        with self._lock:
            self.today_sip_count = 0
            self.today_compliance_count = 0
            self.last_sip_time = None


class _DayBoundaryTracker:
    """Detect when calendar date rolls over (midnight UTC)."""

    def __init__(self) -> None:
        self._last_date: str | None = None

    def check(self, state: NarcState) -> bool:
        """Return True if date changed since last check; reset counts if so."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if self._last_date is None:
            self._last_date = today
            return False
        if today != self._last_date:
            self._last_date = today
            state.reset_today_counts()
            return True
        return False
