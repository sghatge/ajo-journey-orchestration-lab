# Abandoned-cart journey blueprint

## Objective
Recover eligible abandoned carts with relevant reminders while respecting consent, customer fatigue and conversion exits.

## Entry criteria
- An identified or resolvable profile has an `addToCart` event.
- Cart remains unpurchased after the configured 60-minute evaluation window.
- Profile is eligible for the journey and has valid consent for the selected channel.
- Exclude employees, test profiles, fraud/risk holds and suppressed customers where applicable.

## Path
Entry → wait/evaluate 60 minutes → purchase check → email eligibility check → email reminder → wait 24 hours → purchase and consent re-check → SMS eligibility check → SMS reminder → wait/evaluate 24 hours → final email only if still eligible → expiry.

## Global exits
Purchase, consent withdrawal, profile deletion request, invalid identity, fraud/suppression flag, journey expiry or manual suppression.

## Personalization contract
Use first name, cart item name/image, cart total, currency and deep link only when available and valid. Provide a neutral fallback when attributes are missing. Never render raw nulls or unsafe URLs.

## Offer policy
No discount by default. If an incentive is considered, validate loyalty tier, inventory, margin floor, promotion eligibility and configured discount cap. The example 25% ceiling in the reference notes is a lab parameter only and requires business approval.

## Measurement
Primary: recovered orders / eligible abandoned carts. Secondary: incremental revenue, time to purchase, channel conversion, unsubscribe/opt-out, complaints and frequency-policy violations. Use a holdout/control group before claiming incrementality.