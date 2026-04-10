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

Create the `frappe` user, but stay on the current sudo-capable admin user until the system-level setup is done:

```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
sudo chown -R frappe:frappe /opt/triotek
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
sudo ufw allow OpenSSH
sudo ufw default deny incoming
sudo ufw default allow outgoing
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

Do the first SSH hardening pass here on the server itself:

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
```

Edit the SSH server config:

```bash
sudo nano /etc/ssh/sshd_config
```

Set or confirm these values:

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication yes
```

Important:

* keep `PasswordAuthentication yes` for now if your admin user has not yet confirmed key-based SSH access to this server
* keep your current SSH session open while testing a second session
* if you use a custom SSH port, set it here before restarting SSH

Then reload and verify:

```bash
sudo systemctl restart ssh
sudo systemctl status ssh --no-pager
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
```

After you have confirmed that your admin user can log in to the server with SSH keys, come back and change:

```text
PasswordAuthentication no
```

Then restart SSH again and verify from a second SSH session before closing the first one.

The GitHub SSH key for the `frappe` working user comes later in the git setup section. This hardening step is only for securing server access itself.

For normal first setup, the commands above are enough. The Press playbooks can stay as future operator-maintainer tooling, not something the first-time installer needs to use.

### 4. Prepare the working user for source control

Before Bench setup, get the `frappe` working user ready for git, GitHub SSH, and forks.

Switch into the working user:

```bash
sudo su - frappe
cd /opt/triotek
```

Configure git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor nano
git config --global --list
```

Create the GitHub SSH key for this working user:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "your-email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Then do these GitHub-side actions with the same account that should own later changes:

1. Open `GitHub -> Settings -> SSH and GPG keys`
2. Click `New SSH key`
3. Paste the output of `cat ~/.ssh/id_ed25519.pub`
4. Save it with a title such as `3plug-control-server`

Test SSH from the server:

```bash
ssh -T git@github.com
```

Fork these repositories into the GitHub account that should own later changes:

* `Triotek-Ltd/triotek-bench`
* `Triotek-Ltd/3plug-pro-control`

Source URLs to fork:

* `https://github.com/Triotek-Ltd/triotek-bench`
* `https://github.com/Triotek-Ltd/3plug-pro-control`

You can do that either from the GitHub web UI using the `Fork` button, or with GitHub CLI if `gh` is installed:

```bash
gh auth login -h github.com -p ssh -w
gh repo fork Triotek-Ltd/triotek-bench --clone=false --remote=false
gh repo fork Triotek-Ltd/3plug-pro-control --clone=false --remote=false
```

Replace `YOUR_GITHUB_USER` below with the GitHub account or org that owns those forks.

After forking on the web, verify the SSH URLs you will actually use before Bench setup:

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/triotek-bench.git
git ls-remote git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git
```

If both commands return refs instead of an access error, your fork URLs are ready and you can continue to Bench.

### 5. Prepare the bench host prerequisites

Before installing Bench itself, make sure the host prerequisites are ready.

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench
* https://docs.frappe.io/framework/user/en/installation

#### 5a. Install the base system packages

Efficient base commands on Ubuntu / Debian:

```bash
# run these package steps as the original sudo-capable admin user
sudo apt update
sudo apt install -y git redis-server libmariadb-dev mariadb-server mariadb-client pkg-config xvfb libfontconfig cron \
  python3-dev python3-pip python3-venv software-properties-common build-essential
sudo systemctl enable mariadb redis-server
sudo systemctl start mariadb redis-server
sudo systemctl status mariadb --no-pager
sudo systemctl status redis-server --no-pager
```

#### 5b. Harden and verify MariaDB

Run MariaDB hardening before Bench:

```bash
sudo mariadb-secure-installation
```

Recommended answers for a fresh server:

1. `Enter current password for root`: press `Enter`
2. `Switch to unix_socket authentication`: `Y`
3. `Change the root password`: `Y` only if you want a MariaDB password in addition to socket auth
4. `Remove anonymous users`: `Y`
5. `Disallow root login remotely`: `Y`
6. `Remove test database and access to it`: `Y`
7. `Reload privilege tables now`: `Y`

Then verify MariaDB is actually healthy:

```bash
sudo mariadb -e "SELECT VERSION();"
sudo mariadb -e "SHOW DATABASES;"
```

Set the server character set before creating the bench:

```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Make sure this exists under `[mysqld]`:

```ini
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

Restart and verify:

```bash
sudo systemctl restart mariadb
sudo mariadb -e "SHOW VARIABLES LIKE 'character_set_server';"
sudo mariadb -e "SHOW VARIABLES LIKE 'collation_server';"
sudo systemctl status mariadb --no-pager
```

#### 5c. Install and verify wkhtmltopdf

Install wkhtmltopdf with patched Qt:

Use the package that matches your Ubuntu base when it exists:

* Ubuntu 24.04 (`noble`): use the older supported Ubuntu LTS package `jammy`
* Ubuntu 22.04 (`jammy`): use `jammy`
* Ubuntu 20.04 (`focal`): use `focal`

Check your release first:

```bash
lsb_release -a
```

For Ubuntu 24.04 (`noble`), use:

1. Go to `/tmp`:

```bash
cd /tmp
```

2. Download the package:

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

3. Confirm the file exists:

```bash
ls -lh wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

4. Install the package:

```bash
sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb || sudo apt-get -f install -y
```

5. Run dependency repair once more to be safe:

```bash
sudo apt-get -f install -y
```

6. Verify the final binary:

```bash
wkhtmltopdf --version
which wkhtmltopdf
```

For Ubuntu 20.04 (`focal`), use:

1. Go to `/tmp`:

```bash
cd /tmp
```

2. Download the package:

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
```

3. Confirm the file exists:

```bash
ls -lh wkhtmltox_0.12.6-1.focal_amd64.deb
```

4. Install the package:

```bash
sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb || sudo apt-get -f install -y
```

5. Run dependency repair once more to be safe:

```bash
sudo apt-get -f install -y
```

6. Verify the final binary:

```bash
wkhtmltopdf --version
which wkhtmltopdf
```

### 6. Install the bench that will host 3plug itself

This is the bench that will run the actual control panel.

#### 6a. Install Node.js with `nvm`

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24
node -v
```

#### 6b. Install Yarn

```bash
npm install -g yarn
yarn -v
```

#### 6c. Install `uv` and refresh the shell path

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
```

If `uv` is still shadowed by an older command in your shell, run:

```bash
which uv
```

and confirm the path you want is under `/home/frappe/.local/bin/uv`.

#### 6d. Install Python for Bench

This stack currently supports Python 3.10, 3.11, and 3.12. Do not use Python 3.14 for the first setup run because dependency builds such as `greenlet` can fail during `bench get-app`.

```bash
uv python install 3.11 --default
python3 --version
```

If you already created a bench with Python 3.14 and `bench get-app /opt/triotek/control` failed with a `greenlet` build error, remove that failed bench and recreate it with Python 3.11 before continuing.

#### 6e. Install Bench from the user-owned fork of Triotek Bench

```bash
uv tool install "git+ssh://git@github.com/YOUR_GITHUB_USER/triotek-bench.git"
bench --version
```

#### 6f. Create the Bench workspace under `/opt/triotek`

Bench should run as the `frappe` user, not with `sudo`.

First verify the workspace is owned by `frappe`:

```bash
cd /opt
ls -ld /opt/triotek
```

If `/opt/triotek` is not owned by `frappe`, switch back to the original sudo-capable admin user and fix it:

```bash
sudo chown -R frappe:frappe /opt/triotek
```

Then return to the `frappe` user and continue:

```bash
cd /opt/triotek
pwd
bench init frappe-bench
```

After `bench init` finishes successfully, verify the new bench directory:

```bash
cd /opt/triotek/frappe-bench
pwd
bench --version
```

#### 6g. Clone the 3plug product from the user-owned fork

```bash
cd /opt/triotek
git clone git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git control
cd /opt/triotek/control
npm install --legacy-peer-deps
git remote add upstream git@github.com:Triotek-Ltd/3plug-pro-control.git
git remote -v
```

Once Bench is available on the server:

```bash
cd /opt/triotek/frappe-bench
bench get-app /opt/triotek/control
bench new-site 3plug.yourdomain.com
bench --site 3plug.yourdomain.com install-app press
```

That site, `3plug.yourdomain.com`, is your actual 3plug control panel.

### 5. Run the control panel locally first

For the first boot:

```bash
cd /opt/triotek/frappe-bench
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
