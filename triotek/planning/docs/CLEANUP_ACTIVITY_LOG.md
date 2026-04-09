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

### 2026-04-08

Change:

* removed deferred billing and partner permission controls from the role-permissions UI
* renamed marketplace permission wording to a more neutral `Apps`
* left the underlying backend role fields intact for now

Reason:

* this is a safe permissions-surface cleanup pass
* it reduces operator exposure to deferred Press product concepts without forcing a backend role-schema cut yet

Commit:

* `ba517b4` `Trim deferred role permission UI`

### 2026-04-08

Decision noted:

* Docker is not currently a special blocker on the target server
* forensic reporting and logging should be the first implementation task after cleanup

Reason:

* environment attention should stay on actual current risks
* 3plug needs strong traceability once cleanup is complete

### 2026-04-08

Change:

* neutralized deferred billing and partner session-permission helpers in the dashboard session store
* removed the now-unreferenced partner profile settings component

Reason:

* this trims more deferred runtime surface without forcing a deeper partner-module deletion pass yet
* the partner settings card had already been detached from the live profile page, so removing the orphaned component was low risk

### 2026-04-08

Change:

* replaced the root billing, partner, and partner-admin dashboard pages with simple deferred notices
* removed their old tab-shell logic while keeping the route tree intact

Reason:

* this trims more imported Press UI logic from reachable route roots without forcing immediate deletion of deeper child pages
* it keeps cleanup low risk while making the deferred scope more obvious inside the codebase

### 2026-04-08

Change:

* repointed deferred billing, partnership, and partner-admin child routes to their already-neutralized root pages
* kept the original deferred route names intact while removing many deep child-page imports from the live router

Reason:

* this reduces more imported Press surface without risking named-route breakage in existing code
* it keeps the route tree stable while trimming deferred dashboard dependencies one layer deeper

### 2026-04-08

Change:

* deleted the first batch of deferred billing and partner page/component files that are no longer imported by the live router
* kept shared lower-level billing and partner support code in place for later passes

Reason:

* this is the first actual deferred dashboard file-removal pass after route isolation
* limiting deletion to now-unreferenced route-endpoint files keeps the cleanup aggressive enough to matter but still controlled

### 2026-04-08

Change:

* collapsed the remaining deferred partner payout and lead-detail routes to the partner root notice
* deleted the now-unused deferred billing pages and the first orphaned billing and partner lead-detail components

Reason:

* this removes another layer of imported Press surface after confirming the live router no longer needs those files
* it keeps the cleanup incremental by deleting only files that became orphaned after route reduction

### 2026-04-08

Change:

* removed old invoice-settlement and prepaid-credit behavior from the profile settings flow
* repointed remaining live billing prompts in alerts, onboarding, and server setup toward the kept settings path

Reason:

* this trims the last obvious user-facing billing-product behavior without deleting shared billing-detail forms that some kept flows still rely on
* it aligns the visible dashboard language with the current 3plug v1 scope

### 2026-04-08

Change:

* deleted another orphaned batch of deferred billing support dialogs and M-Pesa helper components
* kept the shared settings and plan-management billing forms that still have live imports

Reason:

* these files were no longer imported by reachable dashboard flows after the route and prompt cleanup passes
* this reduces more Press-specific payment surface while preserving the smaller set still needed for kept account-detail flows

### 2026-04-08

Decision correction:

* M-Pesa remains in 3plug scope and should not be trimmed as part of the generic billing cleanup
* restored the deleted M-Pesa helper components for setup, gateway configuration, and partner payout flows

Reason:

* the product decision is to keep M-Pesa support
* cleanup should continue to target generic deferred Press billing surfaces without removing the regional payment path we still want

### 2026-04-08

Change:

* added a payment scope map to separate kept M-Pesa and account-detail code from deferred generic Press billing code
* collapsed deferred checkout and subscription routes to the generic deferred billing page

Reason:

* payment cleanup now needs a clearer boundary than the earlier broad billing bucket
* checkout and subscription are still generic deferred Press product flows and should not keep shaping 3plug v1

### 2026-04-08

Decision correction:

* payments are no longer in scope for `3plug-control`, including M-Pesa
* payment capability now belongs in the separate admin or business site instead
* the old Press-derived payment model is now documented for handoff rather than kept live in the control plane

Reason:

* 3plug v1 is an infrastructure control plane, not the place where customer money movement should live
* documenting the old flow first lets the admin site adopt the useful parts without keeping the control plane tied to Press billing

### 2026-04-08

Change:

