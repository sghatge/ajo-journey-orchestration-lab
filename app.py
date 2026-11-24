import json
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AJO Journey Intelligence Lab", page_icon="🧭", layout="wide")

st.title("🧭 Adobe Journey Optimizer | Journey Intelligence Lab")
st.caption("Design • Simulate • Govern • Measure customer journeys")
st.info("Educational simulator using synthetic profiles. It does not connect to Adobe Experience Platform or AJO and never sends real messages.")

PROFILES = [
    {"customer_id":"C-1001","name":"Aarav Mehta","tier":"Gold","cart_value":24999,"email_consent":True,"sms_consent":True,"purchased":False,"impressions_7d":1,"hours_since_last":30,"last_event":"cart_abandoned"},
    {"customer_id":"C-1002","name":"Diya Shah","tier":"Silver","cart_value":7999,"email_consent":False,"sms_consent":True,"purchased":False,"impressions_7d":0,"hours_since_last":48,"last_event":"cart_abandoned"},
    {"customer_id":"C-1003","name":"Kabir Rao","tier":"Platinum","cart_value":65999,"email_consent":True,"sms_consent":False,"purchased":True,"impressions_7d":2,"hours_since_last":28,"last_event":"purchase"},
    {"customer_id":"C-1004","name":"Mira Iyer","tier":"Gold","cart_value":18999,"email_consent":True,"sms_consent":True,"purchased":False,"impressions_7d":3,"hours_since_last":8,"last_event":"cart_abandoned"},
    {"customer_id":"C-1005","name":"Neel Kapoor","tier":"Bronze","cart_value":3499,"email_consent":True,"sms_consent":False,"purchased":False,"impressions_7d":0,"hours_since_last":72,"last_event":"cart_abandoned"},
    {"customer_id":"C-1006","name":"Tara Desai","tier":"Platinum","cart_value":42999,"email_consent":True,"sms_consent":True,"purchased":False,"impressions_7d":1,"hours_since_last":36,"last_event":"cart_abandoned"},
]
profiles = pd.DataFrame(PROFILES)

def evaluate(profile, channel, cap, min_gap, max_discount, discount, require_purchase_exit=True):
    consent_key = "email_consent" if channel == "Email" else "sms_consent"
    checks = [
        ("Entry event", profile["last_event"] == "cart_abandoned", "Cart-abandonment event present" if profile["last_event"] == "cart_abandoned" else f"Latest event is {profile['last_event']}"),
        ("Channel consent", bool(profile[consent_key]), f"{channel} consent is {'granted' if profile[consent_key] else 'not granted'}"),
        ("Frequency cap", profile["impressions_7d"] < cap, f"{profile['impressions_7d']} impressions in 7 days; cap is {cap}"),
        ("Minimum contact gap", profile["hours_since_last"] >= min_gap, f"{profile['hours_since_last']} hours since last contact; minimum is {min_gap}"),
        ("Purchase exit", not (require_purchase_exit and profile["purchased"]), "No purchase exit detected" if not profile["purchased"] else "Purchase detected; journey must exit"),
        ("Offer policy", discount <= max_discount, f"Proposed {discount}% discount; policy maximum is {max_discount}%"),
    ]
    results = [{"check":name,"status":"PASS" if passed else "BLOCK","explanation":reason} for name,passed,reason in checks]
    eligible = all(x[1] for x in checks)
    return eligible, results

def event_payload(profile, journey_name, channel, eligible, reasons):
    now = datetime.now(timezone.utc).isoformat()
    return {
        "eventId": f"AJO-SIM-{profile['customer_id']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "occurredAt": now,
        "source": "AJO_SIMULATOR",
        "eventType": "journey_action_eligible" if eligible else "journey_action_blocked",
        "customer": {"crmId": profile["customer_id"]},
        "journey": {"journeyName": journey_name, "step": "channel_action", "channel": channel.upper()},
        "decision": {"status": "ELIGIBLE" if eligible else "BLOCKED", "reasons": reasons},
        "synthetic": True
    }

