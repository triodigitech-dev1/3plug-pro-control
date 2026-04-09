# First Doctype Map

## Press-derived starting objects

### `3plug Server`

Reference from Press:

* `Server`

3plug adaptation:

* starts with one active managed server
* stores host identity, operator context, and runtime readiness
* is the parent record for all benches in the deployment

Suggested first fields:

* `hostname`
* `public_ip`
* `private_ip`
* `status`
* `readiness_status`
* `agent_enabled`
* `bench_root`
* `notes`

### `3plug Bench`

Reference from Press:

* `Bench`
* `Bench App`
* `Bench Dependency`

3plug adaptation:

* stores bench path, Python/runtime details, app stack, and status for the managed server
* belongs to one `3plug Server`
* is the parent record for many `3plug Site` records

Suggested first fields:

* `server`
* `bench_name`
* `bench_path`
* `status`
* `frappe_branch`
* `python_version`
* `node_version`
* `apps_summary`
* `stack`
* `last_refreshed_on`

### `3plug Site`

Reference from Press:

* `Site`
* `Site App`
* `Site Domain`

3plug adaptation:

* stores site-to-bench relationship, installed apps, site status, and config preview
* belongs to one `3plug Bench`
* may use one approved `3plug Stack`

Suggested first fields:

* `bench`
* `site_name`
* `status`
* `domain`
* `installed_apps`
* `stack`
* `admin_user`
* `database_name`
* `config_summary`
* `last_backup_on`

### `3plug Job`

Reference from Press:

* `Agent Job`
* `Agent Job Step`

3plug adaptation:

* records queued, running, completed, and failed platform actions
* links actions back to server, bench, and site context

Suggested first fields:

* `job_type`
* `status`
* `server`
* `bench`
* `site`
* `requested_by`
* `queued_on`
* `started_on`
* `finished_on`
* `output_summary`
* `error_summary`

### `3plug App Source`

Reference from Press:

* `App Source`
* `App Release`

3plug adaptation:

* stores approved Triotek-controlled sources and allowed branches
* acts as the approved source registry for stacks and installs

Suggested first fields:

* `app_name`
* `repo_url`
* `default_branch`
* `allowed_branches`
* `status`
* `is_required`
* `notes`

### `3plug Stack`

Reference from Press:

* app grouping and deploy-candidate thinking

3plug adaptation:

* stores approved app stacks for bench/site creation
* groups approved app sources into installable combinations

Suggested first fields:

* `stack_name`
* `status`
* `apps`
* `default_frappe_branch`
* `description`
* `is_default`

## First ownership model

The initial 3plug record tree should be:

* `3plug Server`
* `3plug Bench` belongs to `3plug Server`
* `3plug Site` belongs to `3plug Bench`
* `3plug Job` may point to `3plug Server`, `3plug Bench`, and `3plug Site`
* `3plug Stack` references approved `3plug App Source` records

## First job-to-record mapping

### Register Server

Creates or updates:

* `3plug Server`
* `3plug Job`

### Register Bench

Creates or updates:

* `3plug Bench`
* `3plug Job`

### Create Site

Creates or updates:

* `3plug Site`
* `3plug Job`

### Install App on Site

Creates or updates:

* `3plug Site`
* `3plug Job`

## Design rule

When a Bench-owned action runs, 3plug should record the intent and execution in `3plug Job`, then use the Bench layer for the actual operation.
