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

Start with a clean workspace and do the system prep as explicit subtasks.

#### 1.1 Create the working root

Create the base directory that will hold the control-panel files:

```bash
sudo mkdir -p /opt/triotek
```

#### 1.2 Hand ownership to your current admin user

Make the working directory writable by the sudo-capable user you are using for setup:

```bash
sudo chown -R $USER:$USER /opt/triotek
```

#### 1.3 Move into the working directory

Run the rest of the early setup from the working root:

```bash
cd /opt/triotek
```

#### 1.4 Refresh package metadata

Update the apt package index first:

```bash
sudo apt update
```

#### 1.5 Upgrade the base system

Bring installed packages up to date before adding the control-panel dependencies:

```bash
sudo apt -y upgrade
```

#### 1.6 Install the base packages

Install the core tools used throughout the rest of the setup:

```bash
sudo apt -y install git curl vim ufw fail2ban nginx certbot python3-certbot-nginx
```

#### 1.7 Create the `frappe` working user

Create the application user, but stay on the current sudo-capable admin user until the system-level setup is done:

```bash
sudo adduser frappe
```

#### 1.8 Allow `frappe` to use sudo

Add the new user to the sudo group:

```bash
sudo usermod -aG sudo frappe
```

#### 1.9 Hand the working root to `frappe`

Transfer ownership once the user exists:

```bash
sudo chown -R frappe:frappe /opt/triotek
```

### 2. Do the first server cleanup and layout

Use a clear directory layout before installing the control panel:

#### 2.1 Create the control directory

Create the directory that will hold the cloned product source:

```bash
sudo mkdir -p /opt/triotek/control
```

#### 2.2 Create the logs directory

Create a separate location for operational logs:

```bash
sudo mkdir -p /opt/triotek/logs
```

#### 2.3 Confirm the working tree ownership

Make sure the current setup user can still work inside the tree:

```bash
sudo chown -R $USER:$USER /opt/triotek
```

If this server already has unrelated old test files or abandoned benches, move them out of the way before you begin so the first install is easy to reason about.

### 3. Apply basic security hardening first

Before exposing the control panel, do the basic hardening that reduces avoidable noise and brute-force risk.

#### Firewall

If the firewall is not already enabled, set it up:

##### 3.1 Allow SSH

Keep remote administration open before applying default-deny rules:

```bash
sudo ufw allow OpenSSH
```

##### 3.2 Deny unsolicited inbound traffic

Apply the default inbound policy:

```bash
sudo ufw default deny incoming
```

##### 3.3 Allow outbound traffic

Apply the default outbound policy:

```bash
sudo ufw default allow outgoing
```

##### 3.4 Open HTTP

Allow web traffic for the initial site and certificate flow:

```bash
sudo ufw allow 80/tcp
```

##### 3.5 Open HTTPS

Allow secure browser access:

```bash
sudo ufw allow 443/tcp
```

##### 3.6 Enable the firewall

Turn the rules on:

```bash
sudo ufw enable
```

##### 3.7 Verify the firewall state

Confirm the final ruleset:

```bash
sudo ufw status verbose
```

#### Fail2ban

Enable brute-force protection:

##### 3.8 Enable the service at boot

```bash
sudo systemctl enable fail2ban
```

##### 3.9 Start the service now

```bash
sudo systemctl start fail2ban
```

##### 3.10 Verify the service state

```bash
sudo systemctl status fail2ban
```

You can later tune `/etc/fail2ban/jail.local`, but enabling the service early already helps.

#### SSH hygiene

Do the first SSH hardening pass here on the server itself:

##### 3.11 Back up the SSH daemon config

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

##### 3.12 Review the current SSH settings

```bash
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
```

##### 3.13 Edit the SSH daemon config

Open the file and make the first hardening pass:

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

##### 3.14 Restart SSH

```bash
sudo systemctl restart ssh
```

##### 3.15 Check SSH service health

```bash
sudo systemctl status ssh --no-pager
```

##### 3.16 Recheck the active config

Then verify the expected values are in place:

