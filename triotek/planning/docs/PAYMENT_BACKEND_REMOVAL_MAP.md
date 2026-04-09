# Payment Backend Removal Map

## Purpose

Map the remaining Press-derived payment backend so cleanup can continue in controlled passes after the dashboard payment UI has been removed.

## Current Rule

`3plug-control` should not own payment or billing behavior.

That means the backend direction is:

* stop live payment wiring in the control plane where it is low risk to do so
* document the remaining payment logic that still exists in the Press base
* defer deeper code and doctype deletion until the dependencies are mapped more fully

## Live Wiring Already Reduced

The current hook cleanup already removes several payment and SaaS scheduler and permission entries from [hooks.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/hooks.py).

Examples already deferred there:

* `Subscription`
* `Stripe Payment Method`
* `Invoice`
* `Stripe Webhook Log` doc events
* billing and payout scheduler targets
* signup and SaaS scheduler targets

## Next Low-Risk Backend Cuts

These are the next safe candidates for hook-level or permission-level reduction:

* `Balance Transaction`
* remaining payment-related method permissions
* remaining payment-related scheduler targets if they surface through later sweeps

Reason:

* these are payment records rather than core server, bench, site, or job records
* reducing their live permissions lowers accidental exposure while deeper cleanup is still pending

## Remaining Payment-Coupled Core Code

These files still contain payment assumptions and should be revisited later with care:

* [team.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/team/team.py)
* [server.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/server/server.py)
* [site.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/site/site.py)

Examples of remaining coupling:

* subscription creation and lookup
* invoice lookups
* payment mode checks
* partner-paid or prepaid assumptions
* Razorpay-specific plan-change exceptions

These are not good first deletion targets because they sit close to site and server lifecycle behavior.

## Remaining Payment-Oriented Doctypes

Examples still present in the Press base:

* `invoice`
* `invoice_credit_allocation`
* `invoice_discount`
* `invoice_item`
* `invoice_transaction_fee`
* `subscription`
* `payment_due_extension`
* `payment_gateway`
* `payment_dispute`
* `stripe_payment_method`
* `stripe_payment_event`
* `razorpay_mandate`
* `razorpay_payment_record`
* `razorpay_webhook_log`
* `mpesa_setup`
* `mpesa_payment_record`
* `partner_payment_payout`

These should be treated as deferred backend cleanup inventory, not active 3plug product scope.

## Recommended Cleanup Sequence

1. finish hook and permission reduction
2. classify payment-related method permissions and API entry points
3. map the remaining team, server, and site payment coupling
4. only then start removing deeper backend payment doctypes and code

## Boundary Reminder

The admin or business site should own:

* invoices
* customer billing
* cards
* M-Pesa
* prepaid balances
* vendor or payout logic

`3plug-control` should own:

* infrastructure control
* operator workflows
* jobs
* logs
* forensics
