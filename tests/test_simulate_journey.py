import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from simulate_journey import eligible

def test_purchase_exits_journey():
    ok, reason = eligible({"purchaseWithin60m": True, "emailConsent": "GRANTED"}, "email")
    assert not ok and "purchase" in reason

def test_unknown_consent_blocks():
    ok, reason = eligible({"purchaseWithin60m": False, "emailConsent": "UNKNOWN"}, "email")
    assert not ok and "block" in reason

def test_granted_consent_allows_simulation():
    ok, _ = eligible({"purchaseWithin60m": False, "smsConsent": "GRANTED"}, "sms")
    assert ok
