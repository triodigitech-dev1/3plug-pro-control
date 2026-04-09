# Press Study

## What Press is

Local reference reviewed:

* `../frappe-press/README.md`
* `../frappe-press/press/press/doctype`
* `../frappe-press/press/agent.py`
* `../frappe-press/dashboard/src`

Press is a full hosting platform, not only a Bench wrapper.

It includes:

* a Frappe backend with many infrastructure records
* a separate dashboard SPA
* agent and job orchestration
* server, bench, site, deploy, billing, marketplace, and team concerns

## What Press shows us structurally

The local doctype set includes records such as:

* `Server`
* `Database Server`
* `Proxy Server`
* `Cluster`
* `Bench`
* `Site`
* `Agent Job`
* `App Source`
* `Deploy`
* `Team`
* `Plan`

This shows that Press is designed for a broader cloud operating model with multiple server roles and wider platform concerns.

## What 3plug should keep

Keep these ideas from Press:

* Frappe app backend as the source of truth
* dashboard as the main operator surface
* job and agent execution for real actions
* server, bench, site, and app-source records
* Bench as the execution layer for Bench-owned actions

## What 3plug should simplify

For v1, simplify Press into:

* one 3plug deployment per managed server
* one managed Linux server inside that deployment
* many benches on that server
* many sites on those benches

This means 3plug should not start by reproducing Frappe Cloud's broader shared control-plane model.

## What 3plug should defer

Defer these Press areas unless they directly serve the first slice:

* multiple server-role orchestration across many machines
* broader cloud provider management
* billing and subscriptions
* marketplace breadth
* advanced cluster and distributed infrastructure features
* wider team and self-service product layers

## Decision for current work

Use Press as the base.

Do not keep building the main product in the old coordination repo.

Build 3plug in `3plug-control` as a Press-derived product with a one-server-per-deployment security model first.

See also:

* `PRESS_KEEP_DEFER_MAP.md`