```bash
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

#### 4.1 Switch into the working user

Start the rest of the source-control setup as `frappe`:

```bash
sudo su - frappe
```

#### 4.2 Move into the working root

```bash
cd /opt/triotek
```

#### 4.3 Set the git user name

```bash
git config --global user.name "Your Name"
```

#### 4.4 Set the git email

```bash
git config --global user.email "your-email@example.com"
```

#### 4.5 Set the default branch name

```bash
git config --global init.defaultBranch main
```

#### 4.6 Keep pull behavior simple

```bash
git config --global pull.rebase false
```

#### 4.7 Set the default editor

```bash
git config --global core.editor nano
```

#### 4.8 Review the git config

Confirm the working user has the expected git settings:

```bash
git config --global --list
```

#### 4.9 Create the SSH directory

```bash
mkdir -p ~/.ssh
```

#### 4.10 Lock down SSH directory permissions

```bash
chmod 700 ~/.ssh
```

#### 4.11 Generate the GitHub SSH key

Create the key pair for this working user:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

#### 4.12 Start the SSH agent

```bash
eval "$(ssh-agent -s)"
```

#### 4.13 Add the new key to the agent

```bash
ssh-add ~/.ssh/id_ed25519
```

#### 4.14 Print the public key

Copy the public key so you can add it to GitHub:

```bash
cat ~/.ssh/id_ed25519.pub
```

Then do these GitHub-side actions with the same account that should own later changes:

1. Open `GitHub -> Settings -> SSH and GPG keys`
2. Click `New SSH key`
3. Paste the output of `cat ~/.ssh/id_ed25519.pub`
4. Save it with a title such as `3plug-control-server`

#### 4.15 Test GitHub SSH access

Check that the server can authenticate to GitHub:

```bash
ssh -T git@github.com
```

Fork these repositories into the GitHub account that should own later changes:

* `Triotek-Ltd/triotek-bench`
* `Triotek-Ltd/3plug-pro-control`

Source URLs to fork:

* `https://github.com/Triotek-Ltd/triotek-bench`
* `https://github.com/Triotek-Ltd/3plug-pro-control`

You can do that either from the GitHub web UI using the `Fork` button, or with GitHub CLI if `gh` is installed.

#### 4.16 Authenticate GitHub CLI

```bash
gh auth login -h github.com -p ssh -w
```

#### 4.17 Fork `triotek-bench`

```bash
gh repo fork Triotek-Ltd/triotek-bench --clone=false --remote=false
```

#### 4.18 Fork `3plug-pro-control`

```bash
gh repo fork Triotek-Ltd/3plug-pro-control --clone=false --remote=false
```

Replace `YOUR_GITHUB_USER` below with the GitHub account or org that owns those forks.

#### 4.19 Verify fork access for `triotek-bench`

After forking on the web, verify the SSH URLs you will actually use before Bench setup:

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/triotek-bench.git
```

#### 4.20 Verify fork access for `3plug-pro-control`

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git
```

If both commands return refs instead of an access error, your fork URLs are ready and you can continue to Bench.

### 5. Prepare the bench host prerequisites

Before installing Bench itself, make sure the host prerequisites are ready.

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench
* https://docs.frappe.io/framework/user/en/installation

#### 5a. Install the base system packages

Efficient base commands on Ubuntu / Debian:

##### 5a.1 Refresh package metadata

```bash
sudo apt update
```

##### 5a.2 Install the bench host dependencies

Run these package steps as the original sudo-capable admin user:

```bash
sudo apt install -y git redis-server libmariadb-dev mariadb-server mariadb-client pkg-config xvfb libfontconfig cron \
  python3-dev python3-pip python3-venv software-properties-common build-essential
```

##### 5a.3 Enable MariaDB and Redis

```bash
sudo systemctl enable mariadb redis-server
```

##### 5a.4 Start MariaDB and Redis

```bash
sudo systemctl start mariadb redis-server
```

##### 5a.5 Check MariaDB status

```bash
sudo systemctl status mariadb --no-pager
```

##### 5a.6 Check Redis status

```bash
sudo systemctl status redis-server --no-pager
```

#### 5b. Harden and verify MariaDB

Run MariaDB hardening before Bench:

##### 5b.1 Run the secure-installation helper

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

##### 5b.2 Confirm MariaDB responds

```bash
sudo mariadb -e "SELECT VERSION();"
```

##### 5b.3 Confirm the server lists databases

Then verify MariaDB is actually healthy:

```bash
sudo mariadb -e "SHOW DATABASES;"
```

##### 5b.4 Edit the MariaDB server config

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

##### 5b.5 Restart MariaDB

