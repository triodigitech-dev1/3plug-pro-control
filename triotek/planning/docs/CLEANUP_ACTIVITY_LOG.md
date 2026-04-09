# Cleanup Activity Log

## Purpose

Track cleanup and adaptation changes made to the imported Press base.

This log exists so that 3plug can keep a clear history of what was hidden, deferred, removed, or preserved during the transition from Press to Triotek's single-server product.

## Entries

### 2026-04-08

Change:

* imported the Press codebase into the repo root
* preserved Triotek-specific product and cleanup planning under `triotek/planning`

Reason:

* 3plug should now build from Press directly instead of from a parallel scaffold

Commit:

* `a8e50b0` `Import Press base and preserve Triotek planning`

### 2026-04-08

Change:

* documented the first safe cleanup pass
* classified imported Press modules and dashboard route groups into keep-first and defer-first areas

Reason:

* direct deletion was too risky before mapping hooks, modules, and route surfaces

Commit:

* `fa80231` `Document first safe cleanup pass`

### 2026-04-08

Change:

* hid deferred top-level sidebar navigation for marketplace, billing, and partnership
* renamed the visible dashboard product label from `Frappe Cloud` to `3plug Control`

Reason:

* this is the first low-risk UI isolation pass
* it reduces exposure of clearly out-of-scope Press surfaces without deleting files or breaking route imports

Commit:

* `9e71a93` `Hide deferred sidebar surfaces and track cleanup`

### 2026-04-08

Change:

* hid deferred partner-admin settings tab
* removed the deferred partner profile card from settings profile view
* added a first route guard that redirects deferred billing, partner, signup, checkout, subscription, and marketplace entry routes back to the main site list

Reason:

* this is the second low-risk UI isolation pass
* it reduces direct access to out-of-scope Press flows while leaving the underlying files present for later cleanup

Commit:

* `8665952` `Guard deferred routes and settings surfaces`

### 2026-04-08

Change:

* classified hook cleanup targets in `press/hooks.py`
* disabled deferred billing, marketplace, Stripe, payout, and SaaS hook wiring by exact doctype key and exact scheduler target
* kept the underlying imported modules in place

Reason:

* this is the first low-risk backend isolation pass
* it reduces active deferred backend behavior without deleting code the imported Press base may still reference indirectly

Commit:

* `17afde6` `Disable deferred backend hook wiring`

### 2026-04-08

Change:

* removed the marketplace object from the shared dashboard object registry
* stopped generating marketplace list and detail routes from the shared object route builder

Reason:

* this is a low-risk dashboard isolation step
* it reduces live marketplace route surface without deleting marketplace files or deeper imports yet

Commit:

* `b283fe3` `Reduce marketplace route generation`

### 2026-04-08

Change:

* removed the marketplace-developer prompt from profile settings
* neutralized referral and signup messaging in the profile area
* stopped legacy billing alerts from linking users into deferred billing pages

Reason:

* this is another low-risk UI surface reduction pass
* it removes operator-facing prompts that still pull users toward deferred Press product flows

Commit:

* `7121b67` `Reduce deferred profile and billing prompts`
