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

### 2026-04-09

Change:

* added home-dashboard onboarding state so operators can see the current managed server -> bench -> site stage without opening the server tabs first
* added home job-scope coverage totals for server jobs, bench jobs, and site jobs so the control center confirms the execution spine is being tracked across all three layers
* verified the updated dashboard with the local `LOCAL_VERIFY_BUILD=1` build path after the home control-center changes

Reason:

* the product is now close enough to real live-server testing that the home view needs to answer two operational questions directly: what step is next, and are server, bench, and site jobs actually being tracked

### 2026-04-09

Change:

* added onboarding execution summaries to the self-hosted bench state payload so discovery, managed bench creation, managed site import, and file restore now expose explicit success, running, failed, or idle state
* added recent onboarding jobs and per-scope job counts to the bench onboarding page so server, bench, and site execution can be reviewed inside the flow itself
* verified the updated onboarding flow with Python syntax checks and the local `LOCAL_VERIFY_BUILD=1` dashboard build

Reason:

* the next real value is live-server testing, and that only becomes useful when the onboarding flow tells us which step actually ran, which one failed, and where to inspect the underlying play or job

### 2026-04-13

Change:

* retired the old `/servers/new` dashboard entry point by redirecting it to `Register Managed Server`
* hid self-hosted server-detail tabs that still present the older Press app-vs-db server model, including legacy overview, analytics, bench analytics, snapshots, and generic actions
* removed self-hosted desk shortcuts that jump operators into legacy database-server records from the server detail options menu

Reason:

* the current 3plug product target is the managed-server workflow, not the broader legacy Press server-provisioning model
* the fastest way to reduce operator confusion is to stop steering people into old server surfaces before we do deeper structural cleanup

### 2026-04-13

Change:

* rebranded the Desk-facing app metadata from `Press` to `3plug Control`
* replaced the hidden `Frappe Cloud` workspace with a visible `3plug Control` workspace built around the target operator areas
* reorganized the module map into `Operations`, `Execution`, `Applications`, `Analytics`, `Team`, and `Settings`
* added Desk shortcuts for `Tenants`, `Analytics`, and `Incident Signals` using the closest existing records while the deeper product model is still being built

Reason:

* the first thing the operator should feel is the right product shell, not the old Press branding and workspace model
* this gives us a real Frappe Desk starting point for the next 3plug product cleanup and module-building work

### 2026-04-13

Change:

* added a first-pass `Tenants` module in the dashboard on top of the existing `Team` doctype
* created tenant list and detail surfaces with overview, sites, benches, and servers tabs
* added `Tenants` to the dashboard sidebar so it is now a real app module instead of only a workspace shortcut

Reason:

* `Tenants` is part of the agreed 3plug target product shape, but it previously existed only as hidden account/session plumbing
* this gives the product a real tenant-facing surface without forcing a risky backend rename before the rest of the shell cleanup is done

### 2026-04-13

Change:

* reviewed the current `Press Settings` doctype against the 3plug target state
* documented the intended `Control Settings` scope in `book/control-settings.md`
* split the settings model into:
  * keep and reframe for 3plug operations
  * review carefully before simplifying
  * hide or defer from the main product settings surface
* decided to keep `Press Settings` as the backend single doctype for now while presenting it in-product as `Control Settings`

Reason:

* the settings surface is one of the biggest places where old Press product assumptions still live
* 3plug needs a control-first settings model before we start editing the settings UI blindly
* a direct doctype rename would be risky because `Press Settings` is still referenced widely across the backend

### 2026-04-13

Change:

* relabeled the visible product settings entry points from `Settings` to `Control Settings`
* updated the dashboard sidebar label, settings-page breadcrumb, and Desk workspace shortcut to use the 3plug-facing name
* kept the underlying backend doctype linked to `Press Settings` for compatibility

Reason:

* the product shell should stop teaching operators the old Press name before the backend rename is safe
* this gives us the right operator language immediately without breaking the current settings implementation

### 2026-04-13

Change:

* reorganized the visible `Press Settings` form labels around Triotek control-plane language instead of old Press-first tab names
* reframed tabs and sections into product-facing groups such as `Commercial`, `Storage and Backups`, `Build and Delivery`, `Tenant Provisioning`, `Communications and Integrations`, `App Marketplace`, `Control Plane Operations`, `Control Flags`, `Partner Operations`, `Hybrid Runtime`, and `Security and Compliance`
* added a form-level `Control Settings` title and intro while keeping the underlying doctype and fieldnames unchanged

Reason:

* we agreed to keep billing, marketplace, and partner areas, but they should be presented as Triotek product capabilities rather than stale Press categories
* this gives operators a more intentional settings surface without risking a backend rename or migration yet

### 2026-04-13

Change:

