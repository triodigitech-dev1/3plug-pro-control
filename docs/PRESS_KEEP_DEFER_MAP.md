# Press Keep/Defer Map

## Purpose

Turn the Press study into a concrete implementation filter for 3plug v1.

Reference base:

* `../frappe-press/press/press/doctype`
* `../frappe-press/dashboard/src`

## Keep first: backend doctypes

These areas directly support the one-server 3plug operator model and should guide the first implementation.

### Core inventory and runtime

Keep first:

* `Server`
* `Bench`
* `Site`
* `App Source`
* `Agent Job`
* `Agent Job Step`
* `Site App`
* `Site Domain`
* `Bench App`
* `Common Site Config`

Why:

* they map directly to the first 3plug objects and actions
* they support server to bench to site visibility
* they support app governance and tracked execution

### First supporting relations

Keep first or study closely for direct reuse:

* `Bench Dependency`
* `Bench Variable`
* `Site Config`
* `Site Migration`
* `Site Backup`
* `Server Activity`

Why:

* these support realistic bench and site operations
* they are likely useful soon after the first create and install flows

## Defer: backend doctypes

These belong to the broader Press cloud model and should wait unless a real v1 need appears.

### Multi-server and infrastructure-role expansion

Defer:

* `Database Server`
* `Proxy Server`
* `Registry Server`
* `Log Server`
* `Trace Server`
* `Monitor Server`
* `Code Server`
* `NFS Server`
* `NAT Server`
* `Cluster`
* `Managed Database Service`

Reason:

* these support Press's broader many-role, many-machine platform model
* 3plug v1 should start with one deployment managing one server

### Deploy and release orchestration breadth

Defer:

* `Deploy`
* `Deploy Bench`
* `Deploy Candidate`
* `Deploy Candidate App`
* `Deploy Candidate Build`
* `Release Group Server`
* `Bench Update`
* `Bench Update App`
* `Site Update`

Reason:

* these are important later, but they are not required to start the first server, bench, site, and job slice

### Commercial and customer-platform layers

Defer:

* `Team`
* `Plan`
* `Plan Change`
* billing doctypes
* marketplace doctypes
* partner doctypes
* subscription and payout doctypes

Reason:

* 3plug v1 is an operator platform first, not a commercial cloud product first

## Keep first: dashboard areas

These dashboard areas match the first 3plug operator surface.

### Direct keep

Keep first:

* list/detail patterns from `ListPage.vue` and `DetailPage.vue`
* job visibility from `JobPage.vue`
* site flows from `NewSite.vue`, `NewSiteProgress.vue`, `InstallApp.vue`
* server setup ideas from `NewServer.vue`

Why:

* they align closely with the first write flows and read views

### Reuse as shell and navigation patterns

Keep first or study for reuse:

* page routing from `router.js`
* application shell from `App.vue` and `main.js`
* shared UI patterns in `components/`, `dialogs/`, `controllers/`, and `objects/`

Why:

* 3plug should feel like a Press-derived dashboard, not an unrelated UI

## Defer: dashboard areas

These parts should wait until the one-server operator slice is working.

### Commercial and account flows

Defer:

* billing pages
* checkout pages
* subscription pages
* payout pages
* partner pages

### Marketplace and broader product flows

Defer:

* marketplace-oriented flows
* signup and self-service onboarding flows
* account setup and customer growth flows

### Broader deployment flows

Defer for now:

* release-group and broad deploy candidate flows
* cloud-scale server enablement flows

## Working decision

For 3plug v1:

* keep Press's backend, dashboard, and job architecture
* keep the server, bench, site, app-source, and job spine
* defer the wider many-server cloud and commercial layers
* treat one 3plug deployment as the control plane for one managed server
