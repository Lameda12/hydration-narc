"""macOS menu bar UI for Hydration Narc — status, stats, settings, and control."""

from __future__ import annotations

import time
import threading
from typing import Any

from AppKit import (
    NSApplication,
    NSStatusBar,
    NSMenu,
    NSMenuItem,
    NSVariableStatusItemLength,
    NSObject,
    NSAlert,
    NSTextField,
    NSAlertFirstButtonReturn,
    NSWindow,
    NSImageView,
    NSImage,
    NSTitledWindowMask,
    NSClosableWindowMask,
    NSResizableWindowMask,
    NSBackingStoreBuffered,
    NSFloatingWindowLevel,
)
from Foundation import NSTimer, NSData
from PyObjCTools import AppHelper
import objc
from io import BytesIO

from shared_state import NarcState
from settings_store import SettingsStore


class NarcMenuBarApp(NSObject):
    """Menu bar app delegate — owns the main thread, drives UI updates."""

    def init(self) -> NarcMenuBarApp:
        self = objc.super(NarcMenuBarApp, self).init()
        self._state = None
        self._settings = None
        self._narc_thread = None
        self._status_item = None
        self._menu = None
        self._items = {}
        self._timer = None
        self._camera_window = None
        self._camera_image_view = None
        self._camera_timer = None
        return self

    def applicationDidFinishLaunching_(self, notification: Any) -> None:
        """Called when NSApp starts the event loop."""
        self._build_menu()
        self._setup_status_item()
        self._setup_timer()

    def _setup_status_item(self) -> None:
        """Create the status item (menu bar icon + dropdown)."""
        status_bar = NSStatusBar.systemStatusBar()
        self._status_item = status_bar.statusItemWithLength_(NSVariableStatusItemLength)
        self._status_item.setTitle_("💧100")
        self._status_item.setMenu_(self._menu or NSMenu.new())

    def _build_menu(self) -> None:
        """Construct the full NSMenu tree."""
        self._menu = NSMenu.new()

        # ─── 📊 STATS SECTION
        header = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "📊 STATUS", None, ""
        )
        header.setEnabled_(False)
        self._menu.addItem_(header)

        item_score = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "💧 Health: 100", None, ""
        )
        item_score.setEnabled_(False)
        self._menu.addItem_(item_score)
        self._items["score"] = item_score

        item_water = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "💦 Water: 0/8 sips", None, ""
        )
        item_water.setEnabled_(False)
        self._menu.addItem_(item_water)
        self._items["water"] = item_water

        item_sips = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "🥤 Sips today: 0 (0 compliant)", None, ""
        )
        item_sips.setEnabled_(False)
        self._menu.addItem_(item_sips)
        self._items["sips"] = item_sips

        item_last_sip = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "⏰ Last sip: never", None, ""
        )
        item_last_sip.setEnabled_(False)
        self._menu.addItem_(item_last_sip)
        self._items["last_sip"] = item_last_sip

        # ─── Separator
        self._menu.addItem_(NSMenuItem.separatorItem())

        # ─── 📷 CAMERA SECTION
        camera_header = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "📷 CAMERA", None, ""
        )
        camera_header.setEnabled_(False)
        self._menu.addItem_(camera_header)

        camera_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "👁️ Open Live Preview", "showCameraPreview:", ""
        )
        self._menu.addItem_(camera_item)

        item_face = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  👤 Face: detecting", None, ""
        )
        item_face.setEnabled_(False)
        self._menu.addItem_(item_face)
        self._items["face_detected"] = item_face

        item_smile = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  😊 Smile: 0.00 / 0.28", None, ""
        )
        item_smile.setEnabled_(False)
        self._menu.addItem_(item_smile)
        self._items["smile_ratio"] = item_smile

        item_hand = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  👆 Hand: away", None, ""
        )
        item_hand.setEnabled_(False)
        self._menu.addItem_(item_hand)
        self._items["hand_near"] = item_hand

        # ─── Separator
        self._menu.addItem_(NSMenuItem.separatorItem())

        # ─── Settings submenu
        settings_menu = NSMenu.new()

        decay_interval_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Decay interval: {int(self._settings.get('DECAY_INTERVAL_SEC'))}s",
            "changeDecayInterval:",
            "",
        )
        settings_menu.addItem_(decay_interval_item)
        self._items["decay_interval"] = decay_interval_item

        decay_amount_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Decay amount: {int(self._settings.get('DECAY_AMOUNT'))}pts",
            "changeDecayAmount:",
            "",
        )
        settings_menu.addItem_(decay_amount_item)
        self._items["decay_amount"] = decay_amount_item

        sip_threshold_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Sip threshold: {self._settings.get('SIP_THRESHOLD'):.2f}",
            "changeSipThreshold:",
            "",
        )
        settings_menu.addItem_(sip_threshold_item)
        self._items["sip_threshold"] = sip_threshold_item

        smile_threshold_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Smile threshold: {self._settings.get('SMILE_THRESHOLD'):.2f}",
            "changeSmileThreshold:",
            "",
        )
        settings_menu.addItem_(smile_threshold_item)
        self._items["smile_threshold"] = smile_threshold_item

        nuclear_delay_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Nuclear delay: {int(self._settings.get('NUCLEAR_DELAY_SEC'))}s",
            "changeNuclearDelay:",
            "",
        )
        settings_menu.addItem_(nuclear_delay_item)
        self._items["nuclear_delay"] = nuclear_delay_item

        threat_observed_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Warn at: {int(self._settings.get('THREAT_OBSERVED'))}",
            "changeThreatObserved:",
            "",
        )
        settings_menu.addItem_(threat_observed_item)
        self._items["threat_observed"] = threat_observed_item

        threat_hostage_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"Hostage at: {int(self._settings.get('THREAT_HOSTAGE'))}",
            "changeThreatHostage:",
            "",
        )
        settings_menu.addItem_(threat_hostage_item)
        self._items["threat_hostage"] = threat_hostage_item

        settings_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "⚙️ Settings", None, ""
        )
        settings_item.setSubmenu_(settings_menu)
        self._menu.addItem_(settings_item)

        # ─── Separator
        self._menu.addItem_(NSMenuItem.separatorItem())

        # ─── Control
        toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "▶️ Pause monitoring", "toggleMonitoring:", ""
        )
        self._menu.addItem_(toggle_item)
        self._items["toggle"] = toggle_item

        # ─── Separator
        self._menu.addItem_(NSMenuItem.separatorItem())

        # ─── Help
        help_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "❓ How to Use", None, ""
        )
        help_item.setEnabled_(False)
        self._menu.addItem_(help_item)

        help_text = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  Take a sip → hand near mouth + smile", None, ""
        )
        help_text.setEnabled_(False)
        self._menu.addItem_(help_text)

        help_text2 = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  No smile → sip fails, health decays", None, ""
        )
        help_text2.setEnabled_(False)
        self._menu.addItem_(help_text2)

        help_text3 = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "  Open camera to debug detection", None, ""
        )
        help_text3.setEnabled_(False)
        self._menu.addItem_(help_text3)

        # ─── Separator
        self._menu.addItem_(NSMenuItem.separatorItem())

        # ─── Quit
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "❌ Quit Hydration Narc", "quitApp:", ""
        )
        self._menu.addItem_(quit_item)

        self._status_item.setMenu_(self._menu)

    def _setup_timer(self) -> None:
        """Start a 2-second NSTimer to refresh the menu."""
        self._timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            2.0, self, "timerFired:", None, True
        )

    def timerFired_(self, timer: Any) -> None:
        """Called every 2 seconds on the main thread — update UI."""
        if not self._state or not self._settings:
            return

        snapshot = self._state.get_snapshot()
        score = snapshot["health_score"]
        monitoring = snapshot["monitoring_active"]

        # Update status bar title
        if not monitoring:
            self._status_item.setTitle_("⏸")
        elif score == 0:
            self._status_item.setTitle_("💀0")
        else:
            self._status_item.setTitle_(f"💧{score}")

        # Update stats items
        health_emoji = "🔴" if score <= 30 else "🟡" if score <= 60 else "🟢"
        self._items["score"].setTitle_(f"💧 Health: {score} {health_emoji}")

        sip_count = snapshot["today_sip_count"]
        compliance_count = snapshot["today_compliance_count"]
        compliance_emoji = "✅" if compliance_count == sip_count else "⚠️"
        self._items["sips"].setTitle_(f"🥤 Sips today: {sip_count} ({compliance_count} ✓) {compliance_emoji}")

        last_sip_time = snapshot["last_sip_time"]
        time_since = self._format_time_since(last_sip_time)
        self._items["last_sip"].setTitle_(f"⏰ Last sip: {time_since}")

        # Update water progress with visual bar
        daily_goal = int(self._settings.get("DAILY_WATER_GOAL_SIPS"))
        water_percent = int((sip_count / daily_goal * 100)) if daily_goal > 0 else 0
        filled = int(water_percent / 10)
        bar = "█" * filled + "░" * (10 - filled)
        self._items["water"].setTitle_(f"💦 Water: {sip_count}/{daily_goal} {bar} {water_percent}%")

        # Update toggle button label
        pause_label = "⏸️ Pause monitoring" if monitoring else "▶️ Resume monitoring"
        self._items["toggle"].setTitle_(pause_label)

        # Update camera debug items
        face_detected = snapshot["face_detected"]
        smile_ratio = snapshot["smile_ratio"]
        hand_near = snapshot["hand_near_mouth"]
        smile_threshold = self._settings.get("SMILE_THRESHOLD")

        face_emoji = "👤" if face_detected else "🚫"
        face_status = "detecting ✓" if face_detected else "no face ✗"
        self._items["face_detected"].setTitle_(f"  {face_emoji} Face: {face_status}")

        smile_emoji = "😊" if smile_ratio >= smile_threshold else "😐"
        smile_status = "✓" if smile_ratio >= smile_threshold else "✗"
        self._items["smile_ratio"].setTitle_(f"  {smile_emoji} Smile: {smile_ratio:.2f}/{smile_threshold:.2f} {smile_status}")

        hand_emoji = "👆" if hand_near else "👇"
        hand_status = "near ✓" if hand_near else "away ✗"
        self._items["hand_near"].setTitle_(f"  {hand_emoji} Hand: {hand_status}")

    def _format_time_since(self, last_sip_time: float | None) -> str:
        """Format time since last sip as human-readable string."""
        if last_sip_time is None:
            return "never"
        elapsed = time.time() - last_sip_time
        if elapsed < 60:
            return f"{int(elapsed)}s ago"
        elif elapsed < 3600:
            return f"{int(elapsed / 60)}m {int(elapsed % 60)}s ago"
        else:
            hours = int(elapsed / 3600)
            minutes = int((elapsed % 3600) / 60)
            return f"{hours}h {minutes}m ago"

    # ─── Settings action handlers (each opens an NSAlert input dialog)

    def changeDecayInterval_(self, sender: Any) -> None:
        """Change DECAY_INTERVAL_SEC."""
        current = int(self._settings.get("DECAY_INTERVAL_SEC"))
        new_val = self._prompt_for_float("Decay interval (seconds)", current)
        if new_val is not None and new_val > 0:
            self._settings.set("DECAY_INTERVAL_SEC", new_val)
            sender.setTitle_(f"Decay interval: {int(new_val)}s")

    def changeDecayAmount_(self, sender: Any) -> None:
        """Change DECAY_AMOUNT."""
        current = int(self._settings.get("DECAY_AMOUNT"))
        new_val = self._prompt_for_float("Decay amount (points)", current)
        if new_val is not None and new_val > 0:
            self._settings.set("DECAY_AMOUNT", new_val)
            sender.setTitle_(f"Decay amount: {int(new_val)}pts")

    def changeSipThreshold_(self, sender: Any) -> None:
        """Change SIP_THRESHOLD."""
        current = float(self._settings.get("SIP_THRESHOLD"))
        new_val = self._prompt_for_float("Sip threshold", current)
        if new_val is not None and 0 < new_val < 1:
            self._settings.set("SIP_THRESHOLD", new_val)
            sender.setTitle_(f"Sip threshold: {new_val:.2f}")

    def changeSmileThreshold_(self, sender: Any) -> None:
        """Change SMILE_THRESHOLD."""
        current = float(self._settings.get("SMILE_THRESHOLD"))
        new_val = self._prompt_for_float("Smile threshold", current)
        if new_val is not None and 0 < new_val < 1:
            self._settings.set("SMILE_THRESHOLD", new_val)
            sender.setTitle_(f"Smile threshold: {new_val:.2f}")

    def changeNuclearDelay_(self, sender: Any) -> None:
        """Change NUCLEAR_DELAY_SEC."""
        current = int(self._settings.get("NUCLEAR_DELAY_SEC"))
        new_val = self._prompt_for_float("Nuclear delay (seconds)", current)
        if new_val is not None and new_val > 0:
            self._settings.set("NUCLEAR_DELAY_SEC", new_val)
            sender.setTitle_(f"Nuclear delay: {int(new_val)}s")

    def changeThreatObserved_(self, sender: Any) -> None:
        """Change THREAT_OBSERVED."""
        current = int(self._settings.get("THREAT_OBSERVED"))
        new_val = self._prompt_for_float("Warn at (health score)", current)
        if new_val is not None and 0 <= new_val <= 100:
            self._settings.set("THREAT_OBSERVED", new_val)
            sender.setTitle_(f"Warn at: {int(new_val)}")

    def changeThreatHostage_(self, sender: Any) -> None:
        """Change THREAT_HOSTAGE."""
        current = int(self._settings.get("THREAT_HOSTAGE"))
        new_val = self._prompt_for_float("Hostage at (health score)", current)
        if new_val is not None and 0 <= new_val <= 100:
            self._settings.set("THREAT_HOSTAGE", new_val)
            sender.setTitle_(f"Hostage at: {int(new_val)}")

    def _prompt_for_float(self, label: str, current_value: float | int) -> float | None:
        """Open an NSAlert with a text input field; return parsed float or None."""
        alert = NSAlert.alloc().init()
        alert.setMessageText_(label)
        alert.setInformativeText_(f"Current value: {current_value}")
        alert.addButtonWithTitle_("OK")
        alert.addButtonWithTitle_("Cancel")

        text_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 20)))
        text_field.setStringValue_(str(current_value))
        alert.setAccessoryView_(text_field)

        response = alert.runModal()
        if response == NSAlertFirstButtonReturn:
            try:
                return float(text_field.stringValue())
            except ValueError:
                return None
        return None

    # ─── Control actions

    def toggleMonitoring_(self, sender: Any) -> None:
        """Toggle pause/resume of the narc monitoring loop."""
        if not self._state:
            return

        snapshot = self._state.get_snapshot()
        if snapshot["monitoring_active"]:
            # Pause: request shutdown
            self._state.request_shutdown()
        else:
            # Resume: clear shutdown flag and restart narc thread
            if self._narc_thread and not self._narc_thread.is_alive():
                from narc import run

                self._state.clear_shutdown()
                self._narc_thread = threading.Thread(
                    target=lambda: run(self._state, self._settings), daemon=True
                )
                self._narc_thread.start()

    def showCameraPreview_(self, sender: Any) -> None:
        """Open a floating camera preview window or bring existing one to front."""
        if self._camera_window:
            self._camera_window.makeKeyAndOrderFront_(None)
            return

        # Create small floating window (240×180)
        frame = ((100, 100), (240, 180))
        style_mask = (
            NSTitledWindowMask
            | NSClosableWindowMask
            | NSResizableWindowMask
        )
        win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame, style_mask, NSBackingStoreBuffered, False
        )
        win.setTitle_("Hydration Narc — Camera")
        win.setLevel_(NSFloatingWindowLevel)

        # Add image view to display camera feed
        image_view = NSImageView.alloc().initWithFrame_(((0, 0), (240, 180)))
        image_view.setImageScaling_(2)  # NSImageScaleProportionallyUpOrDown
        win.contentView().addSubview_(image_view)

        win.makeKeyAndOrderFront_(None)
        self._camera_window = win
        self._camera_image_view = image_view

        # Start fast refresh timer for camera preview (10fps)
        self._camera_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.1, self, "cameraTimerFired:", None, True
        )

    def cameraTimerFired_(self, timer: Any) -> None:
        """Called every 0.1s on main thread — refresh camera preview from shared frame."""
        if not self._camera_window or not self._state or not self._camera_image_view:
            return

        snapshot = self._state.get_snapshot()
        frame_bytes = snapshot["last_frame"]

        if not frame_bytes:
            return

        try:
            # Convert JPEG bytes to NSImage
            data = NSData.dataWithBytes_length_(frame_bytes, len(frame_bytes))
            image = NSImage.alloc().initWithData_(data)
            if image:
                self._camera_image_view.setImage_(image)
        except Exception:
            pass

    def quitApp_(self, sender: Any) -> None:
        """Request shutdown and terminate the application."""
        # Stop camera timer if running
        if self._camera_timer:
            self._camera_timer.invalidate()
            self._camera_timer = None

        # Close camera window if open
        if self._camera_window:
            self._camera_window.close()
            self._camera_window = None

        if self._state:
            self._state.request_shutdown()

        # Give narc thread time to clean up
        if self._narc_thread:
            self._narc_thread.join(timeout=2.0)

        NSApplication.sharedApplication().terminate_(self)
