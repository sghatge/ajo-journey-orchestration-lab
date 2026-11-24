"""Illustrative local eligibility simulation; does not send messages."""
import json
from pathlib import Path


def eligible(profile: dict, channel: str) -> tuple[bool, str]:
    if profile.get("purchaseWithin60m"):
        return False, "purchase detected — exit journey"
    consent = profile.get(f"{channel}Consent", "UNKNOWN")
    if consent != "GRANTED":
        return False, f"{channel} consent is {consent.lower()} — block action"
    return True, "eligible for simulated action"


def main() -> None:
    rows = json.loads(Path("data/sample-events.json").read_text())
    for row in rows:
        email_ok, email_reason = eligible(row, "email")
        sms_ok, sms_reason = eligible(row, "sms")
        print(f"{row['profileId']}: email={email_ok} ({email_reason}); sms={sms_ok} ({sms_reason})")

if __name__ == "__main__":
    main()