* continued curating `Control Settings` by renaming weak infrastructure labels to clearer operator-facing names such as `Platform Identity`, `Bench Runtime Defaults`, `Runtime Scaling`, `Managed Server IP`, `Default Runtime Plan Type`, and `Protect Redis with Password`
* reframed a few legacy field labels like `Trial Site Plan`, `Usage Record Batch Size`, `GitHub Personal Access Token`, `Card Verification Policy`, and `Wazuh Endpoint`
* hid the orphan placeholder field `data_40` and the `ngrok_auth_token` field from the main operator form

Reason:

* after the tab-level relabeling, the next problem was that several individual fields still felt like stale internals rather than deliberate product controls
* this keeps the backend intact while making the visible settings form more intentional for operators

### 2026-04-13

Change:

* reshaped the `Control Settings` field order so the most important controls appear first inside the main product tabs
* prioritized commercial defaults before deeper payment and backoffice details
* moved build runtime and release controls ahead of registry and storage details
* moved GitHub/source controls to the top of the integrations tab
* moved core platform operations, monitoring, runtime defaults, and certificates ahead of lower-priority infrastructure details
* reordered feature flags so execution and incident-response controls appear before secondary signup and billing-adjacent flags

Reason:

* the settings form now had better naming, but operators still would have landed on lower-value controls before the real platform knobs
* this aligns the visible flow of the form with the actual 3plug operating model

### 2026-04-13

Change:

* deeply shaped the `Control Plane Operations` tab so it now flows through:
  * platform identity
  * bench runtime defaults
  * jobs, monitoring, and alerts
  * TLS and certificate runtime
  * SSH trust
  * network overrides
  * runtime scaling
  * agent and automation internals
* renamed the remaining vague infrastructure labels to clearer operator-facing names such as `Monitoring Server`, `Monitoring Token`, `Monitoring Service Password`, `Certificate Registration Email`, `Agent Source Owner`, `Agent GitHub Token`, `Agent Branch`, `Network Overrides`, and `Shared Runtime Directory`

Reason:

* `Control Plane Operations` is the closest thing to the product's operational backbone, so it needed to reflect the actual order in which a 3plug operator thinks and works
* this makes the tab feel intentional instead of like a mixed bag of inherited Press infrastructure fields

### 2026-04-13

Change:

* deeply shaped the `Build and Delivery` tab around the 3plug app and release workflow
* reordered the tab so operators see build runtime and release execution controls first, then release queue automation, asset storage, registry delivery, remote distribution, documentation publishing, and storage enforcement
* renamed delivery-facing fields to clearer product language such as `Release Build Server`, `Minimum Build Memory`, `Bench Provisioning Concurrency Limit`, `Use Job Callbacks`, `Enable Asset Store`, `Container Registry and Delivery`, `Remote Distribution and Links`, and `Site Storage Limits`

Reason:

* `Build and Delivery` is where 3plug should feel like a control plane for app and bench change delivery, not like a generic Docker settings page
* this aligns the tab with the real release pipeline operators care about

### 2026-04-13

Change:

* deeply shaped the `Commercial` tab so it now starts with trial, pricing, usage, and invoicing policy before payment gateway details and backoffice integrations
* kept billing, payment, and commercial integrations in the product, but reframed them with clearer Triotek-facing language such as `Default Trial Site Count`, `Usage Record Sync Batch Size`, `Pricing and Invoicing Policy`, `Primary Payment Gateway`, `Regional Payment Gateway`, `Signup Credits`, `Card Verification Charge`, `NPO Discount Percentage`, and `Autoscale Discount Percentage`

Reason:

* we agreed not to drop billing and commercial controls, but they needed to stop reading like a stale Press billing admin page
* this makes the commercial tab feel like part of the 3plug product instead of a leftover payment console

### 2026-04-13

Change:

* deeply shaped the `App Marketplace` tab around Triotek app-channel controls
* reordered the tab so storefront and channel controls lead, followed by payout policy, marketplace embedding, and analytics
* renamed marketplace-facing fields to clearer product language such as `Marketplace Channel Controls`, `Max Storefront Screenshots`, `Publisher Payout Threshold`, `Marketplace Commission Rate`, `Reference USD Rate`, `Marketplace Embed Script`, and `Marketplace Analytics`
* updated `book/control-settings.md` so billing, marketplace, and partnership settings are now documented as retained-but-reframed Triotek product areas instead of hidden/deferred areas

Reason:

* we agreed to keep marketplace and partner capabilities in the product, but they should read like deliberate Triotek channel operations rather than inherited Press marketplace residue

### 2026-04-13

Change:

* deeply shaped the `Partner Operations` tab around partner commercial policy, enablement resources, and sector integrations
* renamed the remaining partner-facing fields to clearer product language such as `Partner Commercial Policy`, `Partner Fee (USD)`, `Partner Fee (INR)`, `Partner Enablement Resources`, `Partner Resource Hub Link`, and `Education Partner Integration`
* updated the settings contract so any remaining school-specific controls are treated as partner-sector integrations rather than core product identity

