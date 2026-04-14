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

Run the base host setup one command at a time.

#### 1.1 Create `/opt/triotek`

This creates the root folder that will hold the 3plug working files.

```bash
sudo mkdir -p /opt/triotek
```

Check: `/opt/triotek` should now exist.

#### 1.2 Give your admin user access to `/opt/triotek`

This makes the working directory writable by the sudo-capable user you are using right now.

```bash
sudo chown -R $USER:$USER /opt/triotek
```

Check: `ls -ld /opt/triotek` should show your current user as owner.

#### 1.3 Move into `/opt/triotek`

This puts your shell inside the working directory before you continue.

```bash
cd /opt/triotek
```

#### 1.4 Refresh the apt package list

This downloads the latest package metadata from your configured apt repositories.

```bash
sudo apt update
```

#### 1.5 Upgrade installed packages

This upgrades packages that are already installed on the server.

```bash
sudo apt -y upgrade
```

#### 1.6 Install `git`

This installs Git so you can clone repos and work with forks.

```bash
sudo apt -y install git
```

#### 1.7 Install `curl`

This installs `curl` for download-based install steps later in the guide.

```bash
sudo apt -y install curl
```

#### 1.8 Install `vim`

This installs a terminal editor in case you prefer it over `nano`.

```bash
sudo apt -y install vim
```

#### 1.9 Install `ufw`

This installs the firewall tool used in the hardening section.

```bash
sudo apt -y install ufw
```

#### 1.10 Install `fail2ban`

This installs the brute-force protection service used later.

```bash
sudo apt -y install fail2ban
```

#### 1.11 Install `nginx`

This installs Nginx for the control-panel web entrypoint and HTTPS setup.

```bash
sudo apt -y install nginx
```

#### 1.12 Install `certbot`

This installs Certbot so you can request a public TLS certificate later.

```bash
sudo apt -y install certbot
```

#### 1.13 Install the Nginx Certbot plugin

This installs the Certbot plugin that can edit Nginx for certificate setup.

```bash
sudo apt -y install python3-certbot-nginx
```

#### 1.14 Create the `frappe` user

This creates the working user that will own the bench and app files. Stay on your current admin account for now.

```bash
sudo adduser frappe
```

Check: the command should create `/home/frappe`.

#### 1.15 Add `frappe` to the sudo group

This lets the `frappe` user run admin commands when needed.

```bash
sudo usermod -aG sudo frappe
```

#### 1.16 Hand `/opt/triotek` to `frappe`

This transfers ownership of the working tree to the user that will run Bench.

```bash
sudo chown -R frappe:frappe /opt/triotek
```

Check: `ls -ld /opt/triotek` should show `frappe frappe`.

### 2. Do the first server cleanup and layout

Create the base layout before you install the control panel.

#### 2.1 Create `/opt/triotek/control`

This creates the directory where the 3plug product repo will live.

```bash
sudo mkdir -p /opt/triotek/control
```

#### 2.2 Create `/opt/triotek/logs`

This creates a dedicated place for logs and later diagnostics.

```bash
sudo mkdir -p /opt/triotek/logs
```

#### 2.3 Reapply ownership on `/opt/triotek`

This makes sure your current setup user can still write inside the working tree after creating the new directories.

```bash
sudo chown -R $USER:$USER /opt/triotek
```

If this server already has unrelated old test files or abandoned benches, move them out of the way before you begin so the first install is easy to reason about.

### 3. Apply basic security hardening first

Apply the basic hardening before you expose the control panel.

#### Firewall

If the firewall is not already enabled, set it up:

##### 3.1 Allow `OpenSSH`

Allow SSH first so you do not lock yourself out.

```bash
sudo ufw allow OpenSSH
```

##### 3.2 Set inbound traffic to `deny`

Set the default inbound policy.

```bash
sudo ufw default deny incoming
```

##### 3.3 Set outbound traffic to `allow`

Set the default outbound policy.

```bash
sudo ufw default allow outgoing
```

##### 3.4 Open port `80`

Allow HTTP for the first web and certificate flow.

```bash
sudo ufw allow 80/tcp
```

##### 3.5 Open port `443`

Allow HTTPS.

```bash
sudo ufw allow 443/tcp
```

##### 3.6 Enable `ufw`

Enable the firewall.

```bash
sudo ufw enable
```

##### 3.7 Check firewall status

Check the final firewall rules.

```bash
sudo ufw status verbose
```

