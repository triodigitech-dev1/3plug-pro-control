# 3plug Control

3plug Control is Triotek's Press-derived control plane for Frappe operations.

It is no longer being shaped as a broad multi-server cloud product first.

The current v1 direction is:

* one 3plug deployment per managed server
* one managed Linux server in that deployment
* many benches on that server
* many sites on those benches
* jobs, plays, and forensic records for traceability

This repo uses Press as the base and is being adapted into the operator product Triotek actually wants to run.

## What 3plug is for

The current product spine is:

* register a managed Linux server
* verify and set up the self-hosted server through the real Press flow
* onboard an existing bench from that server
* discover apps and sites from the real bench
* create the managed bench record
* import managed site records
* review jobs, plays, and forensic signals from the dashboard

This is not the old coordination-repo CLI path anymore.

This is also not a billing-first control plane anymore.

Business billing and payment collection belong in the separate admin/business site, not here.

## Current scope

In scope for v1:

* managed server registration
* bench onboarding
* managed site import
* job and play visibility
* forensic logging and incident signals
* operator-first dashboard workflows

Deferred from Press for v1:

* broad multi-server cloud orchestration
* commercial billing and subscriptions
* partner and marketplace breadth
* wider infrastructure-role expansion that does not help the first server -> bench -> site path

See:

* [V1 product scope](./triotek/planning/docs/V1_PRODUCT.md)
* [Single-server adaptation](./triotek/planning/docs/SINGLE_SERVER_ADAPTATION.md)
* [Cleanup and transition log](./triotek/planning/docs/CLEANUP_ACTIVITY_LOG.md)

## Actual Linux server setup

This is the updated setup path for testing on real Linux infrastructure.

### 1. Prepare the 3plug control plane

Before onboarding a target server, make sure the control plane itself is ready:

* this repo is deployed and reachable
* the dashboard is accessible
* your operator team has self-hosted server access enabled
* a default SSH key exists in the control plane, because the managed-server flow copies and uses that key for verification

The current managed registration page uses:

* a self-hosted server plan from `press.api.selfhosted.options_for_new`
* the default SSH public key from the same endpoint

### 2. Prepare the target Linux environment

The current managed-server flow expects Linux hosts that 3plug can reach over SSH and verify with Ansible.

Current baseline assumptions from the product:

* SSH access from 3plug to the target host or hosts
* the default 3plug SSH key is installed for the verification user
* private IP values supplied in the form must actually belong to the target machines
* minimum baseline remains 4 GB RAM, 2 vCPU, and 40+ GB storage
* Docker is part of the environment baseline and is not currently treated as a special blocker

The current registration flow asks for:

* application public IP
* application private IP
* database public IP
* database private IP

If your first live setup uses a single Linux box for both application and database duties, use the matching app and db IP values for that box. This is an inference from the current registration flow and should be the simplest first test.

### 3. Register the managed server in 3plug

Use the dashboard flow:

* open `Servers`
* choose `Register Managed Server`
* enter the server title and IP details
* copy the displayed SSH key if you still need to place it on the target host
* submit the registration

What happens next:

* 3plug creates the self-hosted server record
* 3plug verifies both application and database endpoints
* 3plug starts the managed server setup flow
* the next operator visibility is on the server plays and jobs

Relevant product files:

* [RegisterManagedServer.vue](./dashboard/src/pages/RegisterManagedServer.vue)
* [selfhosted.py](./press/api/selfhosted.py)

### 4. Onboard the existing bench

After the server is registered:

* open the managed server
* open the `Bench Onboarding` tab
* enable existing bench import if the bench already exists on the Linux server
* save the real bench path
* run bench discovery
* create the managed bench
* create managed sites
* run file restore if needed

The onboarding page now exposes:

* stage-by-stage onboarding progress
* recent jobs
* recent plays
* execution status for discovery, managed bench creation, managed site import, and file restore

Relevant product files:

* [ServerBenchOnboarding.vue](./dashboard/src/components/server/ServerBenchOnboarding.vue)
* [selfhosted.py](./press/api/selfhosted.py)

### 5. Validate the first live test

For the first real server test, keep it narrow:

1. register one managed server
2. discover one real bench
3. create one managed bench
4. import one or more managed sites
5. confirm jobs and plays are visible
6. confirm forensic events and signals are being captured

This is the quickest route to useful feedback.

## Local verification

For local dashboard verification in this repo:

```powershell
$env:LOCAL_VERIFY_BUILD='1'
& 'C:\Program Files\nodejs\npm.cmd' install --legacy-peer-deps
& 'C:\Program Files\nodejs\npm.cmd' run build
```

The verification build uses the guarded local mode added in `dashboard/vite.config.ts`.

Backend syntax checks used during current product work:

```powershell
python -m py_compile press\api\selfhosted.py
python -m py_compile press\press\doctype\team\team.py
```

## MVP status

3plug Control is now past the cleanup-only stage.

Current live-testable product areas:

* managed server registration
* managed bench onboarding
* managed site import
* jobs and plays visibility
* forensic event capture
* forensic incident signals
* home control-center summaries

Still worth treating as active MVP work during live testing:

* validating the first real Linux happy path end to end
* catching leftover Press assumptions that do not fit the one-server model
* tightening unclear status messages or missing next actions based on real operator feedback

## Development note

This repo still contains broader Press code because 3plug is being built from Press, not from a blank slate.

That does not mean all Press features are part of the 3plug product.

When in doubt, follow the single-server operator model described in the planning docs and recent cleanup log.
