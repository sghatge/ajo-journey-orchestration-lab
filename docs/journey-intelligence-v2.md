# AJO Journey Intelligence Lab — Interactive Simulator

## Purpose
This lab demonstrates how an event-triggered customer journey can be designed, simulated, governed and measured. It uses deterministic synthetic profiles and is intended for learning and portfolio demonstration.

## Scenario
Abandoned-cart recovery:
1. Receive a synthetic `cart_abandoned` event.
2. Qualify the profile and check channel consent.
3. Apply a configurable wait.
4. Re-check purchase suppression, contact frequency and minimum contact gap.
5. Evaluate the proposed offer against tier, inventory, margin and discount policy.
6. Simulate an email or SMS action only when all checks pass.
7. Preview a lifecycle outcome event for downstream analytics.

## App modules
- **Overview:** journey topology and operating principles.
- **Journey Designer:** configure entry event, audience, channels, waits, exit event and expiry; export a JSON specification.
- **Simulation:** run a synthetic profile through entry, consent, fatigue, timing, purchase-exit and offer checks.
- **Decisioning:** evaluate illustrative tier-based discount, inventory and margin rules.
- **QA & Governance:** track pre-publish validation items.
- **Analytics:** inspect sample eligibility and suppression counts; export CSV.
- **Event Contract:** preview and export a synthetic outcome event.

## Local run
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Free deployment
Deploy the repository to Streamlit Community Cloud using:
- Repository: `sghatge/ajo-journey-orchestration-lab`
- Branch: `main`
- Main file: `app.py`

GitHub and Streamlit Community Cloud are used for the portfolio demo. No Vercel, paid database or paid hosting is required.

## Important limitations
- No live AEP or AJO tenant connection.
- No real message delivery, profile lookup, event ingestion or offer publication.
- All profiles, event outcomes and analytics are synthetic.
- Waits and branching are simulated synchronously; this is not a production journey runtime.
- Consent, frequency, offer and quiet-hour rules are illustrative and must be validated against the organisation's policies, legal requirements and Adobe tenant configuration.

## Portfolio learning outcomes
The lab demonstrates journey orchestration concepts: event entry, audience qualification, branching, wait/timeout design, conversion exits, channel consent, fatigue management, offer guardrails, QA and outcome measurement.
