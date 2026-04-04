"""Entry point for menu bar app — spins narc daemon on background thread."""

from __future__ import annotations

import threading

from AppKit import NSApplication
from PyObjCTools import AppHelper

import narc
from menubar import NarcMenuBarApp
from shared_state import NarcState
from settings_store import SettingsStore


if __name__ == "__main__":
    # 1. Create shared objects
    state = NarcState()
    settings = SettingsStore()
    settings.load()

    # 2. Start narc on background thread BEFORE NSApp initialization
    def narc_thread_target() -> None:
        narc.run(state, settings)
        state.monitoring_active = False

    narc_thread = threading.Thread(target=narc_thread_target, daemon=True)
    narc_thread.start()

    # 3. NSApp setup (main thread must own the application object)
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(1)  # NSApplicationActivationPolicyAccessory (no Dock icon)

    # 4. Build and attach menu bar delegate
    menu_bar_app = NarcMenuBarApp.alloc().init()
    menu_bar_app._state = state
    menu_bar_app._settings = settings
    menu_bar_app._narc_thread = narc_thread
    app.setDelegate_(menu_bar_app)

    # 5. Hand main thread to AppKit event loop
    AppHelper.runEventLoop()
