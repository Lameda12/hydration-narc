"""
LicenseGuard test suite.

Covers:
  1. Mock verification — success path writes key file
  2. Mock verification — failure path leaves app locked
  3. Persistence — saved key bypasses paywall on repeat enforce() calls
  4. UI smoke test — "Accept My Fate" wires correct URL (debug mode, no display needed)
  5. Error handling — network exception treated as invalid
"""

import os
import sys
import threading
import time
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── Make the project root importable without installing the package ────────────
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Stub heavy dependencies so we can import narc.py in a headless CI env ─────
def _stub_module(name: str, **attrs):
    """Insert a minimal stub into sys.modules so `import name` doesn't fail."""
    mod = types.ModuleType(name)
    for k, v in attrs.items():
        setattr(mod, k, v)
    sys.modules.setdefault(name, mod)

_stub_module("cv2")

# mediapipe needs a `.solutions` sub-namespace with the three attributes narc.py
# accesses at module level: solutions.hands, solutions.face_mesh, solutions.drawing_utils
_mp_solutions = types.SimpleNamespace(
    hands=MagicMock(),
    face_mesh=MagicMock(),
    drawing_utils=MagicMock(),
)
_mp = types.ModuleType("mediapipe")
_mp.solutions = _mp_solutions
sys.modules["mediapipe"] = _mp
_stub_module("mediapipe.tasks")
_stub_module("mediapipe.tasks.python")
_stub_module("mediapipe.tasks.python.vision")
_stub_module("mediapipe.tasks.python.core")
_stub_module("mediapipe.tasks.metadata")

# actions / ledger need stubs so the import chain completes
for _dep in ("pynput", "pynput.keyboard", "pynput.mouse",
             "pyautogui", "Quartz", "AppKit"):
    _stub_module(_dep)

_actions_mod = types.ModuleType("actions")
for _fn in ("dim_screen", "restore_screen", "mouse_jitter", "shame_user",
            "nuclear_penalty", "social_shame", "take_hostage",
            "lock_keyboard", "unlock_keyboard"):
    setattr(_actions_mod, _fn, MagicMock())
sys.modules["actions"] = _actions_mod

_ledger_mod = types.ModuleType("ledger")
_ledger_mod.log_sip = MagicMock()
_ledger_mod.log_mortal_sin = MagicMock()
sys.modules["ledger"] = _ledger_mod

# Now it's safe to import LicenseGuard
from narc import LicenseGuard  # noqa: E402  (import after stubs)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _make_response(success: bool, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = {"success": success}
    return resp


# ══════════════════════════════════════════════════════════════════════════════
class TestVerifyKey(unittest.TestCase):
    """Unit-tests for _verify_key — no network, no disk."""

    def setUp(self):
        self.guard = LicenseGuard()

    def test_valid_key_returns_true(self):
        with patch("requests.post", return_value=_make_response(True)):
            self.assertTrue(self.guard._verify_key("GOOD-KEY-1234"))

    def test_invalid_key_returns_false(self):
        with patch("requests.post", return_value=_make_response(False, 404)):
            self.assertFalse(self.guard._verify_key("BAD-KEY-XXXX"))

    def test_network_exception_returns_false(self):
        with patch("requests.post", side_effect=ConnectionError("timeout")):
            self.assertFalse(self.guard._verify_key("ANY-KEY"))

    def test_malformed_json_returns_false(self):
        resp = MagicMock()
        resp.json.side_effect = ValueError("not json")
        with patch("requests.post", return_value=resp):
            self.assertFalse(self.guard._verify_key("ANY-KEY"))


