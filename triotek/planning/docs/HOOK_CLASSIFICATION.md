# Hook Classification

## Purpose

Classify `press/hooks.py` into keep-first and defer-first areas before deeper backend cleanup.

Reference:

* `press/hooks.py`

## Keep first

Keep first:

* core server, bench, site, app-source, deploy-candidate, and job permissions
* core site and server doc events
* core site, bench, backup, job, and maintenance scheduler work that supports the server to bench to site spine

## Defer first

Defer first:

* billing-related permissions and doc events
* marketplace-specific jinja filters and scheduler jobs
* Stripe webhook processing
* invoice finalization and payout creation jobs
* SaaS trial and signup scheduler jobs
* billing and partner audit scheduler jobs

## Safe reduction rule

For the first backend reduction:

* remove deferred hook wiring by exact key or exact scheduler target
* do not delete underlying modules yet
* do not remove core team, server, bench, site, or job permissions yet

## First candidates

Low-risk first candidates:

* `Subscription`
* `Stripe Payment Method`
* `Balance Transaction`
* `Invoice`
* `Stripe Webhook Log` doc event
* `Address` billing validation event
* `Marketplace App Subscription` doc event
* scheduler entries for marketplace auto-review, referral bonus, invoice finalization, payout creation, SaaS trial stats, subscription usage creation, signup e2e, and billing or partner audit jobs
