# Backend Implementation Map

## Purpose

Turn the kept Press backend spine into a build-ready first implementation target for 3plug.

References:

* `app/DOCTYPE_MAP.md`
* `docs/PRESS_KEEP_DEFER_MAP.md`
* `../frappe-press/press/press/doctype`

## First records to implement

Implement these first in the backend:

* `3plug Server`
* `3plug Bench`
* `3plug Site`
* `3plug Job`
* `3plug App Source`
* `3plug Stack`

## Record relationships

### `3plug Server`

Role:

* the single managed server record for one 3plug deployment

Owns:

* many `3plug Bench`
* many `3plug Job`

### `3plug Bench`

Role:

* the managed Bench runtime on the server

Belongs to:

* one `3plug Server`

Owns:

* many `3plug Site`
* many `3plug Job`

### `3plug Site`

Role:

* the managed Frappe site on a bench

Belongs to:

* one `3plug Bench`

References:

* zero or one `3plug Stack`

### `3plug Job`

Role:

* the tracked execution record for platform actions

References:

* one `job_type`
* optional `3plug Server`
* optional `3plug Bench`
* optional `3plug Site`

### `3plug App Source`

Role:

* registry of approved app origins and allowed branches

Used by:

* `3plug Stack`
* install and validation flows

### `3plug Stack`

Role:

* approved installable app combinations for benches and sites

References:

* many approved `3plug App Source`

## First backend flows

### Register server

Backend should:

* create or update `3plug Server`
* record a `3plug Job`
* store readiness and capability status

### Register bench

Backend should:

* validate that the bench belongs to the managed server context
* create or update `3plug Bench`
* record a `3plug Job`
* refresh linked site inventory when possible

### Create site

Backend should:

* validate the target bench and stack
* create a queued `3plug Job`
* run the real Bench site-creation flow
* create or update `3plug Site`

### Install app on site

Backend should:

* validate the app against approved sources or stacks
* create a queued `3plug Job`
* run the real Bench install flow
* refresh `3plug Site`

## First backend rules

Rules:

* backend records are the source of truth for operator state
* every mutating action must create a `3plug Job`
* job state should be readable by the dashboard
* Bench remains the execution layer for Bench-owned operations
* one deployment manages one server in v1

## Immediate next implementation step

After this map, the next coding step should be to define the first actual backend model skeletons in the repo using this record set and relationship tree.

## Post-cleanup priority

Before broader product expansion, the first implementation task after cleanup should be the forensic layer described in:

* `FORENSIC_LAYER_PLAN.md`