```bash
sudo systemctl restart mariadb
```

##### 5b.6 Verify the server character set

```bash
sudo mariadb -e "SHOW VARIABLES LIKE 'character_set_server';"
```

##### 5b.7 Verify the server collation

```bash
sudo mariadb -e "SHOW VARIABLES LIKE 'collation_server';"
```

##### 5b.8 Check final MariaDB status

```bash
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

##### 5c.1 Move into `/tmp`

```bash
cd /tmp
```

##### 5c.2 Download the `jammy` package

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

##### 5c.3 Confirm the package file exists

```bash
ls -lh wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

##### 5c.4 Install the package

```bash
sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb || sudo apt-get -f install -y
```

##### 5c.5 Repair any missing dependencies

```bash
sudo apt-get -f install -y
```

##### 5c.6 Verify the installed binary

```bash
wkhtmltopdf --version
```

##### 5c.7 Confirm the binary path

```bash
which wkhtmltopdf
```

For Ubuntu 20.04 (`focal`), use:

##### 5c.8 Move into `/tmp`

```bash
cd /tmp
```

##### 5c.9 Download the `focal` package

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
```

##### 5c.10 Confirm the package file exists

```bash
ls -lh wkhtmltox_0.12.6-1.focal_amd64.deb
```

##### 5c.11 Install the package

```bash
sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb || sudo apt-get -f install -y
```

##### 5c.12 Repair any missing dependencies

```bash
sudo apt-get -f install -y
```

##### 5c.13 Verify the installed binary

```bash
wkhtmltopdf --version
```

##### 5c.14 Confirm the binary path

```bash
which wkhtmltopdf
```

### 6. Install the bench that will host 3plug itself

This is the bench that will run the actual control panel.

#### 6a. Install Node.js with `nvm`

##### 6a.1 Install `nvm`

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

##### 6a.2 Reload the shell config

```bash
source ~/.bashrc
```

##### 6a.3 Install Node.js 24

```bash
nvm install 24
```

##### 6a.4 Use Node.js 24

```bash
nvm use 24
```

##### 6a.5 Set Node.js 24 as the default

```bash
nvm alias default 24
```

##### 6a.6 Verify the Node.js version

```bash
node -v
```

#### 6b. Install Yarn

##### 6b.1 Install Yarn globally

```bash
npm install -g yarn
```

##### 6b.2 Verify the Yarn version

```bash
yarn -v
```

#### 6c. Install `uv` and refresh the shell path

##### 6c.1 Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

##### 6c.2 Load the `uv` environment

```bash
source $HOME/.local/bin/env
```

##### 6c.3 Verify the `uv` version

```bash
uv --version
```

If `uv` is still shadowed by an older command in your shell, run:

```bash
which uv
```

and confirm the path you want is under `/home/frappe/.local/bin/uv`.

#### 6d. Install Python for Bench

Use Python 3.12 for the first setup run, and pin the Frappe source/branch during `bench init`.

Why:

* the default Frappe source currently pulled by `bench init` asks for Python 3.14+
* Python 3.14 is too new for parts of the Press-derived stack and can fail on dependencies such as `greenlet`
* the project helper install path already pins a compatible Frappe source and branch:
  * `https://github.com/balamurali27/frappe`
  * branch `fc-ci`

##### 6d.1 Install Python 3.12 through `uv`

```bash
uv python install 3.12 --default
```

##### 6d.2 Verify the default Python

```bash
python3 --version
```

If you already created a bench with Python 3.11, 3.12, or 3.14 and installation failed, remove that failed bench and recreate it with Python 3.12 plus the explicit Frappe source/branch before continuing.

#### 6e. Install Bench from the user-owned fork of Triotek Bench

This step has not changed.

The working Bench installation command is still the fork-based Triotek Bench install:

##### 6e.1 Install Bench from the fork

```bash
uv tool install "git+ssh://git@github.com/YOUR_GITHUB_USER/triotek-bench.git"
```

##### 6e.2 Verify the Bench version

```bash
bench --version
```

Why the docs changed later:

* this Bench install step was already working
* the failures started later, when `bench init` bootstrapped Frappe and when `bench get-app /opt/triotek/control` installed the Press-derived app
* so we did not change the Bench install command itself
* we changed the later bootstrap path so Bench uses a compatible Python and a pinned Frappe source/branch