Check: you should see SSH, `80/tcp`, and `443/tcp` allowed.

#### Fail2ban

Enable brute-force protection.

##### 3.8 Enable `fail2ban` at boot

```bash
sudo systemctl enable fail2ban
```

##### 3.9 Start `fail2ban`

```bash
sudo systemctl start fail2ban
```

##### 3.10 Check `fail2ban` status

```bash
sudo systemctl status fail2ban
```

Check: the service state should be `active (running)`.

You can later tune `/etc/fail2ban/jail.local`, but enabling the service early already helps.

#### SSH hygiene

Do the first SSH hardening pass on the server.

##### 3.11 Back up `sshd_config`

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

##### 3.12 Review current SSH settings

```bash
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
```

##### 3.13 Edit `sshd_config`

Open the file and apply the first SSH hardening pass.

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

##### 3.14 Restart the SSH service

```bash
sudo systemctl restart ssh
```

##### 3.15 Check SSH service status

```bash
sudo systemctl status ssh --no-pager
```

Check: the service should be active before you close any SSH session.

##### 3.16 Recheck the SSH config values

Check that the expected SSH values are in place.

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

Prepare the `frappe` user for git, GitHub SSH, and forks.

#### 4.1 Switch into the working user

Switch to `frappe`.

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

Check the git config.

```bash
git config --global --list
```

Check: confirm your name, email, default branch, and editor are all present.

#### 4.9 Create the SSH directory

```bash
mkdir -p ~/.ssh
```

#### 4.10 Lock down SSH directory permissions

```bash
chmod 700 ~/.ssh
```

#### 4.11 Generate the GitHub SSH key

Create the SSH key pair.

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

Print the public key so you can add it to GitHub.

```bash
cat ~/.ssh/id_ed25519.pub
```

Then do these GitHub-side actions with the same account that should own later changes:

1. Open `GitHub -> Settings -> SSH and GPG keys`
2. Click `New SSH key`
3. Paste the output of `cat ~/.ssh/id_ed25519.pub`
4. Save it with a title such as `3plug-control-server`

#### 4.15 Test GitHub SSH access

Check GitHub SSH access.

```bash
ssh -T git@github.com
```

Check: GitHub should confirm authentication, even if shell access is denied.

Fork these repositories into the GitHub account that should own later changes:

* `Triotek-Ltd/triotek-bench`
* `Triotek-Ltd/3plug-pro-control`

Source URLs to fork:

* `https://github.com/Triotek-Ltd/triotek-bench`
* `https://github.com/Triotek-Ltd/3plug-pro-control`

Choose one forking path below. Do not do both.

#### Option A. Fork in the GitHub web UI

Use the `Fork` button on both source repositories in your browser.

If you already forked both repos in the web UI, skip the GitHub CLI forking steps below and go straight to the verification steps.

#### Option B. Fork with GitHub CLI

Use this path only if you want to fork from the server instead of the browser.

##### 4.16 Install `gh`

This installs GitHub CLI so you can authenticate and create forks from the server.

```bash
sudo apt install -y gh
```

##### 4.17 Check the `gh` version

This confirms that GitHub CLI is available before you try to log in.

```bash
gh --version
```

Check: the command should print a GitHub CLI version instead of `command not found`.

##### 4.18 Authenticate GitHub CLI

This signs GitHub CLI into the GitHub account that should own your forks.

```bash
gh auth login -h github.com -p ssh -w
```

##### 4.19 Fork `triotek-bench`

This creates your fork of `Triotek-Ltd/triotek-bench`.

```bash
gh repo fork Triotek-Ltd/triotek-bench --clone=false --remote=false
```

##### 4.20 Fork `3plug-pro-control`

This creates your fork of `Triotek-Ltd/3plug-pro-control`.

```bash
gh repo fork Triotek-Ltd/3plug-pro-control --clone=false --remote=false
```

Replace `YOUR_GITHUB_USER` below with the GitHub account or org that owns those forks.

#### 4.21 Verify fork access for `triotek-bench`

After you fork by either path above, verify the SSH URL you will actually use before Bench setup:

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/triotek-bench.git
```

#### 4.22 Verify fork access for `3plug-pro-control`

After you fork by either path above, verify the second SSH URL too:

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git
```

If both commands return refs instead of an access error, your fork URLs are ready and you can continue to Bench.

### 5. Prepare the bench host prerequisites

Install the host prerequisites before Bench.

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench
* https://docs.frappe.io/framework/user/en/installation