* added `PAYMENT_HANDOFF_TO_ADMIN_SITE.md` to document the current Press-derived payment architecture and what should move to the admin site
* updated `PAYMENT_SCOPE_MAP.md` to reflect full payment removal from `3plug-control`
* removed remaining live payment gating from home, install-app, list, onboarding, plan-change, and server-creation flows
* deleted the now-orphaned payment dialogs, alerts, Stripe, Razorpay, prepaid-credit, and M-Pesa dashboard components

Reason:

* this completes the UI-level separation between infrastructure control and business billing
* the control plane can now keep moving toward operations and forensic work without carrying payment-product assumptions

### 2026-04-08

Change:

* removed payment-state blocking from core site and server plan-change validation
* kept the deeper subscription engine untouched for now

Reason:

* this shifts plan changes toward operational control instead of checkout-style gating
* keeping the subscription engine for a later pass reduces the risk of breaking unrelated lifecycle behavior

### 2026-04-08

Change:

* neutralized site and server `update_subscription` sync paths so routine updates no longer maintain Press commercial subscription state
* kept the simpler plan-change history helpers for now

Reason:

* these update-time subscription writes are commercial bookkeeping rather than core server or site operations
* removing them reduces backend payment churn without forcing a deeper subscription-model rewrite in the same pass

### 2026-04-08

Change:

* removed payment-based `Team` gating for site creation and paid-app eligibility
* changed onboarding and login-route completion rules so they no longer depend on payment mode

Reason:

* the control plane should not treat billing setup as the condition for basic operational access
* this moves `Team` behavior closer to 3plug's ops-first model while leaving the deeper billing engine for a later focused pass

### 2026-04-08

Change:

* removed payment and budget payload fields from `Team.get_doc` so dashboard sessions no longer receive billing-specific team data
* removed `billing_info` from the account bootstrap payload and forced the exposed `billing` permission flag to `false`
* deleted orphaned dashboard components that only served card, invoice, and budget-alert payment flows

Reason:

* these payloads and components were no longer part of live 3plug-control flows after the earlier payment cleanup
* trimming them now reduces hidden coupling before we move into the forensic layer

### 2026-04-08

Change:

* disabled billing-scoped API actions at the role-guard layer, with `validate_gst` left available for address validation
* changed the remaining account and SaaS billing entry points to throw a handoff message that points payment work to the admin business site

Reason:

* this closes the public control-plane payment entry surface without forcing a risky invoice-doctype rewrite in the same pass
* it keeps the cleanup careful while making the product boundary much clearer

### 2026-04-09

Change:

* removed stale payment permission and doctype hook declarations from `hooks.py`
* removed the leftover `allow_billing` role field from `Press Role` metadata, Python types, account permission reads, and role patch logic
* removed clearly payment-only patch entries from `patches.txt` so new migrations stop advertising billing-era cleanup work

Reason:

* these were legacy declarations after the earlier payment shutdown passes and were now adding confusion rather than value
* cleaning the model and patch metadata makes the control-plane boundary clearer before we move on to the forensic layer

### 2026-04-09

Change:

* removed payment doctypes from the client API allowlist in `press/api/client.py`
* removed `Subscription` and `Invoice` shortcuts from the Press workspace and relabeled that section to `Plans`
* updated the remaining account onboarding copy so it no longer points operators toward platform invoicing

Reason:

* these were still exposing payment-era objects and messages after the earlier cleanup passes
* trimming the visible client surface makes the control-plane boundary much more consistent

### 2026-04-09

Change:

* collapsed the extra billing route tree in the dashboard so checkout and subscription paths now redirect to the generic deferred billing page
* removed the hidden billing nav item and stripped the leftover `Billing` communication type
* removed the marketplace app `Subscriptions` tab that still depended on the `Subscription` doctype

Reason:

* these were some of the last operator-facing payment references still hanging around in the dashboard shell
* reducing them now keeps the UI aligned with the infrastructure-only 3plug-control scope

### 2026-04-09

Change:

* removed `Payout Order` from the client API allowlist
* deleted the orphaned `PayoutTable.vue` component
* changed marketplace plan copy from `Subscription Price` to `Plan Price`

Reason:

* these were lingering marketplace payout and payment-era terms after the broader cleanup
* this makes the remaining operator-facing surface more consistent before we declare the payment cleanup substantially complete

### 2026-04-09

Change:

* added a first forensic-layer slice with a new `Forensic Event` doctype
* wired automatic forensic capture from `Agent Job`, `Site Activity`, and `Server Activity`
* exposed `Forensic Event` in the client allowlist and Press workspace so the logs are inspectable

