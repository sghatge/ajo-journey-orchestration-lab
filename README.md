# Adobe Journey Optimizer — Journey Orchestration Lab

Hands-on lab for Adobe Journey Optimizer (AJO): event-triggered journeys, audience qualification, channel actions, offer decisioning, consent, fatigue controls and outcome measurement.

> This repository is a learning blueprint with synthetic data. It does not connect to or execute sends in a live AJO tenant.

## Business outcome
Design and validate relevant, consent-aware customer journeys that respond to behaviour and stop immediately when the customer converts or becomes ineligible.

## Reference scenario: abandoned cart
1. Website emits `addToCart` and subsequent cart-abandonment context to AEP.
2. AEP/Real-Time CDP evaluates cart age, identity and purchase suppression.
3. AJO starts an eligible journey.
4. Email reminder is considered after 60 minutes.
5. If no purchase, an SMS follow-up may be considered after 24 hours only when SMS consent is granted.
6. Purchase or other exit condition suppresses all remaining actions.
7. Journey outcomes are made available for measurement and CRM feedback.

## Journey guardrails
- Entry = qualifying event + audience eligibility + valid channel consent.
- Re-check consent and eligibility at the point of action where the implementation supports it.
- Exit on purchase, refund/return exception if relevant, consent withdrawal, or expiry.
- Example fatigue policy: maximum 3 marketing impressions in 7 days and at least 24 hours between messages. Treat these as configurable lab defaults, not universal legal or platform defaults.
- Offer eligibility must check tier, inventory, margin and discount policy.
- Always include wait, condition, timeout and exit behaviour in journey design.

## Repository map
- `docs/` — journey blueprint, event contract, QA and measurement
- `journeys/` — platform-neutral journey specification
- `data/` — synthetic events and profiles
- `src/` — local journey eligibility simulation
- `tests/` — journey rule tests
- `ROADMAP.md` — 8-week hands-on plan

## Run locally
```bash
python -m venv .venv
pip install -e .[dev]
pytest
python src/simulate_journey.py
```

## Shared lifecycle integration
The lab includes an Integration Contract tab and shares `contracts/customer-lifecycle-event.json` plus `contracts/salesforce-followup-action.json` with the AEP and Salesforce labs. See `docs/phase-5-shared-lifecycle-integration.md`. No live event ingestion or message send is enabled.

## Prerequisites for real AJO practice
An appropriately licensed AJO sandbox, AEP dataset/profile access, event configuration, channel surface and sender setup, test identities, and approval for any outbound testing. Start with test profiles and non-production channels.

## Source material
Based on the user's Google Drive consolidated Adobe/AEP/AJO/Salesforce guide and abandoned-cart case study. Validate tenant-specific capabilities and current product behaviour against Adobe documentation.