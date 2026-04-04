"""Trackpad Witness™ — macOS trackpad pressure + click attestation (requires Accessibility)."""

from __future__ import annotations

import sys
import threading
import time

# ── Tuning (used by narc HUD + gate) ─────────────────────────────────────────
WITNESS_WINDOW_SEC = 3.5
# Integrated (pressure - PRESSURE_FLOOR) * dt must reach this (force-touch path).
WITNESS_PRESSURE_INTEGRAL_TARGET = 0.42
PRESSURE_FLOOR = 0.08
# Each left click while armed counts toward fallback attestation.
WITNESS_CLICKS_ALONE_TARGET = 3


class _NullWitness:
    """Non-macOS or monitor failed — witness not required."""

    available: bool = False
    reason: str = ""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def set_armed(self, armed: bool) -> None:
        pass

    def read_pressure(self) -> float:
        return 0.0

    def take_click_delta(self) -> int:
        return 0


class TrackpadWitness(_NullWitness):
    """Background NSEvent global monitor — pressure on drag/pressure events, clicks when armed."""

    def __init__(self) -> None:
        self.available = True
        self.reason = ""
        self._lock = threading.Lock()
        self._pressure = 0.0
        self._armed = False
        self._click_delta = 0
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._monitor = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="TrackpadWitness", daemon=True)
        self._thread.start()
        time.sleep(0.2)

    def stop(self) -> None:
        self._stop.set()
        if self._monitor is not None:
            try:
                from AppKit import NSEvent

                NSEvent.removeMonitor_(self._monitor)
            except Exception:
                pass
            self._monitor = None
        if self._thread is not None:
            self._thread.join(timeout=1.5)
            self._thread = None

    def set_armed(self, armed: bool) -> None:
        with self._lock:
            self._armed = armed
            if not armed:
                self._pressure = 0.0

    def read_pressure(self) -> float:
        with self._lock:
            return self._pressure

    def take_click_delta(self) -> int:
        with self._lock:
            n = self._click_delta
            self._click_delta = 0
            return n

    def _handler(self, event) -> None:
        try:
            from AppKit import (
                NSEventTypeLeftMouseDown,
                NSEventTypeLeftMouseDragged,
                NSEventTypeLeftMouseUp,
                NSEventTypePressure,
            )

            t = event.type()
            p = 0.0
            try:
                p = float(event.pressure())
            except (AttributeError, TypeError, ValueError):
                p = 0.0

            with self._lock:
                if t == NSEventTypeLeftMouseDown and self._armed:
                    self._click_delta += 1
                if t in (NSEventTypeLeftMouseDragged, NSEventTypePressure):
                    self._pressure = p
                elif t == NSEventTypeLeftMouseUp:
                    self._pressure = 0.0
        except Exception:
            pass

    def _run(self) -> None:
        try:
            from AppKit import (
                NSEvent,
                NSEventMaskLeftMouseDown,
                NSEventMaskLeftMouseDragged,
                NSEventMaskLeftMouseUp,
                NSEventMaskPressure,
            )

            try:
                NSApplication = __import__("AppKit", fromlist=["NSApplication"]).NSApplication
                NSApplication.sharedApplication()
            except Exception as ns_err:
                self.available = False
                self.reason = f"NSApplication initialization failed: {ns_err}"
                print(f"[narc] Trackpad Witness: {self.reason}")
                return

            mask = (
                NSEventMaskLeftMouseDown
                | NSEventMaskLeftMouseDragged
                | NSEventMaskLeftMouseUp
                | NSEventMaskPressure
            )
            self._monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
                mask,
                self._handler,
            )
            if self._monitor is None:
                self.available = False
                self.reason = (
                    "Global event monitor unavailable — grant Accessibility to this app "
                    "(System Settings → Privacy & Security → Accessibility), then restart."
                )
                print(f"[narc] Trackpad Witness: {self.reason}")
                return

            from PyObjCTools import AppHelper

            while not self._stop.is_set():
                AppHelper.runConsoleEventLoop(installInterrupt=True, maxTimeout=0.2)
        except Exception as e:
            self.available = False
            self.reason = str(e)
            print(f"[narc] Trackpad Witness disabled: {e}")


def create_witness() -> _NullWitness | TrackpadWitness:
    if sys.platform != "darwin":
        n = _NullWitness()
        n.reason = "not macOS"
        return n
    try:
        w = TrackpadWitness()
        w.start()
        if not w.available:
            return _NullWitness()
        return w
    except Exception as e:
        n = _NullWitness()
        n.reason = str(e)
        print(f"[narc] Trackpad Witness disabled: {e}")
        return n