#### 6f. Create the Bench workspace under `/opt/triotek`

Bench should run as the `frappe` user, not with `sudo`.

##### 6f.1 Move to `/opt`

```bash
cd /opt
```

##### 6f.2 Check the workspace ownership

First verify the workspace is owned by `frappe`:

```bash
ls -ld /opt/triotek
```

##### 6f.3 Repair ownership if needed

If `/opt/triotek` is not owned by `frappe`, switch back to the original sudo-capable admin user and fix it:

```bash
sudo chown -R frappe:frappe /opt/triotek
```

Then return to the `frappe` user and continue:

Use an explicit Frappe source and branch for this stack instead of letting `bench init` choose its default. The project helper install path pins:

* Frappe source: `https://github.com/balamurali27/frappe`
* Frappe branch: `fc-ci`

This is the part that changed, not the Bench install command above.

The reason is simple:

* your forked Triotek Bench tool installed and ran correctly
* default `bench init` then pulled a Frappe base that did not match this Press-derived stack cleanly
* the fix is to keep using the same Bench command, but pin the Frappe bootstrap path during `bench init`

```bash
cd /opt/triotek
```

##### 6f.4 Confirm the working directory

```bash
pwd
```

##### 6f.5 Create the bench with the pinned Frappe source

```bash
bench init frappe-bench --python /home/frappe/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 --frappe-path https://github.com/balamurali27/frappe --frappe-branch fc-ci
```

##### 6f.6 Move into the new bench

After `bench init` finishes successfully, verify the new bench directory:

```bash
cd /opt/triotek/frappe-bench
```

##### 6f.7 Confirm the bench path

```bash
pwd
```

##### 6f.8 Check the Bench version inside the workspace

```bash
bench --version
```

If `bench init` was already run with the wrong Frappe source or branch and failed during Frappe install, remove the failed bench and rerun the command above with the explicit `--frappe-path` and `--frappe-branch`.

#### 6g. Clone the 3plug product from the user-owned fork

##### 6g.1 Clone the product fork

```bash
cd /opt/triotek
git clone git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git control
```

##### 6g.2 Move into the product checkout

```bash
cd /opt/triotek/control
```

##### 6g.3 Install frontend dependencies

```bash
npm install --legacy-peer-deps
```

##### 6g.4 Add the upstream remote

```bash
git remote add upstream git@github.com:Triotek-Ltd/3plug-pro-control.git
```

##### 6g.5 Verify the remotes

```bash
git remote -v
```

Once Bench is available on the server:

##### 6g.6 Move into the bench

```bash
cd /opt/triotek/frappe-bench
```

##### 6g.7 Register the local app with Bench

```bash
bench get-app /opt/triotek/control
```

##### 6g.8 Create the control-panel site

```bash
bench new-site 3plug.yourdomain.com
```

##### 6g.9 Install the `press` app

```bash
bench --site 3plug.yourdomain.com install-app press
```

That site, `3plug.yourdomain.com`, is your actual 3plug control panel.

### 7. Run the control panel locally first

#### 7.1 Move into the bench

```bash
cd /opt/triotek/frappe-bench
```

#### 7.2 Start the local dev server

For the first boot:

```bash
bench start
```

If you are still validating the app, keep it in foreground/dev mode first so you can see what breaks quickly.

### 8. Put HTTPS in front so the browser does not warn

Use a real domain that points to the server first, then issue a certificate.

Basic Nginx + Certbot path:

#### 8.1 Request the certificate through Nginx

```bash
sudo certbot --nginx -d 3plug.yourdomain.com
```

After that, test renewal:

#### 8.2 Dry-run certificate renewal

```bash
sudo certbot renew --dry-run
```

This is the simplest way to avoid the browser showing a dangerous-site warning.

The Press base also has TLS-related machinery and certificate records, but for the first live control-panel setup, a straightforward valid public certificate is the right starting point.

### 9. Log into the real 3plug control panel

After the site is up:

* open `https://3plug.yourdomain.com`
* log in as the site administrator
* make sure the operator team has self-hosted server access enabled
* confirm a default SSH key exists, because the managed-server registration flow exposes and uses it

The managed registration page pulls:

* a self-hosted server plan from `press.api.selfhosted.options_for_new`
* the default SSH public key from that same endpoint

### 10. Register the server inside 3plug

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

### 11. Onboard the existing bench

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