Reason:

* partner settings were still reading like raw inherited program fields rather than a coherent Triotek partner operations surface
* this keeps the capability while making the product language much more intentional

### 2026-04-13

Change:

* deeply shaped the `Communications and Integrations` tab around source control hooks, outbound messaging, cloud credentials, incident messaging, and email safety services
* renamed the main sections and fields to clearer product language such as `Source Control and Release Hooks`, `Outbound Email`, `Telegram Alerts`, `Cloud Credentials`, `Incident Messaging`, `Email Safety`, `GitHub Service Token`, `Release Trigger Marker`, `Telegram Alert Channel ID`, `Cloud Access Key ID`, `Twilio Sender Number`, and `Spam Filter Endpoint`

Reason:

* this tab was still reading like a grab bag of unrelated provider settings
* the new framing makes it feel like the integration hub for the control plane instead of a leftover integrations page

### 2026-04-13

Change:

* updated the visible commercial and partner currency labels from `USD`/`INR` to `GBP`/`KSh` in the settings surface
* updated the settings contract to note that the backend still uses legacy `usd`/`inr` fieldnames and should be migrated separately later

Reason:

* the product language should reflect the intended Triotek currency presentation now, even before we take on a deeper billing data-model migration

### 2026-04-13

Change:

* added a shared currency helper in `press/utils/currency.py` so the product can use `GBP` and `KSh` behavior without renaming the legacy `*_usd` and `*_inr` storage fields yet
* updated team creation and team validation defaults so new teams now default to `KES` for Kenya and `GBP` elsewhere
* updated billing micro-charge selection, prepaid minimum validation, plan-price field lookup, invoice PDF generation, and budget-alert formatting to use the shared currency helper instead of hardcoded `USD` and `INR` checks
* updated the team currency test so it now asserts `KES` for Kenya and `GBP` for the United Kingdom

Reason:

* the settings surface already spoke in `GBP` and `KSh`, but the runtime still behaved like an old `USD` and `INR` product
* this gives the control plane a safe first backend currency pass while preserving legacy billing fields and older invoice data for the deeper migration later

### 2026-04-13

Change:

* extended the currency migration into partner flows, marketplace pricing lookups, payouts, and bootstrap defaults
* replaced fixed partner conversion math with shared currency conversion helpers
* updated marketplace plan and payout lookups to resolve against the legacy `price_usd` / `price_inr` and `net_total_usd` / `net_total_inr` fields through the shared helper layer instead of building field names directly from the live team currency
* updated the bootstrap flow so the setup wizard, starter teams, and starter plan names now reflect the Triotek `GBP` and `KES` direction while still writing into the legacy price columns

Reason:

* after the first backend currency pass, partner and marketplace paths were still a source of immediate breakage because they were building field lookups and conversions around the old `USD` and `INR` assumptions
* this keeps the product behavior aligned with the new currency direction without forcing a dangerous full schema migration in the same pass

### 2026-04-13

Change:

* added `price_gbp` / `price_kes` aliases to marketplace plan responses while keeping the legacy `price_usd` / `price_inr` keys for compatibility
* added `net_total_gbp` / `net_total_kes` and `gbp_items` / `kes_items` aliases to marketplace payout responses while preserving the older payout keys
* updated the marketplace pricing editor labels in the dashboard from `USD` / `INR` to `GBP` / `KSh`

Reason:

* after the runtime currency cleanup, the API and UI were still visibly leaking the old currency model even where the underlying values were already behaving correctly
* this starts the outward-facing payload migration without breaking the current frontend callers in one shot

### 2026-04-13

Change:

* added shared dashboard pricing helpers for live team currency, active price field, and plan amount resolution in `dashboard/src/utils/format.js`
* updated the core plan cards, site app plan selector, new-site summary, site login, site overview, and new-site app selector to use the shared helper layer instead of branching directly on `INR`

Reason:

* after the API-level cleanup, the main dashboard surfaces were still repeating the old `INR` / `USD` assumptions file by file
* this gives the core site-planning and plan-display flows a single pricing model, which is enough to close the settings-and-currency slice cleanly before we move to the next feature

### 2026-04-14

Change:

* reshaped the `Servers` feature toward the one-managed-server 3plug model
* added a dedicated managed server overview component for self-hosted server records
* simplified the server list to a single `Plan` column instead of app-plan and database-plan split labels
* removed the old database-server Desk shortcuts from the main server actions menu
* collapsed managed-server registration to one public IP and one private IP in the dashboard
* updated the self-hosted server creation API to accept the one-server input shape while still mapping it onto the legacy internal records needed by the older setup and onboarding flow

Reason:

* the product target is one 3plug deployment managing one Linux server, but the server feature was still visibly teaching the old Press split-host model
* this gives operators a cleaner managed-server experience now without forcing a high-risk backend deletion of the old internal server and database records in the same pass
## 2026-04-14 - Server operational tabs shaped for the one-managed-server model

- Added a self-hosted `Health` tab to the server detail flow so operators can see managed-server readiness, onboarding checks, and recent jobs/plays without dropping into legacy split-infra views.
- Added a self-hosted `Security` tab that frames access posture around recorded IPs, TLS identity, and the existing server firewall document instead of generic cloud-server language.
- Added a self-hosted `Operations` tab that wraps the existing server action engine for restart, cleanup, and recovery work while preserving the old server internals only as implementation detail.
- Wired these tabs into the self-hosted server detail route so the operator-facing server surface now reads as `Overview`, `Health`, `Security`, `Operations`, and `Bench Onboarding`.

## 2026-04-14 - Home reshaped into a real client-facing command center

- Reworked the main home summary away from a generic resource stack into a tighter command-center layout.
- Made the top of the page lead with one primary next action, operator scripts, and a clearer attention board instead of mixed summary blocks.
- Kept the existing home data contract, but reorganized the surface around the agreed product spine: managed server, bench onboarding, managed sites, jobs, and incident signals.
- Tightened the home page toward the product benchmark so it feels more like a real client-facing control panel and less like inherited Press scaffolding.

## 2026-04-14 - Benches reshaped toward the MVP product surface

- Added a real bench overview tab so the bench feature now starts with runtime summary, managed server context, deploy state, and next action instead of dropping straight into inherited sub-screens.
- Tightened product-facing bench language in the detail flow by renaming visible tabs and actions from generic internal wording to operator-facing bench wording such as `Bench Config`, `Bench Env`, and `Operations`.
- Updated the new bench page copy so it reads as bench creation and runtime selection instead of leftover Frappe Cloud-style wording.

## 2026-04-14 - Sites reshaped toward site management

- Added a managed site overview tab so the site feature now starts with runtime summary, bench/server context, plan state, monitoring state, and next action instead of dropping directly into the older usage-heavy overview.
- Renamed the most visible site tabs toward the product shape by making `Insights` read as `Health and Insights` and `Actions` read as `Operations`.
- Tightened a high-visibility site action label from `Visit Site` to `Open Site` so the product reads more like an operator control panel than an inherited hosting dashboard.

## 2026-04-14 - Jobs tightened toward execution tracking

- Renamed the shared jobs tab label to `Execution` so server, bench, and site detail flows present jobs as tracked product execution rather than raw background records.
- Tightened the shared job list columns from `Job Type`, `Site`, and `Created By` to `Action`, `Target`, and `Triggered By`.
- Updated the job detail page to describe the job as tracked execution in context instead of leaving it as a bare internal job record view.

## 2026-04-14 - Forensics tightened toward incident review and evidence

- Reframed the forensic event detail tab from `Overview` to `Evidence` so the product presents forensic records as incident evidence, not just generic documents.
- Tightened the incident signals page wording around operator review, repeated failure patterns, and evidence, while keeping the underlying data flow intact.
- Renamed several high-visibility labels on the forensics surfaces so they read more like an incident-review product area and less like a raw internal event stream.

## 2026-04-14 - Apps tightened toward a real product module

- Renamed the main `/apps` module from `Marketplace` to `Apps` so it reads as a core product area instead of a deferred legacy marketplace shell.
- Tightened visible tab and action labels around catalog, version support, releases, and pricing while preserving the marketplace-backed implementation under the hood.
- Updated site and bench app-management wording so app operations read more like internal runtime management and less like inherited Frappe Cloud marketplace copy.

## 2026-04-14 - Analytics wording tightened for the MVP product

- Reframed site insights navigation from `Analytics / Reports / Jobs` to `Overview / Performance / Execution` so the analytics area reads more like an operator workflow.
- Tightened several site analytics card titles toward product-facing language such as `Usage Trend`, `Request Volume`, `Request CPU Load`, and `Operational Analytics`.
- Updated the analytics card share affordance text so it reads like a deliberate dashboard feature instead of a low-level implementation detail.

## 2026-04-14 - Sidebar and workspace tightened toward the v16-style product shell

- Updated the dashboard sidebar so the main MVP modules are more visible and intentional, especially `Benches` on the real `/benches` route and `Apps` as a first-class product area.
- Reduced sidebar confusion by promoting the actual product modules and pushing secondary/internal areas lower in the shell.
- Simplified the Desk workspace content into clearer groups: `Runtime`, `Apps`, `Execution And Evidence`, and `Administration`.
- Removed duplicate or low-signal workspace shortcuts so the Desk entry surface better matches the MVP product instead of exposing a grab-bag of inherited records.