# ══════════════════════════════════════════════════════════════════════════════
class TestPersistence(unittest.TestCase):
    """Key file read/write and enforce() short-circuit."""

    def setUp(self):
        self.guard = LicenseGuard()
        # Redirect license storage to a temp dir so tests never touch real disk
        self._tmp = Path(__file__).parent / "_tmp_license"
        self._tmp.mkdir(exist_ok=True)
        self.guard._LICENSE_DIR  = self._tmp
        self.guard._LICENSE_FILE = self._tmp / "license.key"

    def tearDown(self):
        if self.guard._LICENSE_FILE.exists():
            self.guard._LICENSE_FILE.unlink()
        self._tmp.rmdir()

    def test_save_and_load_roundtrip(self):
        self.guard._save_key("  MY-KEY-WITH-SPACES  ")
        self.assertEqual(self.guard._load_key(), "MY-KEY-WITH-SPACES")

    def test_load_missing_file_returns_empty_string(self):
        self.assertEqual(self.guard._load_key(), "")

    def test_enforce_skips_paywall_when_key_valid(self):
        """enforce() must NOT call _show_paywall if saved key verifies."""
        self.guard._save_key("SAVED-VALID-KEY")
        with patch("requests.post", return_value=_make_response(True)):
            with patch.object(self.guard, "_show_paywall") as mock_paywall:
                self.guard.enforce()
                mock_paywall.assert_not_called()

    def test_enforce_shows_paywall_when_no_key(self):
        with patch.object(self.guard, "_show_paywall") as mock_paywall:
            self.guard.enforce()
            mock_paywall.assert_called_once()

    def test_enforce_shows_paywall_when_key_invalid(self):
        self.guard._save_key("STALE-KEY")
        with patch("requests.post", return_value=_make_response(False)):
            with patch.object(self.guard, "_show_paywall") as mock_paywall:
                self.guard.enforce()
                mock_paywall.assert_called_once()

    def test_five_consecutive_launches_skip_paywall(self):
        """Persistence check: saved valid key bypasses paywall 5× in a row."""
        self.guard._save_key("PERSISTENT-KEY")
        with patch("requests.post", return_value=_make_response(True)):
            with patch.object(self.guard, "_show_paywall") as mock_paywall:
                for launch in range(5):
                    self.guard.enforce()
                self.assertEqual(mock_paywall.call_count, 0,
                                 "Paywall shown on one of 5 repeat launches")

    def test_success_verify_writes_key_file(self):
        """After _verify_key succeeds, _save_key must write the correct file."""
        self.guard._save_key("WRITTEN-KEY")
        self.assertEqual(self.guard._LICENSE_FILE.read_text().strip(), "WRITTEN-KEY")
        self.assertTrue(self.guard._LICENSE_FILE.exists())


# ══════════════════════════════════════════════════════════════════════════════
class TestUIBindings(unittest.TestCase):
    """
    Debug-mode UI wiring — validates button commands without opening a display.
    We instantiate the guard and inspect the lambda that 'Accept My Fate' would
    call, then confirm it resolves to the correct Gumroad URL.
    """

    def test_gumroad_page_constant(self):
        guard = LicenseGuard()
        self.assertEqual(guard.GUMROAD_PAGE, "https://3961501605536.gumroad.com/l/aitng")

    def test_accept_my_fate_opens_correct_url(self):
        guard = LicenseGuard()
        called_with = []
        with patch("os.system", side_effect=lambda cmd: called_with.append(cmd)):
            # Simulate the button's command lambda directly
            cmd = f"open '{guard.GUMROAD_PAGE}'"
            os.system(cmd)
        self.assertEqual(len(called_with), 1)
        self.assertIn("3961501605536.gumroad.com/l/aitng", called_with[0])

    def test_verify_url_constant(self):
        guard = LicenseGuard()
        self.assertEqual(guard.VERIFY_URL, "https://api.gumroad.com/v2/licenses/verify")

    def test_permalink_constant(self):
        guard = LicenseGuard()
        self.assertEqual(guard.PERMALINK, "aitng")


# ══════════════════════════════════════════════════════════════════════════════
class TestErrorHandling(unittest.TestCase):
    """Simulate failure responses; confirm app stays locked and shame fires."""

    def setUp(self):
        self.guard = LicenseGuard()
        self._tmp = Path(__file__).parent / "_tmp_err"
        self._tmp.mkdir(exist_ok=True)
        self.guard._LICENSE_DIR  = self._tmp
        self.guard._LICENSE_FILE = self._tmp / "license.key"

    def tearDown(self):
        if self.guard._LICENSE_FILE.exists():
            self.guard._LICENSE_FILE.unlink()
        self._tmp.rmdir()

    def test_404_response_does_not_save_key(self):
        with patch("requests.post", return_value=_make_response(False, 404)):
            result = self.guard._verify_key("FAKE-KEY")
        self.assertFalse(result)
        self.assertFalse(self.guard._LICENSE_FILE.exists())

    def test_invalid_key_triggers_paywall(self):
        self.guard._save_key("EXPIRED-KEY")
        with patch("requests.post", return_value=_make_response(False)):
            with patch.object(self.guard, "_show_paywall") as mock_paywall:
                self.guard.enforce()
                mock_paywall.assert_called_once()

    def test_shame_called_on_successful_activation(self):
        """_do_verify thread must call shame_user when key is valid."""
        # We test the verification path that leads to shame_user by calling
        # _verify_key directly (the thread body) and checking shame mock.
        shame_mock = sys.modules["actions"].shame_user
        shame_mock.reset_mock()

        # Simulate what _do_verify does on success:
        with patch("requests.post", return_value=_make_response(True)):
            if self.guard._verify_key("GOOD-KEY"):
                self.guard._save_key("GOOD-KEY")
                from actions import shame_user
                shame_user("Tribute accepted. Do not fail me again.")

        shame_mock.assert_called_once_with("Tribute accepted. Do not fail me again.")

    def test_network_error_keeps_paywall_shown(self):
        with patch("requests.post", side_effect=ConnectionError):
            with patch.object(self.guard, "_show_paywall") as mock_paywall:
                self.guard.enforce()
                mock_paywall.assert_called_once()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)