tab_overview, tab_design, tab_sim, tab_decision, tab_qa, tab_analytics, tab_contract = st.tabs([
    "Overview", "Journey Designer", "Simulation", "Decisioning", "QA & Governance", "Analytics", "Event Contract"
])

with tab_overview:
    st.subheader("Journey operating model")
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Synthetic profiles", len(profiles))
    k2.metric("Journey scenario", "Abandoned cart")
    k3.metric("Channels", "Email + SMS")
    k4.metric("Live sends", "Disabled")
    st.graphviz_chart("""
    digraph journey {
      rankdir=LR; graph [bgcolor="transparent"]; node [shape=box,style="rounded,filled",fontname="Arial",color="#64748b",fillcolor="#eaf2ff"];
      entry [label="Event entry\\ncart_abandoned"]; qualify [label="Audience +\\nidentity checks"]; wait1 [label="Wait\\n60 minutes"];
      purchase [label="Purchase\\nsince entry?"]; email [label="Email action\\nconsent + fatigue"]; wait2 [label="Wait\\n24 hours"];
      sms [label="SMS action\\nre-check consent"]; exit [label="Exit +\\noutcome event"];
      entry->qualify->wait1->purchase; purchase->exit [label="Yes"]; purchase->email [label="No"]; email->wait2->sms->exit;
    }
    """)
    st.markdown("**Design principle:** every action is conditional. Re-check consent, purchase suppression and contact fatigue at the point of action; record why a profile continued, waited, exited or was blocked.")

    st.markdown("#### Journey decision map")
    st.graphviz_chart("""
    digraph decision {
      rankdir=TB; graph [bgcolor="transparent",pad="0.2",nodesep="0.28",ranksep="0.38"];
      node [shape=box,style="rounded,filled",fontname="Arial",fontsize=10,color="#7892b5",fillcolor="#edf4ff"];
      edge [color="#64748b",fontname="Arial",fontsize=9,arrowsize=0.75];
      entry [label="Event received"];
      consent [label="Channel consent?"];
      fatigue [label="Frequency + quiet-time checks?"];
      bought [label="Purchase detected?"];
      send [label="Simulate action",fillcolor="#dcf5e8",color="#29945b"];
      block [label="Block + record reason",fillcolor="#ffe4e6",color="#d44d5c"];
      exit [label="Exit journey",fillcolor="#eee8ff",color="#7554c7"];
      entry->consent; consent->fatigue [label="Yes"]; consent->block [label="No"];
      fatigue->bought [label="Pass"]; fatigue->block [label="Fail"];
      bought->exit [label="Yes"]; bought->send [label="No"];
    }
    """)

    st.warning("This topology is a conceptual journey blueprint. Actual AJO capabilities, limits and configuration depend on tenant licensing and implementation.")

with tab_design:
    st.subheader("Configure a reusable journey blueprint")
    journey_name = st.text_input("Journey name", "Abandoned Cart Recovery")
    c1,c2 = st.columns(2)
    with c1:
        entry_event = st.selectbox("Entry event", ["cart_abandoned","product_viewed","checkout_started","subscription_renewal_due"])
        entry_audience = st.selectbox("Entry audience", ["Cart value > ₹5,000","Gold or Platinum customers","All eligible cart abandoners"])
        first_channel = st.selectbox("First channel", ["Email","SMS"])
        first_wait = st.number_input("Wait before first action (minutes)", min_value=0, max_value=10080, value=60, step=15)
    with c2:
        followup_channel = st.selectbox("Follow-up channel", ["SMS","Email"])
        followup_wait = st.number_input("Wait before follow-up (hours)", min_value=1, max_value=168, value=24)
        exit_event = st.selectbox("Conversion / exit event", ["purchase","subscription_started","booking_confirmed"])
        journey_ttl = st.number_input("Journey expiry (hours)", min_value=1, max_value=720, value=72)
    st.markdown("**Journey summary**")
    st.write(f"{entry_event} → {entry_audience} → wait {first_wait} min → {first_channel} → wait {followup_wait} h → {followup_channel} → exit on {exit_event} or {journey_ttl} h expiry.")
    spec = {"journey_name":journey_name,"entry_event":entry_event,"entry_audience":entry_audience,"first_channel":first_channel,"first_wait_minutes":first_wait,"followup_channel":followup_channel,"followup_wait_hours":followup_wait,"exit_event":exit_event,"journey_expiry_hours":journey_ttl,"synthetic":True}
    st.download_button("Download journey specification JSON", json.dumps(spec, indent=2).encode(), file_name="ajo_journey_spec.json", mime="application/json")