#### 5a. Install the base system packages

Use these Ubuntu or Debian host steps.

##### 5a.1 Refresh package metadata

```bash
sudo apt update
```

##### 5a.2 Install `redis-server`

This installs Redis for queueing and background job support.

```bash
sudo apt install -y redis-server
```

##### 5a.3 Install `libmariadb-dev`

This installs the MariaDB development headers used by Python dependencies.

```bash
sudo apt install -y libmariadb-dev
```

##### 5a.4 Install `mariadb-server`

This installs the MariaDB database server.

```bash
sudo apt install -y mariadb-server
```

##### 5a.5 Install `mariadb-client`

This installs the MariaDB client tools.

```bash
sudo apt install -y mariadb-client
```

##### 5a.6 Install `pkg-config`

This installs `pkg-config`, which some builds use to find native libraries.

```bash
sudo apt install -y pkg-config
```

##### 5a.7 Install `xvfb`

This installs the virtual framebuffer used by headless render steps.

```bash
sudo apt install -y xvfb
```

##### 5a.8 Install `libfontconfig`

This installs font configuration libraries used by PDF tooling.

```bash
sudo apt install -y libfontconfig
```

##### 5a.9 Install `cron`

This installs the cron service for scheduled tasks.

```bash
sudo apt install -y cron
```

##### 5a.10 Install `python3-dev`

This installs Python headers needed by packages with native extensions.

```bash
sudo apt install -y python3-dev
```

##### 5a.11 Install `python3-pip`

This installs `pip` for Python package management.

```bash
sudo apt install -y python3-pip
```

##### 5a.12 Install `python3-venv`

This installs Python virtual environment support.

```bash
sudo apt install -y python3-venv
```

##### 5a.13 Install `software-properties-common`

This installs helper tools used by repository and package setup workflows.

```bash
sudo apt install -y software-properties-common
```

##### 5a.14 Install `build-essential`

This installs the base C and build toolchain.

```bash
sudo apt install -y build-essential
```

##### 5a.15 Enable `mariadb`

This makes MariaDB start automatically on boot.

```bash
sudo systemctl enable mariadb
```

##### 5a.16 Enable `redis-server`

This makes Redis start automatically on boot.

```bash
sudo systemctl enable redis-server
```

##### 5a.17 Start `mariadb`

This starts the database server now.

```bash
sudo systemctl start mariadb
```

##### 5a.18 Start `redis-server`

This starts Redis now.

```bash
sudo systemctl start redis-server
```

##### 5a.19 Check `mariadb` status

```bash
sudo systemctl status mariadb --no-pager
```

Check: MariaDB should be `active (running)`.

##### 5a.20 Check `redis-server` status

```bash
sudo systemctl status redis-server --no-pager
```

#### 5b. Harden and verify MariaDB

Harden MariaDB before Bench.

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

Check that MariaDB responds normally.

```bash
sudo mariadb -e "SHOW DATABASES;"
```

Check: the command should return the default system databases without errors.

##### 5b.4 Edit the MariaDB server config

Set the MariaDB character set before creating the bench.

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

Check: MariaDB should still be `active (running)` after the config change.

#### 5c. Install and verify wkhtmltopdf

Install wkhtmltopdf with patched Qt.

Use the package that matches your Ubuntu base when it exists:

* Ubuntu 24.04 (`noble`): use the older supported Ubuntu LTS package `jammy`
* Ubuntu 22.04 (`jammy`): use `jammy`
* Ubuntu 20.04 (`focal`): use `focal`

Check the Ubuntu release first.

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

Check: the command should print a version string instead of `command not found`.

##### 5c.7 Confirm the binary path

```bash
which wkhtmltopdf
```

Check: the binary path should resolve successfully.

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

Check: the command should print a version string instead of `command not found`.

##### 5c.14 Confirm the binary path

```bash
which wkhtmltopdf
```

Check: the binary path should resolve successfully.

### 6. Install the bench that will host 3plug itself

This bench will run the real control panel.

If you previously created a broken bench and renamed it to something like `frappe-bench-broken-f16`, do not start from the top of the README again.

Use this restart rule:

* if `bench --version` still works for the `frappe` user, resume from `6f`
* if `/opt/triotek/control` already exists and already points at your 3plug product checkout, keep it and do not clone it again
* if both the Bench tool and the control checkout are already present, your fresh-bench restart point is `6f.1`

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

Check: the version should report Node 24.

#### 6b. Install Yarn

