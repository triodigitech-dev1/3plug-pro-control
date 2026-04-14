# 3plug Control

3plug Control is Triotek's operator control panel for managing a single Linux server that hosts Frappe benches and sites.

It is built from Press, but this version is not trying to be the full Press product.

The current product shape is narrower and more practical:

* one 3plug deployment per managed server
* one Linux server managed by that deployment
* many benches on that server
* many sites on those benches
* jobs, plays, and forensic records for traceability

## What This Product Is

3plug Control is a backend-plus-dashboard product for real operations.

It uses:

* a Frappe backend for records, permissions, and APIs
* a dashboard as the main operator surface
* jobs and plays for real execution
* forensic events and signals for failure visibility

This means the product is not just a set of shell scripts or an external coordination repo.

The operator is supposed to work inside the control panel.

## What It Is Supposed To Do

In its current intended workflow, 3plug Control should let an operator:

* register a managed Linux server
* verify and set up that server through the self-hosted Press flow
* onboard an existing bench from that server
* discover the apps and sites on that bench
* create the managed bench record
* create managed site records
* follow jobs, plays, and forensic signals from the dashboard

The main operator surface visible in the code today is:

* a home summary for servers, benches, sites, jobs, and forensic signals
* a managed server registration flow
* a bench onboarding flow for existing benches
* server, bench, site, job, and forensics views

## What It Is Not

This product is not the old broad Press story in full.

For this version, it is specifically not trying to lead with:

* multi-server cloud orchestration
* billing-first workflows
* marketplace breadth
* broad partner programs
* infrastructure features that do not help the first server to bench to site path

Business billing and payment collection are not the center of this version of the product.

The center is operator control of one managed server and the benches and sites on it.

## Core Operating Model

The current v1 operating model is:

1. install 3plug Control on the real server
2. open the control panel site
3. register the managed server
4. let 3plug verify and prepare the server
5. onboard the real bench that already exists on that server
6. discover and import the real sites
7. operate through tracked jobs, plays, and forensic signals

This keeps Bench as the execution layer for Bench-owned work, while keeping records, visibility, and permissions inside the control plane.

## Why This Book Exists

This `book` folder is meant to explain the real product behavior of 3plug Control as it exists now.

The goal is to document:

* the actual workflow the operator should follow
* what the key screens and records mean
* what the product does today
* what is still incomplete, rough, or deferred

## What Comes Next

The next pages in this book should explain:

1. the first operator workflow from login to managed server registration
2. the bench onboarding workflow
3. how sites, jobs, plays, and forensic signals fit together
4. the current MVP boundaries and known gaps

Start with:

* [Product Target State](./product-target-state.md)
* [Product Shell And Features](./product-shell-and-features.md)