with tab_sim:
    st.subheader("Run a customer through the journey")
    selected_id = st.selectbox("Select synthetic customer", profiles["customer_id"].tolist(), format_func=lambda x: f"{profiles.loc[profiles.customer_id==x,'name'].iloc[0]} ({x})")
    profile = profiles.loc[profiles.customer_id==selected_id].iloc[0].to_dict()
    st.dataframe(pd.DataFrame([profile]), use_container_width=True, hide_index=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        channel = st.selectbox("Action channel", ["Email","SMS"], key="sim_channel")
        wait = st.slider("Wait before action (minutes)", 0, 240, 60, 15)
    with c2:
        cap = st.slider("Maximum marketing impressions / 7 days", 1, 6, 3)
        min_gap = st.slider("Minimum hours between contacts", 1, 72, 24)
    with c3:
        discount = st.slider("Proposed offer discount (%)", 0, 40, 10)
        max_discount = st.slider("Offer policy maximum (%)", 0, 40, 25)
    if st.button("Simulate journey decision", type="primary"):
        eligible, checks = evaluate(profile, channel, cap, min_gap, max_discount, discount)
        st.session_state["last_simulation"] = {"profile":profile,"channel":channel,"eligible":eligible,"checks":checks,"wait":wait,"journey_name":"Abandoned Cart Recovery"}
        st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
        if eligible:
            st.success(f"Eligible for a simulated {channel} action after {wait} minutes. No message was sent.")
        elif profile["purchased"]:
            st.info("Journey exits because the customer has purchased. Suppress all remaining marketing actions.")
        else:
            st.error("Action blocked. Review the failed checks before attempting another channel or journey step.")
    if "last_simulation" in st.session_state:
        st.caption("Most recent simulation is available in the Event Contract tab.")

with tab_decision:
    st.subheader("Offer decisioning sandbox")
    tier = st.selectbox("Customer tier", ["Bronze","Silver","Gold","Platinum"])
    cart = st.number_input("Cart value (₹)", min_value=0, max_value=500000, value=25000, step=1000)
    inventory = st.selectbox("Inventory status", ["In stock","Low stock","Out of stock"])
    margin_ok = st.checkbox("Offer preserves minimum margin", value=True)
    requested = st.slider("Requested discount (%)", 0, 50, 10)
    tier_cap = {"Bronze":5,"Silver":10,"Gold":15,"Platinum":20}[tier]
    allowed = min(tier_cap, 25)
    valid = inventory != "Out of stock" and margin_ok and requested <= allowed and cart > 0
    st.metric("Maximum tier discount", f"{allowed}%")
    if valid:
        st.success(f"Offer passes lab policy: {requested}% discount on ₹{cart:,.0f} cart.")
    else:
        st.error("Offer rejected by inventory, margin, cart-value or tier-discount policy.")
    st.caption("Illustrative business rules only. Real offer eligibility must use approved commercial and inventory sources.")

with tab_qa:
    st.subheader("Pre-publish QA checklist")
    checks = [
        "Entry event schema, namespace and identity are validated",
        "Entry audience and exclusion logic are documented",
        "Consent is checked for each channel at action time",
        "Purchase / conversion exit is configured",
        "Frequency cap and minimum contact gap are configured",
        "Wait, timeout and journey expiry behaviour are defined",
        "Offer tier, inventory, margin and discount rules are tested",
        "Message content, links, personalization and fallback are tested",
        "Quiet hours, suppression and channel surface are reviewed",
        "Holdout group and success KPI are defined",
        "Blocked / exited outcomes are auditable",
        "Test identities and non-production channels are used"
    ]
    completed = [st.checkbox(item, key="qa_"+str(i)) for i,item in enumerate(checks)]
    score = sum(completed)
    st.metric("QA readiness", f"{score}/{len(checks)}", f"{score/len(checks):.0%} complete")
    st.progress(score/len(checks))
    if score == len(checks):
        st.success("All lab QA checks marked complete. This is not a substitute for formal production approval.")
    else:
        st.info(f"{len(checks)-score} checks remain.")

with tab_analytics:
    st.subheader("Journey performance — synthetic demonstration data")
    base = profiles.copy()
    base["eligible_email"] = base.apply(lambda r: evaluate(r.to_dict(),"Email",3,24,25,10)[0], axis=1)
    base["eligible_sms"] = base.apply(lambda r: evaluate(r.to_dict(),"SMS",3,24,25,10)[0], axis=1)
    total = len(base)
    email_eligible = int(base.eligible_email.sum())
    sms_eligible = int(base.eligible_sms.sum())
    converted = int(base.purchased.sum())
    a,b,c,d = st.columns(4)
    a.metric("Profile sample", total)
    b.metric("Email eligible", email_eligible)
    c.metric("SMS eligible", sms_eligible)
    d.metric("Already converted", converted)
    summary = pd.DataFrame([
        {"stage":"Sample profiles","profiles":total},
        {"stage":"Email eligible","profiles":email_eligible},
        {"stage":"SMS eligible","profiles":sms_eligible},
        {"stage":"Purchase exits","profiles":converted},
        {"stage":"Email blocked","profiles":total-email_eligible},
        {"stage":"SMS blocked","profiles":total-sms_eligible},
    ])
    st.bar_chart(summary.set_index("stage"))
    st.markdown("#### Journey eligibility funnel")
    funnel = pd.DataFrame([
        {"stage":"All sample profiles","profiles":total},
        {"stage":"Email eligible","profiles":email_eligible},
        {"stage":"SMS eligible","profiles":sms_eligible},
        {"stage":"Purchase exits","profiles":converted},
    ])
    st.bar_chart(funnel.set_index("stage"))

    st.dataframe(base[["customer_id","tier","cart_value","eligible_email","eligible_sms","purchased","impressions_7d"]], use_container_width=True, hide_index=True)
    st.download_button("Export analytics CSV", summary.to_csv(index=False).encode(), file_name="ajo_journey_analytics.csv", mime="text/csv")
    st.caption("These are deterministic sample-profile counts, not campaign results, delivery metrics or measured incremental lift.")

with tab_contract:
    st.subheader("AJO lifecycle outcome event preview")
    sim = st.session_state.get("last_simulation")
    if sim:
        p = sim["profile"]
        eligible = sim["eligible"]
        reasons = [x["explanation"] for x in sim["checks"] if x["status"] != "PASS"]
        payload = event_payload(p, sim["journey_name"], sim["channel"], eligible, reasons or ["All lab checks passed"])
    else:
        st.info("Run a simulation first to generate an outcome event preview.")
        p = profiles.iloc[0].to_dict()
        payload = event_payload(p, "Abandoned Cart Recovery", "Email", False, ["No simulation has been run"])
    st.json(payload)
    st.download_button("Download lifecycle event JSON", json.dumps(payload, indent=2).encode(), file_name="ajo_lifecycle_outcome.json", mime="application/json")
    st.caption("Preview only. No event is ingested into AEP, and no Salesforce action or message send is triggered.")

st.divider()
st.caption("AJO Journey Intelligence Lab • Synthetic data • Educational use • No live Adobe tenant connection")