##### 6b.1 Install Yarn globally

```bash
npm install -g yarn
```

##### 6b.2 Verify the Yarn version

```bash
yarn -v
```

Check: the command should print a Yarn version.

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

Check: the command should print a `uv` version.

If `uv` is still shadowed by an older command in your shell, run:

```bash
which uv
```

and confirm the path you want is under `/home/frappe/.local/bin/uv`.

#### 6d. Install Python for Bench

Use Python 3.12 and pin the Frappe source and branch during `bench init`.

Why:

* the default Frappe source currently pulled by `bench init` asks for Python 3.14+
* Python 3.14 is too new for parts of the Press-derived stack and can fail on dependencies such as `greenlet`
* the official Triotek framework base for this product is:
  * `https://github.com/Triotek-Ltd/triotek-frappe.git`
  * branch `main`

##### 6d.1 Install Python 3.12 through `uv`

```bash
uv python install 3.12 --default
```

##### 6d.2 Verify the default Python

```bash
python3 --version
```

Check: the default Python should now be 3.12.

If you already created a bench with Python 3.11, 3.12, or 3.14 and installation failed, remove that failed bench and recreate it with Python 3.12 plus the explicit Frappe source/branch before continuing.

#### 6e. Install Bench from the user-owned fork of Triotek Bench

Use the fork-based Triotek Bench install.

##### 6e.1 Install Bench from the fork

```bash
uv tool install "git+ssh://git@github.com/YOUR_GITHUB_USER/triotek-bench.git"
```

##### 6e.2 Verify the Bench version

```bash
bench --version
```

Check: the command should print a Bench version from your fork install.

Why the docs changed later:

* this Bench install step was already working
* the failures started later, when `bench init` bootstrapped Frappe and when `bench get-app /opt/triotek/control` installed the Press-derived app
* so we did not change the Bench install command itself
* we changed the later bootstrap path so Bench uses a compatible Python and the official Triotek Frappe base

#### 6f. Create the Bench workspace under `/opt/triotek`

Run Bench as `frappe`, not with `sudo`.

If you only renamed the old broken bench and kept the rest of `/opt/triotek`, this is the section to restart from.

##### 6f.1 Move to `/opt`

```bash
cd /opt
```

##### 6f.2 Check the workspace ownership

Check that `frappe` owns the workspace.

```bash
ls -ld /opt/triotek
```

##### 6f.3 Repair ownership if needed

If `/opt/triotek` is not owned by `frappe`, switch back to the original sudo-capable admin user and fix it:

```bash
sudo chown -R frappe:frappe /opt/triotek
```

Then return to the `frappe` user and continue:

Use an explicit Frappe source and branch for this stack instead of letting `bench init` choose its default. The official Triotek base is:

* Frappe source: `https://github.com/Triotek-Ltd/triotek-frappe.git`
* Frappe branch: `main`
* Bench source: `https://github.com/Triotek-Ltd/triotek-bench.git`

This is the part that changed, not the Bench install command above.

The reason is simple:

* your forked Triotek Bench tool installed and ran correctly
* the stale docs were still bootstrapping Frappe from the wrong upstream source
* the fix is to keep using the Triotek Bench command and pin the Triotek Frappe bootstrap path during `bench init`

```bash
cd /opt/triotek
```

##### 6f.4 Confirm the working directory

```bash
pwd
```

Check: the output should be `/opt/triotek`.

##### 6f.5 Create the bench with the pinned Frappe source

```bash
bench init frappe-bench --python /home/frappe/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 --frappe-path https://github.com/Triotek-Ltd/triotek-frappe.git --frappe-branch main
```

Check: the command should finish without stopping in dependency or Frappe bootstrap errors.

##### 6f.6 Move into the new bench

After `bench init`, verify the new bench directory.

```bash
cd /opt/triotek/frappe-bench
```

##### 6f.7 Confirm the bench path

```bash
pwd
```

Check: the output should be `/opt/triotek/frappe-bench`.

##### 6f.8 Check the Bench version inside the workspace

```bash
bench --version
```

Check: Bench should still resolve inside the new workspace.

If `bench init` already failed with the wrong Frappe source or branch, remove that failed bench and rerun it with the explicit `--frappe-path` and `--frappe-branch`.

#### 6g. Clone the 3plug product from the user-owned fork

If `/opt/triotek/control` already exists and is your current 3plug checkout, do not clone it again.

In that case:

