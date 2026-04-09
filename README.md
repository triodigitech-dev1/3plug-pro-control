# 3plug Control

3plug Control is Triotek's Press-based control plane.

The direction is not to rebuild Press behavior from scratch beside Press.

The direction is:

* use Press as the base
* adapt it into Triotek's 3plug product
* narrow the first operating model to one managed server
* keep one 3plug deployment per managed server for clearer security isolation
* keep Bench-first lifecycle management as the first product scope
* define the product clearly before copying or reshaping large parts of Press

## Base reference

Local base reference:

* `../frappe-press`

Important reference areas:

* `../frappe-press/press`
* `../frappe-press/dashboard`
* `../frappe-press/press/agent.py`
* `../frappe-press/press/press/doctype`

## What 3plug v1 is

The first real 3plug release should be a Press-style operator platform for one managed server.

It should let Triotek:

* register and inspect the managed server
* register and inspect multiple benches on that server
* create and inspect multiple sites on those benches
* manage approved app sources and installable stacks
* run actions through recorded jobs instead of shell-only foreground execution

## First product adaptation

Press is broader and more cloud-heavy.

3plug Control should start with:

* one 3plug deployment managing one server
* many benches on that server
* many sites on those benches
* Triotek-controlled app sources and stacks

## Workspace shape

This repo now mirrors the broad Press split:

* `app/` for backend/Frappe-app adaptation notes and starting points
* `dashboard/` for operator UI adaptation notes and starting points
* `agent/` for runner/agent adaptation notes and starting points
* `docs/` for the 3plug-specific Press adaptation plan
* `src/threeplugpro_control/` for lightweight Python package scaffolding as implementation begins

## What comes next

1. lock the keep/defer map for Press doctypes and dashboard areas
2. define the first 3plug doctypes from the Press model
3. define the first dashboard pages from the Press dashboard model
4. define the first agent/job flows for single-server Bench operations
5. copy or port only the Press slices needed for that first scope

See:

* `docs/V1_PRODUCT.md`
* `docs/SINGLE_SERVER_ADAPTATION.md`
* `docs/COPY_FROM_PRESS_PLAN.md`
* `docs/PRESS_STUDY.md`
* `docs/PRESS_KEEP_DEFER_MAP.md`
* `docs/BACKEND_IMPLEMENTATION_MAP.md`
