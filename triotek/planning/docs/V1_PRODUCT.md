# 3plug v1 Product

## Goal

Build 3plug as Triotek's Press-based control plane for a single managed server.

This is not a general cloud platform in v1.

This is not a shell-command wrapper in v1.

This is an operator product that uses:

* a Frappe backend for records, permissions, and APIs
* a dashboard for inventory and actions
* a job system for real execution and traceability

## Core operating model

One managed server first:

* one 3plug deployment per managed server
* one Linux server managed by Triotek
* many benches on that server
* many sites on those benches

This is the first simplification of Press.

This also creates the first security boundary:

* one 3plug instance should manage its own server
* one 3plug instance should not become a shared control plane for many unrelated customer servers in v1

## First managed records

These are the first records 3plug should own:

* `3plug Server`
* `3plug Bench`
* `3plug Site`
* `3plug Job`
* `3plug App Source`
* `3plug Stack`

## First operator outcomes

The first release should let an operator:

* see the managed server and its readiness
* see all benches on that server
* see all sites on those benches
* register an existing bench
* create a new site on a bench
* install an approved app on a site
* track every action through a job record

## First UI surface

The first dashboard should include:

* server overview
* bench inventory
* bench detail
* site inventory
* site detail
* job activity

## First write flows

The first write flows should be:

* register server
* register bench
* create site
* install app on site

## Product rules

Rules for v1:

* use real Bench behavior where Bench is the correct execution layer
* move execution behind jobs instead of running long actions only in the foreground
* keep app installation governed by approved app sources and stacks
* do not adopt Press modules that are unrelated to the one-server v1 scope
* keep the control plane scoped to its own managed server for isolation and simpler security
* treat forensic reporting and logging as the first implementation task after cleanup

## Environment note

Current operating assumption:

* Docker is available on the target server and is not currently a special blocker to watch for

This means Docker should remain part of the environment baseline, but it is not the primary cleanup or risk focus right now.

## Explicitly out of scope for v1

These areas should not drive the first implementation:

* multi-server orchestration
* cloud provider provisioning
* billing and subscription features
* marketplace breadth beyond Triotek-approved apps
* advanced HA and distributed infrastructure features
* customer self-service beyond the operator-facing control plane