Reason:

* this turns the post-cleanup plan into real product behavior instead of more planning-only work
* it gives 3plug-control an initial searchable evidence trail for operator and system actions

### 2026-04-09

Change:

* added a second forensic-layer slice in the dashboard with a dedicated `Forensic Event` object, detail route, sidebar entry, and reusable forensic list helpers
* added contextual forensic tabs to `Site`, `Server`, and `Bench` detail pages so investigations can start from the affected infrastructure record
* added a forensic CSV export helper in the doctype backend for incident review and reporting

Reason:

* the first slice captured evidence, but operators still needed a practical way to browse and export it
* this makes forensic records usable in the normal 3plug workflow instead of leaving them as backend-only artifacts

### 2026-04-09

Change:

* expanded forensic capture to include `Press Job`, `Press Job Step`, and `Security Update Check` lifecycle updates
* extended the forensic dashboard filters so operators can isolate these higher-level orchestration and readiness events

Reason:

* the first two slices covered agent jobs and activity logs well, but higher-level failure summaries were still underrepresented
* adding these sources makes investigations more useful for bench and server operations without introducing noisy low-level capture

### 2026-04-09

Change:

* added direct navigation from forensic records back to related sites, benches, servers, and contextual job pages
* updated the forensic detail view to surface linked primary targets, source records, and operational context
* hardened shared list rendering so rows only become clickable when a valid link actually exists

Reason:

* investigations should move directly from evidence to the affected infrastructure record instead of forcing operators to search manually
* this makes the forensic layer feel like an investigation hub rather than a passive event archive

### 2026-04-09

Change:

* added grouped forensic incident signals on top of `Forensic Event` so repeated failures are summarized by target and event type
* added a dedicated `Incident Signals` dashboard page, route, and sidebar entry for operator review
* linked the raw forensic event list to the new signal view so operators can move between grouped signals and the underlying event stream

Reason:

* raw events are useful for evidence, but operators also need a quicker way to spot repeated failures without rebuilding the full old Press incident subsystem
* this keeps 3plug focused on single-server operational value instead of spending more time on low-value leftover surfaces

### 2026-04-09

Change:

* turned the home dashboard into a 3plug control center instead of a thin generic Press landing page
* expanded `Team.get_home_data` to return server, bench, site, job, and forensic signal summaries for the current operator team
* made the control center show the main operator spine together in one place: managed server, benches, sites, active jobs, and open forensic signals

Reason:

* the actual product is not “cleaned Press” by itself; it needs an operator-facing surface that reflects the single-server 3plug model
* this starts turning the imported Press base into the real 3plug product instead of spending more cycles on lower-value leftover areas

### 2026-04-09

Change:

* added a dedicated `Register Managed Server` dashboard page for the self-hosted one-server 3plug flow
* wired home and quick-create entry points toward that focused registration path instead of only the older broad Press server-creation page
* kept the flow grounded on the existing self-hosted Press API so server verification, record creation, and setup still use real product behavior

Reason:

* 3plug v1 needs an explicit one-server onboarding path, not just a cleaned dashboard shell around the old cloud-era `New Server` page
* this makes the main product entry point match the actual deployment model we decided to build

### 2026-04-09

Change:

* switched the main server list CTA and empty-state banner to `Register Managed Server`
* updated sidebar server-route highlighting to include the new managed registration flow
* tightened home quick-create wording from `Benches` to `Bench` so the operator actions read as concrete next steps

Reason:

* the product should keep steering operators into the single-server 3plug flow we chose, instead of drifting back toward the older generic Press server-creation path

### 2026-04-09

Change:

* added managed bench onboarding APIs on top of the existing self-hosted Press flow
* added a `Bench Onboarding` server-detail tab for self-hosted servers so operators can configure an existing bench path, run discovery, and create the managed bench record from the dashboard
* reset self-hosted bench discovery child tables before re-running import so repeated discovery reflects current server state instead of duplicating rows

Reason:

* 3plug needs the real server -> bench path working in the product UI, not just as Desk-only self-hosted actions
* this keeps us building directly on Press's existing self-hosted behavior while making the operator flow usable inside the actual 3plug control plane

### 2026-04-09

Change:

* extended managed bench onboarding with site import and file-restore actions on top of the existing self-hosted Press flow
* added recent Ansible play visibility directly to the bench onboarding page so operators can track the run history behind discovery and restoration without leaving the flow

Reason:

* the real product path is server -> bench -> site -> jobs/plays, so the bench onboarding surface needed to continue into site onboarding instead of stopping halfway
