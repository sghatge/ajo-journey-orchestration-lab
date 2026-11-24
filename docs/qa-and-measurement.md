# AJO journey QA and measurement checklist

## Before activation
- Confirm event schema and identity resolution assumptions.
- Verify audience qualification, re-entry and suppression.
- Test purchase before entry, purchase during wait and purchase after each touch.
- Test granted, denied and unknown email/SMS consent independently.
- Test missing first name, product image, price, currency and deep link.
- Test duplicate events, late events and out-of-order timestamps.
- Verify frequency caps across concurrent journeys, not just this journey.
- Validate offer eligibility and inventory/margin rules.
- Check tracking, attribution windows, unsubscribe and preference-centre links.
- Use seed/test profiles and non-production destinations first.

## KPI definitions
- Journey entry rate = entered profiles / eligible profiles.
- Cart recovery rate = attributed purchases / eligible abandoned carts.
- Revenue recovered = sum of attributed purchase value under the approved attribution rule.
- Channel conversion = attributed conversions / delivered messages.
- Opt-out rate = opt-outs / delivered messages.

Metrics in examples are not real performance results. Establish a baseline and holdout before reporting lift.