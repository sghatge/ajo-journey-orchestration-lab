<div align="center">

<img src="https://raw.githubusercontent.com/sghatge/sghatge/main/assets/portfolio/project-banner.svg" width="100%" alt="Sangram Ghatge engineering portfolio banner">

**INDEPENDENT ENGINEERING PORTFOLIO · AJO JOURNEY ORCHESTRATION LAB**

[GitHub Profile](https://github.com/sghatge) · [Portfolio](https://sghatge.github.io/adobe-campaign-v8-governance/)

</div>

---

# Adobe Journey Optimizer — Journey Intelligence Lab

An interactive, hands-on learning lab for Adobe Journey Optimizer (AJO), built with Streamlit and synthetic customer data.

> **Educational simulator only:** this project does not connect to a live Adobe Experience Platform (AEP) or AJO tenant, ingest events, publish offers, or send messages.

## What you can explore
- **Journey Designer:** configure event entry, audience criteria, channels, waits, conversion exit and expiry.
- **Customer Journey Simulation:** test synthetic profiles against entry, consent, purchase suppression, frequency cap and minimum-gap rules.
- **Decisioning Sandbox:** evaluate tier-based discount limits, inventory and margin conditions.
- **QA & Governance:** track pre-publish checks for event identity, consent, fatigue, content, suppression and measurement.
- **Journey Analytics:** inspect synthetic eligibility and suppression counts, with CSV export.
- **Lifecycle Event Contract:** preview and download an outcome event for downstream AEP/CRM analytics.

## Reference scenario: abandoned-cart recovery
1. A synthetic `cart_abandoned` event enters the journey.
2. The profile is evaluated against the entry audience and eligibility rules.
3. A configurable wait is applied.
4. Purchase suppression, channel consent and contact fatigue are evaluated.
5. A channel action is simulated only if all required checks pass.
6. A follow-up action and conversion exit are represented in the journey blueprint.
7. An outcome event can be previewed for downstream measurement.

## Run locally
```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

## Deploy for free
Use Streamlit Community Cloud:
- Repository: `sghatge/ajo-journey-orchestration-lab`
- Branch: `main`
- Main file: `app.py`

No Vercel, paid hosting or hosted database is required.

## Documentation
See [Journey Intelligence Simulator](docs/journey-intelligence-v2.md) for the scenario, app modules, limitations and learning outcomes.

## Production boundary
This is a learning and portfolio project. Real AJO implementation requires a licensed tenant, AEP profile/event configuration, approved channel surfaces, message configuration, identity and consent design, test profiles, and formal operational/legal approval. The simulator's business rules are illustrative, not universal platform defaults or legal advice.