* skip `6g.1` through `6g.6`
* move straight to `6g.7`
* make sure the existing checkout has your latest intended code before you continue

##### 6g.1 Clone the product fork

```bash
cd /opt/triotek
```

##### 6g.2 Move into the product checkout

```bash
git clone git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git control
```

##### 6g.3 Move into the product checkout

```bash
cd /opt/triotek/control
```

##### 6g.4 Install frontend dependencies

```bash
npm install --legacy-peer-deps
```

##### 6g.5 Add the upstream remote

```bash
git remote add upstream git@github.com:Triotek-Ltd/3plug-pro-control.git
```

##### 6g.6 Verify the remotes

```bash
git remote -v
```

Check: you should see both `origin` and `upstream`.

Once Bench is ready on the server, install the app into it.

##### 6g.7 Move into the bench

```bash
cd /opt/triotek/frappe-bench
```

##### 6g.8 Register the local app with Bench

```bash
bench get-app /opt/triotek/control
```

##### 6g.9 Create the control-panel site

```bash
bench new-site 3plug.yourdomain.com
```

##### 6g.10 Install the `press` app

```bash
bench --site 3plug.yourdomain.com install-app press
```

Check: the app install should complete without traceback errors.

That site, `3plug.yourdomain.com`, is your actual 3plug control panel.

### 7. Set up the bench for production

Use the production path on the real server. Do not use `bench start` for this setup flow.

#### 7.1 Leave any accidental virtual environment shell

If your prompt shows something like `(env)`, leave that shell first:

```bash
deactivate
```

#### 7.2 Move into the bench

```bash
cd /opt/triotek/frappe-bench
```

#### 7.3 Confirm the site exists

```bash
bench list-sites
```

Check: `3plug.yourdomain.com` should be listed.

#### 7.4 Find the Bench binary path

```bash
which bench
```

Check: this should normally resolve to `/home/frappe/.local/bin/bench`.

#### 7.5 Make Bench available under `/usr/local/bin`

This avoids later production setup issues where `sudo` cannot resolve the Bench command path.

```bash
sudo ln -sf /home/frappe/.local/bin/bench /usr/local/bin/bench
```

#### 7.6 Prepare `pip` inside the Bench tool runtime

If the Bench tool was installed by `uv`, make sure its own Python has `pip` available:

```bash
/home/frappe/.local/share/uv/tools/frappe-bench/bin/python -m ensurepip --upgrade
```

#### 7.7 Verify `pip` inside the Bench tool runtime

```bash
/home/frappe/.local/share/uv/tools/frappe-bench/bin/python -m pip --version
```

#### 7.8 Install Ansible for the Bench tool runtime

This is needed by `bench setup production` when it prepares the production services.

```bash
/home/frappe/.local/share/uv/tools/frappe-bench/bin/python -m pip install ansible
```

#### 7.9 Run production setup

```bash
sudo /home/frappe/.local/bin/bench setup production frappe
```

Check: the production setup should finish without traceback errors.

#### 7.10 Check Supervisor services

```bash
sudo supervisorctl status
```

Check: the Bench web, redis, worker, and scheduler services should all be running.

#### 7.11 Run site migration after services are up

```bash
bench --site 3plug.yourdomain.com migrate
```

#### 7.12 Clear the site cache

```bash
bench --site 3plug.yourdomain.com clear-cache
```

#### 7.13 Confirm the installed apps

```bash
bench --site 3plug.yourdomain.com list-apps
```

Check: you should see both `frappe` and `press`.

After this point, the production bench should be serving the real control panel.

### 8. Put HTTPS in front so the browser does not warn

Point a real domain at the server, then issue the certificate.

Use the basic Nginx and Certbot flow.

#### 8.1 Request the certificate through Nginx

```bash
sudo certbot --nginx -d 3plug.yourdomain.com
```

After that, test renewal:

#### 8.2 Dry-run certificate renewal

```bash
sudo certbot renew --dry-run
```

Check: the dry run should complete successfully.

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

This is the first real control-panel workflow after the bench and site are fully up.

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

This is the next real control-panel workflow after the managed server is registered.

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
```

```powershell
& 'C:\Program Files\nodejs\npm.cmd' install --legacy-peer-deps
```

```powershell
& 'C:\Program Files\nodejs\npm.cmd' run build
```

The verification build uses the guarded local mode added in `dashboard/vite.config.ts`.

Backend syntax checks used during current product work:

```powershell
python -m py_compile press\api\selfhosted.py
```

```powershell
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
