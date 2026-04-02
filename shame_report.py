"""The Shame Report — calculates your Hydration Purity Score and drafts your confession."""

import json
import os
import sys
from datetime import datetime, timezone

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "ledger.json")


def _load_ledger() -> list:
    if not os.path.exists(LEDGER_PATH):
        print("No ledger found. Either you are perfectly hydrated or the Narc hasn't started yet.")
        sys.exit(0)
    with open(LEDGER_PATH) as f:
        return json.load(f)


def _today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _tally(records: list, date: str | None = None) -> tuple[int, int]:
    """Return (sips, mortal_sins) optionally filtered to a single date (YYYY-MM-DD)."""
    sips = mortal_sins = 0
    for r in records:
        if date and not r.get("timestamp", "").startswith(date):
            continue
        if r["event"] == "sip":
            sips += 1
        elif r["event"] == "mortal_sin":
            mortal_sins += 1
    return sips, mortal_sins


def purity_score(sips: int, mortal_sins: int) -> int:
    return (sips * 10) - (mortal_sins * 50)


def generate_confession(sips: int, mortal_sins: int, score: int) -> str:
    raisin_pct  = min(100, mortal_sins * 20)
    disappoint  = 100 - raisin_pct
    return (
        f"I have failed the Narc. {mortal_sins} Mortal Sin{'s' if mortal_sins != 1 else ''} today. "
        f"I am {raisin_pct}% raisin, {disappoint}% disappointment. "
        f"Purity Score: {score}. "
        f"#HydrationNarc #MortalSin"
    )


def run(date: str | None = None) -> None:
    records = _load_ledger()
    target  = date or _today_utc()
    sips, mortal_sins = _tally(records, target)
    score = purity_score(sips, mortal_sins)

    print(f"\n{'─' * 44}")
    print(f"  HYDRATION NARC — SHAME REPORT ({target})")
    print(f"{'─' * 44}")
    print(f"  Sips logged    : {sips}")
    print(f"  Mortal Sins    : {mortal_sins}")
    print(f"  Purity Score   : {score:+d}")
    print(f"{'─' * 44}\n")

    if score < 0:
        confession = generate_confession(sips, mortal_sins, score)
        print("  CONFESSION REQUIRED:\n")
        print(f"  \"{confession}\"\n")
        from actions import post_to_x
        post_to_x(confession)
    elif sips == 0 and mortal_sins == 0:
        print("  No activity recorded today. The Narc is watching. It is always watching.\n")
    else:
        print(f"  Purity score is non-negative. You are merely mediocre, not condemned.\n")


if __name__ == "__main__":
    date_filter = sys.argv[1] if len(sys.argv) > 1 else None
    run(date_filter)
