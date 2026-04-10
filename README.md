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
* [Control-panel runbook](./docs/3plug-control-runbook.md)

## Same-server control panel setup

This is the actual deployment shape we are aiming for first:

* one Linux server
* one Frappe bench on that server
* one 3plug control-panel site on that same server
* that site is the real 3plug product you will use

So you are not installing a separate Press and then a separate 3plug.

You are using this repo as your Press-derived product and installing its `press` app into the bench that will host the real 3plug control panel.

If you want the step-by-step operator checklist version of this setup, use:

* [3plug Control Runbook](./docs/3plug-control-runbook.md)

### 1. Prepare the Linux server

Start by creating a clean working directory and updating the base system.

```bash
sudo mkdir -p /opt/triotek
sudo chown -R $USER:$USER /opt/triotek
cd /opt/triotek

sudo apt update
sudo apt -y upgrade
sudo apt -y install git curl vim ufw fail2ban nginx certbot python3-certbot-nginx
```

Create the `frappe` user and switch into it before continuing:

```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
sudo chown -R frappe:frappe /opt/triotek
sudo su - frappe
cd /opt/triotek
```

### 2. Do the first server cleanup and layout

Use a clear directory layout before installing the control panel:

```bash
sudo mkdir -p /opt/triotek/control
sudo mkdir -p /opt/triotek/logs
sudo chown -R $USER:$USER /opt/triotek
```

If this server already has unrelated old test files or abandoned benches, move them out of the way before you begin so the first install is easy to reason about.

### 3. Apply basic security hardening first

Before exposing the control panel, do the basic hardening that reduces avoidable noise and brute-force risk.

#### Firewall

If the firewall is not already enabled, set it up:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

#### Fail2ban

Enable brute-force protection:

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo systemctl status fail2ban
```

You can later tune `/etc/fail2ban/jail.local`, but enabling the service early already helps.

#### SSH hygiene

Recommended first-pass SSH hygiene:

* use SSH keys, not password login, wherever possible
* avoid direct root password SSH
* confirm the SSH port you intend to use
* keep the authorized keys clean and intentional

If you want to harden SSH further, the Press base already contains hardening-oriented playbooks such as:

* `press/playbooks/harden.yml`
* `press/playbooks/fail2ban.yml`
* `press/playbooks/ufw.yml`
* `press/playbooks/roles/sshd_hardening/*`

### 4. Set up the bench that will host 3plug itself

This is the bench that will run the actual control panel.

Follow the normal Frappe Bench host prerequisites first, then create the bench. The official Bench setup reference is:

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench

Once Bench is available on the server:

```bash
cd /opt/triotek
git clone https://github.com/Triotek-Ltd/3plug-pro-control.git control
cd control
npm install --legacy-peer-deps
```

Then add the app into your Frappe bench:

```bash
cd /opt/frappe-bench
bench get-app /opt/triotek/control
bench new-site 3plug.yourdomain.com
bench --site 3plug.yourdomain.com install-app press
```

That site, `3plug.yourdomain.com`, is your actual 3plug control panel.

### 5. Run the control panel locally first

For the first boot:

```bash
cd /opt/frappe-bench
bench start
```

If you are still validating the app, keep it in foreground/dev mode first so you can see what breaks quickly.

### 6. Put HTTPS in front so the browser does not warn

Use a real domain that points to the server first, then issue a certificate.

Basic Nginx + Certbot path:

```bash
sudo certbot --nginx -d 3plug.yourdomain.com
```

After that, test renewal:

```bash
sudo certbot renew --dry-run
```

This is the simplest way to avoid the browser showing a dangerous-site warning.

The Press base also has TLS-related machinery and certificate records, but for the first live control-panel setup, a straightforward valid public certificate is the right starting point.

### 7. Log into the real 3plug control panel

After the site is up:

* open `https://3plug.yourdomain.com`
* log in as the site administrator
* make sure the operator team has self-hosted server access enabled
* confirm a default SSH key exists, because the managed-server registration flow exposes and uses it

The managed registration page pulls:

* a self-hosted server plan from `press.api.selfhosted.options_for_new`
* the default SSH public key from that same endpoint

### 8. Register the server inside 3plug

If you are testing the same server that hosts the control panel, start with that same machine as the first managed server.

Use:

* `Servers`
* `Register Managed Server`

Current form inputs:

* server title
* application public IP
* application private IP
* database public IP
* database private IP

For the first same-server test, if the same Linux machine is serving both app and db roles, use the matching app and db IPs for that same box.

What happens next:

* 3plug creates the self-hosted server record
* 3plug verifies reachability and minimum specs
* 3plug starts the setup flow
* plays and jobs become visible from the server pages

Relevant product files:

* [RegisterManagedServer.vue](./dashboard/src/pages/RegisterManagedServer.vue)
* [selfhosted.py](./press/api/selfhosted.py)

### 9. Onboard the existing bench

After the server is registered:

* open the managed server
* open the `Bench Onboarding` tab
* enable existing bench import if the bench already exists on the Linux server
* save the real bench path such as `/home/frappe/frappe-bench`
* run bench discovery
* create the managed bench
* create managed sites
* run file restore if needed

The onboarding page now shows:

* stage-by-stage onboarding progress
* recent jobs
* recent plays
* execution status for discovery, managed bench creation, managed site import, and file restore

Relevant product files:

* [ServerBenchOnboarding.vue](./dashboard/src/components/server/ServerBenchOnboarding.vue)
* [selfhosted.py](./press/api/selfhosted.py)

## Control panel workflow after setup

This is the current practical guidebook flow for using 3plug after the control panel is live.

### First-use workflow

1. bring up the control-panel site
2. confirm login works over HTTPS
3. confirm firewall and fail2ban are active on the host
4. confirm the default SSH key is available in the control panel
5. register the first managed server
6. onboard the existing bench
7. import managed sites
8. confirm plays, jobs, and forensic events are visible

### Normal operator workflow

After setup, 3plug is meant to be used like this:

1. open the home control center and review server, bench, site, job, and forensic summaries
2. open the managed server to inspect readiness and recent plays
3. use bench onboarding when adopting or re-syncing the real bench state
4. inspect benches and sites from the normal detail pages
5. watch jobs when actions are running
6. use forensic events and forensic signals when something fails repeatedly

### First live test workflow

For the first real test on a live server, keep it narrow:

1. register one managed server
2. discover one real bench
3. create one managed bench
4. import one or more managed sites
5. confirm jobs and plays are visible
6. confirm forensic events and signals are being captured
7. note every unclear status, broken assumption, or missing next action

This is the fastest route to actionable feedback.

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
