import pandas as pd
import streamlit as st
st.set_page_config(page_title="AJO Journey Lab",page_icon="🧭",layout="wide")
st.title("🧭 Adobe Journey Optimizer | Journey Simulation Lab")
st.caption("Event entry → consent and eligibility → wait → condition → channel action → conversion exit")
st.info("Local simulator only. It does not connect to AJO or send messages.")
people=[
{"id":"C-1001","name":"Aarav Mehta","email_ok":True,"sms_ok":True,"purchased":False,"weekly":1,"gap":30,"cart":24999},
{"id":"C-1002","name":"Diya Shah","email_ok":False,"sms_ok":True,"purchased":False,"weekly":0,"gap":48,"cart":7999},
{"id":"C-1003","name":"Kabir Rao","email_ok":True,"sms_ok":False,"purchased":True,"weekly":2,"gap":28,"cart":65999},
{"id":"C-1004","name":"Mira Iyer","email_ok":True,"sms_ok":True,"purchased":False,"weekly":3,"gap":8,"cart":18999}]
df=pd.DataFrame(people)
a,b,c=st.columns(3); a.metric("Profiles",len(df)); b.metric("Entry event","cart_abandoned"); c.metric("Default wait","60 min")
t1,t2,t3,t4=st.tabs(["Journey designer","Run simulation","QA and measurement","Integration contract"])
with t1:
 st.subheader("Abandoned cart recovery topology")
 st.graphviz_chart('''digraph journey {rankdir=LR; node [shape=box,style="rounded,filled",fillcolor="#EAF2FF"]; A [label="Entry: cart_abandoned"]; B [label="Consent + audience"]; C [label="Wait 60 min"]; D [label="Purchase since entry?"]; E [label="Email reminder"]; F [label="Wait 24 h"]; G [label="SMS follow-up"]; H [label="Exit"]; A->B->C->D; D->H [label="Yes"]; D->E [label="No"]; E->F->G->H;}''')
 st.markdown("Every journey must include event eligibility, consent, frequency control, conversion exit and auditable outcomes.")
with t2:
 p=st.selectbox("Customer",people,format_func=lambda x:f"{x['name']} ({x['id']})")
 wait=st.slider("Delay after abandonment (minutes)",15,180,60,15)
 cap=st.slider("Max impressions in 7 days",1,5,3)
 gap=st.slider("Minimum hours between messages",1,72,24)
 discount=st.slider("Proposed discount (%)",0,40,10)
 channel=st.selectbox("First channel",["Email","SMS"])
 consent=p["email_ok"] if channel=="Email" else p["sms_ok"]
 if st.button("Run journey",type="primary"):
  rows=[
  ("Entry event","PASS","cart_abandoned received"),
  ("Channel consent","PASS" if consent else "BLOCK","Consent present" if consent else "Consent is false"),
  ("Frequency cap","PASS" if p["weekly"]<cap else "BLOCK",f"{p['weekly']} impressions; cap {cap}"),
  ("Minimum gap","PASS" if p["gap"]>=gap else "WAIT",f"{p['gap']} hours since last message; minimum {gap}"),
  ("Purchase exit","EXIT" if p["purchased"] else "CONTINUE","Purchase recorded" if p["purchased"] else "No purchase recorded"),
  ("Offer cap","PASS" if discount<=25 else "BLOCK",f"{discount}% proposed; maximum 25%")]
  st.dataframe(pd.DataFrame(rows,columns=["Step","Result","Reason"]),use_container_width=True,hide_index=True)
  blocked=(not consent or p["weekly"]>=cap or p["gap"]<gap or p["purchased"] or discount>25)
  if p["purchased"]: st.success("Exit journey: converted profile. Do not send.")
  elif blocked: st.error("No send: a consent, fatigue, timing or offer policy blocked the action.")
  else: st.success(f"Eligible for simulated {channel} after {wait} minutes. No real message was sent.")
with t3:
 checks=["Entry event schema and identity verified","Audience qualification current","Salesforce consent synchronized to AEP","Channel consent checked at send time","Purchase exit condition configured","Frequency cap and minimum gap configured","Offer tier, stock and discount cap validated","Suppression, quiet hours and channel surface checked","Holdout and conversion KPI defined","Audit event and rejection reason captured"]
 done=[st.checkbox(x,key=x) for x in checks]
 st.metric("QA completion",f"{sum(done)}/{len(done)}"); st.progress(sum(done)/len(done))
 st.write("Measure incremental conversion vs holdout, revenue per eligible profile, opt-out rate, complaints and exit reasons. Click rate alone does not prove incremental impact.")
 st.warning("Production AJO also requires channel surfaces, message configuration, quiet hours, suppression and profile checks.")

with t4:
 st.subheader("Shared AEP lifecycle event contract")
 st.caption("Preview the event AJO would publish to the shared lifecycle stream. No network call is made.")
 p=st.selectbox("Customer for hand-off",people,key="contract_person",format_func=lambda x:f"{x['name']} · {x['id']}")
 channel=st.selectbox("Outcome channel",["EMAIL","SMS","NONE"],key="contract_channel")
 consent=p["email_ok"] if channel=="EMAIL" else p["sms_ok"] if channel=="SMS" else True
 correlation=f"CORR-{p['id']}-AJO-001"
 payload={"eventId":"LCE-"+correlation,"correlationId":correlation,"occurredAt":pd.Timestamp.now(tz="UTC").isoformat(),"source":"AJO","eventType":"message_eligible" if consent else "message_blocked","customer":{"crmId":p["id"]},"journey":{"journeyId":"JRN-CART-001","journeyName":"Abandoned cart recovery","step":"channel_decision","channel":channel},"consent":{"email":"GRANTED" if p["email_ok"] else "DENIED","sms":"GRANTED" if p["sms_ok"] else "DENIED"},"status":"ELIGIBLE" if consent else "BLOCKED","reason":"Channel consent granted" if consent else "Channel consent missing"}
 st.json(payload)
 st.download_button("Download lifecycle event JSON",pd.Series(payload).to_json(indent=2).encode("utf-8"),file_name="ajo_lifecycle_event.json",mime="application/json")
 st.info("Canonical JSON Schema is in the shared contracts folder. This is a synthetic payload preview, not a live AEP event ingestion.")

with st.expander("AEP-to-AJO architecture mapping"):
 st.markdown("**Event:** cart_abandoned ExperienceEvent from AEP.\n\n**Profile:** AEP Real-Time Customer Profile and audience eligibility.\n\n**Journey:** event entry, wait, condition, message action and exit.\n\n**Governance:** consent, fatigue, discount cap, stock and audit logging.\n\n**Measurement:** AJO outcomes in AEP datasets for analysis and CRM feedback.")
st.caption("Source alignment: Consolidated Adobe/AEP/AJO/Salesforce Guide and MarTech 2030 Governed AI Agent Architecture. Synthetic profiles only.")
