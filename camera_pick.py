"""Pick the MacBook built-in camera for OpenCV (skip iPhone / Continuity when possible)."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import cv2


@dataclass(frozen=True)
class _AVDevice:
    av_index: int
    name: str
    device_type: str

    @property
    def name_lower(self) -> str:
        return self.name.lower()

    @property
    def type_lower(self) -> str:
        return self.device_type.lower()

    def is_iphone_like(self) -> bool:
        n = self.name_lower
        return any(x in n for x in ("iphone", "ipad", "ipod", "continuity"))

    def is_builtin_wide(self) -> bool:
        return "builtin" in self.type_lower and "wide" in self.type_lower.replace("_", "")

    def is_facetime_like(self) -> bool:
        n = self.name_lower
        return "facetime" in n or "hd camera" in n or "macbook" in n or "imac" in n


def _avfoundation_devices() -> list[_AVDevice] | None:
    if sys.platform != "darwin":
        return None
    try:
        import AVFoundation as AV
        from AVFoundation import AVCaptureDeviceDiscoverySession, AVMediaTypeVideo
    except ImportError:
        return None

    type_names = (
        "AVCaptureDeviceTypeBuiltInWideAngleCamera",
        "AVCaptureDeviceTypeExternal",
        "AVCaptureDeviceTypeContinuityCamera",
        "AVCaptureDeviceTypeDeskViewCamera",
    )
    types: list[object] = []
    for name in type_names:
        t = getattr(AV, name, None)
        if t is not None and t not in types:
            types.append(t)
    if not types:
        return None

    pos = getattr(AV, "AVCaptureDevicePositionUnspecified", 0)
    sess = AVCaptureDeviceDiscoverySession.discoverySessionWithDeviceTypes_mediaType_position_(
        types,
        AVMediaTypeVideo,
        pos,
    )
    devs = sess.devices()
    if not devs or devs.count() == 0:
        return None

    out: list[_AVDevice] = []
    for i in range(devs.count()):
        d = devs.objectAtIndex_(i)
        name = d.localizedName() or ""
        dt = str(d.deviceType() or "")
        out.append(_AVDevice(i, name, dt))
    return out


def preferred_opencv_indices() -> list[int]:
    """Ordered OpenCV indices to try (AVFoundation backend on macOS)."""
    raw = os.environ.get("HYDRATION_NARC_CAMERA_INDEX")
    if raw is not None and raw.strip() != "":
        return [int(raw.strip())]

    if sys.platform != "darwin":
        return [0]

    av = _avfoundation_devices()
    if not av:
        return [0]

    n = len(av)
    builtin_idx: int | None = None
    iphone_idx: int | None = None

    for d in av:
        if d.is_iphone_like() and iphone_idx is None:
            iphone_idx = d.av_index
        if d.is_builtin_wide() or (d.is_facetime_like() and not d.is_iphone_like()):
            if builtin_idx is None:
                builtin_idx = d.av_index

    if builtin_idx is None:
        builtin_idx = 0

    # OpenCV's AVFoundation backend often enumerates Continuity Camera *before* the
    # built-in FaceTime camera, even when AVFoundation's discovery order is the opposite.
    if (
        iphone_idx is not None
        and builtin_idx < iphone_idx
    ):
        head = [iphone_idx, builtin_idx]
        tail = [d.av_index for d in av if d.av_index not in (iphone_idx, builtin_idx)]
        ordered = head + tail
    else:
        ordered = [builtin_idx] + [d.av_index for d in av if d.av_index != builtin_idx]

    seen: set[int] = set()
    uniq: list[int] = []
    for i in ordered:
        if i not in seen and i >= 0:
            seen.add(i)
            uniq.append(i)
    for i in range(min(n + 2, 8)):
        if i not in seen:
            uniq.append(i)
    return uniq


def open_preferred_capture() -> cv2.VideoCapture:
    """Open the first working capture device, preferring built-in FaceTime on macOS.

    Falls back to indices 0, 1, 2 if preferred candidates fail.
    """
    backend = cv2.CAP_AVFOUNDATION if sys.platform == "darwin" else 0
    last: cv2.VideoCapture | None = None
    indices = preferred_opencv_indices()

    for idx in indices:
        cap = cv2.VideoCapture(idx, backend) if backend else cv2.VideoCapture(idx)
        last = cap
        if not cap.isOpened():
            cap.release()
            continue
        ok, _ = cap.read()
        if ok:
            print(f"[narc] Camera OpenCV index {idx} (backend={'AVFoundation' if backend else 'default'})")
            return cap
        cap.release()

    # Fallback cycle through indices 0, 1, 2 if preferred indices exhausted.
    print("[narc] Preferred indices failed, cycling through fallback indices 0, 1, 2...")
    for fallback_idx in [0, 1, 2]:
        cap = cv2.VideoCapture(fallback_idx, backend) if backend else cv2.VideoCapture(fallback_idx)
        if not cap.isOpened():
            cap.release()
            continue
        ok, _ = cap.read()
        if ok:
            print(f"[narc] Fallback: Camera OpenCV index {fallback_idx} opened successfully")
            return cap
        cap.release()

    # Final fallback: return index 0 regardless of state.
    print("[narc] All fallbacks exhausted, returning index 0")
    return cv2.VideoCapture(0, backend) if backend else cv2.VideoCapture(0)
