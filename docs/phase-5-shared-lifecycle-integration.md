# Phase 5 — Shared lifecycle integration

The AJO lab now includes an **Integration contract** tab and the shared contract files:
- `contracts/customer-lifecycle-event.json`
- `contracts/salesforce-followup-action.json`

Use the tab to preview an AJO-originated lifecycle event with a correlation ID, journey identity, channel, consent and eligible/blocked outcome. The payload is synthetic and is not ingested into AEP.

The canonical end-to-end sequence is documented in the AEP repository: `docs/enterprise-lifecycle-integration.md`. The three labs remain independently deployable. Production event delivery, message activation and CRM writes are not enabled.
