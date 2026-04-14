# Product Shell And Features

This page defines the target product shell and feature set for 3plug Control.

It answers a simple question:

What should the product actually contain once it feels like a real 3plug app instead of a cleaned Press fork?

## Product Shell

3plug Control should use a real Frappe v16-style app shell.

That means:

* a proper app icon
* a Desk entry
* the standard Frappe Desk shell pattern
* sidebar-driven navigation
* workspaces or module entry points that feel like a normal Frappe product

The goal is to move away from a Press-shaped dashboard shell and toward a 3plug product that lives naturally inside the current Frappe experience.

## Target Feature Set

The target state should include these top-level product areas:

* Desk
* Servers
* Benches
* Sites
* Tenants
* Apps
* Analytics
* Jobs
* Forensics / Incident Signals
* Team
* Settings

## What Each Area Means

### Desk

The default operator shell for 3plug.

It should provide:

* the app launcher presence for 3plug
* the main sidebar and workspace entry points
* a clear starting place for day-to-day operations

### Servers

This is the managed-server layer for 3plug.

In the current product direction, this should focus on:

* the one managed Linux server for the deployment
* its registration and verification flow
* its operational state
* its relationship to benches, jobs, and forensics

This should not drift back into the old broad Press infrastructure story.

### Benches

This is the runtime layer behind the sites.

It should cover:

* bench inventory
* bench onboarding
* bench detail
* bench actions that 3plug is meant to manage

### Sites

This is the main managed application layer.

It should cover:

* site inventory
* site detail
* site onboarding and creation flows
* site operations that belong in the control plane

### Tenants

This is the business or ownership layer above sites where needed.

It should eventually help answer:

* who owns which sites
* how sites are grouped commercially or operationally
* what operator context belongs to a tenant instead of to a raw site

### Apps

This is the application-management layer.

It should cover:

* apps discovered on benches
* apps allowed or approved for use
* app metadata and internal catalog behavior
* the app-facing parts of the control model

### Analytics

This is the operational reporting layer.

It should combine useful visibility across:

* server state
* bench state
* site state
* execution activity
* operator-facing health signals

### Jobs

This is a core feature, not a side panel.

3plug should track real work through jobs so operators can see:

* what ran
* what is running
* what failed
* what object the work belongs to

### Forensics / Incident Signals

This is also a core feature.

3plug should make investigations possible through:

* forensic event history
* incident signals
* links from servers, benches, sites, and jobs into the investigation trail

### Team

This is the operator and access layer.

It should cover:

* team context
* operators
* roles
* permissions
* collaboration around the managed environment

### Settings

This is the configuration layer for the product.

It should include:

* organization-level settings
* product-level settings
* operator or team-level configuration that belongs outside raw runtime views

## Core Product Principle

Jobs and forensics are not optional extras.

They are part of the defining promise of 3plug because this product is supposed to give operators real traceability across server, bench, and site actions.

## Immediate Build Meaning

When we review or build product surfaces next, we should test them against this question:

Does this page, module, or flow clearly belong to one of the target product areas above?

If not, then it is probably:

* inherited Press surface we should retire
* old naming we should replace
* deferred functionality we should hide
* missing 3plug functionality we should build correctly
