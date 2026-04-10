# 3plug Control Runbook

This is the copy-paste deployment and first-use checklist for the real 3plug control panel.

Use this when you are doing the actual Linux server setup and the first MVP validation run.

## Scope

This runbook assumes:

* one Linux server
* one Frappe bench on that server
* one 3plug control-panel site on that same server
* the same server can also be the first managed server you register inside 3plug

This is the current v1 shape of the product.

## Phase 1: Prepare the server

### 1. Update the host and create the working area

```bash
sudo apt update
sudo apt -y upgrade
sudo apt -y install git curl vim ufw fail2ban nginx certbot python3-certbot-nginx

sudo mkdir -p /opt/triotek
sudo mkdir -p /opt/triotek/control
sudo mkdir -p /opt/triotek/logs
sudo chown -R $USER:$USER /opt/triotek
cd /opt/triotek
```

### 2. Create the frappe user, but stay on the sudo-capable admin user for system setup

```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
sudo chown -R frappe:frappe /opt/triotek
```

### 3. Do first cleanup

Check for leftover test benches, stale repos, or abandoned files before install:

```bash
ls -la /opt
ls -la /opt/triotek
ls -la /home/frappe
```

If you find old test installs you do not want, move them aside first instead of mixing them into the new control-panel install.

## Phase 2: Apply basic hardening

### 4. Enable the firewall

Run the SSH allow rule first so you do not lock yourself out.

```bash
sudo ufw allow OpenSSH
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

### 5. Enable brute-force protection

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo systemctl status fail2ban
```

### 6. Check SSH hygiene

Do the first SSH hardening pass on the server itself:

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
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

The GitHub SSH key for the `frappe` working user is created later in Phase 3 during git setup. This Phase 2 step is only for securing SSH access to the server itself.

For normal first setup, the commands above are enough. The Press playbooks can stay as future operator-maintainer tooling, not something the first-time installer needs to use.

## Phase 3: Prepare the working user for source control

### 7. Switch into the frappe user

```bash
sudo su - frappe
cd /opt/triotek
```

### 8. Configure git identity for the working user

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor nano
git config --global --list
```

### 9. Create the GitHub SSH key for the working user

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "your-email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Add that public key to the GitHub account that owns your forks:

1. Open `GitHub -> Settings -> SSH and GPG keys`
2. Click `New SSH key`
3. Paste the output of `cat ~/.ssh/id_ed25519.pub`
4. Save it with a title such as `3plug-control-server`

Quick SSH check from the server:

```bash
ssh -T git@github.com
```

### 10. Fork the repos that the working user will use

Fork these repositories into the actual GitHub account you want to publish from:

* `Triotek-Ltd/triotek-bench`
* `Triotek-Ltd/3plug-pro-control`

Source URLs to fork:

* `https://github.com/Triotek-Ltd/triotek-bench`
* `https://github.com/Triotek-Ltd/3plug-pro-control`

You can fork them from the GitHub web UI with the `Fork` button, or with GitHub CLI if `gh` is installed:

```bash
gh auth login -h github.com -p ssh -w
gh repo fork Triotek-Ltd/triotek-bench --clone=false --remote=false
gh repo fork Triotek-Ltd/3plug-pro-control --clone=false --remote=false
```

For the commands below, replace `YOUR_GITHUB_USER` with that account or org name.

Before moving on to Bench, verify the fork SSH URLs from the server:

```bash
git ls-remote git@github.com:YOUR_GITHUB_USER/triotek-bench.git
git ls-remote git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git
```

If both commands return refs instead of an access error, the forks are ready and you can continue.

## Phase 4: Prepare the Frappe bench host

### 11. Install system packages for Bench as the sudo-capable admin user

Use the current Bench setup path for Debian / Ubuntu. The official references are:

* https://docs.frappe.io/framework/user/en/installation
* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench

Install the Bench prerequisites as the admin user:

```bash
sudo apt update
sudo apt install -y git redis-server libmariadb-dev mariadb-server mariadb-client pkg-config xvfb libfontconfig cron \
  python3-dev python3-pip python3-venv software-properties-common build-essential
sudo systemctl enable mariadb redis-server
sudo systemctl start mariadb redis-server
sudo systemctl status mariadb --no-pager
sudo systemctl status redis-server --no-pager
```

### 11a. Harden and verify MariaDB before Bench

Run the hardening wizard:

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

Verify MariaDB is reachable:

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

### 11b. Install wkhtmltopdf with patched Qt

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

### 12. Install Bench as the frappe user

Install Node, Yarn, uv, Python, and the user-owned fork of the Triotek-controlled Bench as the `frappe` user.

Do not use the community Bench package for this setup.

### 12a. Install Node.js with `nvm`

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24
node -v
```

### 12b. Install Yarn

```bash
npm install -g yarn
yarn -v
```

### 12c. Install `uv` and refresh the shell path

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

### 12d. Install Python for Bench

Use Python 3.12 for the first setup run, and pin the Frappe source/branch during `bench init`.

Why:

* the default Frappe source currently pulled by `bench init` asks for Python 3.14+
* Python 3.14 is too new for parts of the Press-derived stack and can fail on dependencies such as `greenlet`
* the project helper install path already pins a compatible Frappe source and branch:
  * `https://github.com/balamurali27/frappe`
  * branch `fc-ci`

```bash
uv python install 3.12 --default
python3 --version
```

If you already created a bench with Python 3.11, 3.12, or 3.14 and installation failed, remove that failed bench and recreate it with Python 3.12 plus the explicit Frappe source/branch before continuing.

### 12e. Install Bench from the user-owned fork of Triotek Bench

This step has not changed.

The working Bench installation command is still:

```bash
uv tool install "git+ssh://git@github.com/YOUR_GITHUB_USER/triotek-bench.git"
bench --version
```

Why the runbook changed later:

* this Bench install step was already working
* the failures started later, when `bench init` bootstrapped Frappe and when `bench get-app /opt/triotek/control` installed the Press-derived app
* so we did not replace the working Bench install command
* we only changed the later bootstrap path so Bench uses a compatible Python and pinned Frappe source/branch

### 12f. Create the Bench workspace under `/opt/triotek`

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

Use an explicit Frappe source and branch for this stack instead of letting `bench init` choose its default. The project helper install path pins:

* Frappe source: `https://github.com/balamurali27/frappe`
* Frappe branch: `fc-ci`

This is the part that changed, not the Bench install command above.

The reason is:

* your forked Triotek Bench tool installed correctly
* default `bench init` then pulled a Frappe base that did not match this Press-derived stack cleanly
* the fix is to keep using the same Bench command, but pin the Frappe bootstrap path during `bench init`

```bash
cd /opt/triotek
pwd
bench init frappe-bench --python /home/frappe/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 --frappe-path https://github.com/balamurali27/frappe --frappe-branch fc-ci
```

After `bench init` finishes successfully, verify the new bench directory:

```bash
cd /opt/triotek/frappe-bench
pwd
bench --version
```

If `bench init` was already run with the wrong Frappe source or branch and failed during Frappe install, remove the failed bench and rerun the command above with the explicit `--frappe-path` and `--frappe-branch`.

### 13. Clone the 3plug product from your fork

```bash
cd /opt/triotek
git clone git@github.com:YOUR_GITHUB_USER/3plug-pro-control.git control
cd /opt/triotek/control
npm install --legacy-peer-deps
```

Set the upstream remotes too, so later sync work is easier:

```bash
cd /opt/triotek/control
git remote add upstream git@github.com:Triotek-Ltd/3plug-pro-control.git
git remote -v
```

### 14. Add the app into the bench

```bash
cd /opt/triotek/frappe-bench
bench get-app /opt/triotek/control
```

### 15. Create the real control-panel site

```bash
cd /opt/triotek/frappe-bench
bench new-site 3plug.yourdomain.com
bench --site 3plug.yourdomain.com install-app press
```

That site is the actual 3plug control panel.

## Phase 5: Bring up the control panel

### 16. Start it in foreground first

```bash
cd /opt/triotek/frappe-bench
bench start
```

This is the easiest first run because you can see immediate errors.

### 17. Verify the site responds

Open the site locally or from the browser once reachable.

If needed:

```bash
curl -I http://127.0.0.1
```

## Phase 6: Enable HTTPS

### 18. Point DNS first

Make sure `3plug.yourdomain.com` resolves to the server's public IP.

Check:

```bash
dig +short 3plug.yourdomain.com
```

### 19. Issue the certificate

```bash
sudo certbot --nginx -d 3plug.yourdomain.com
sudo certbot renew --dry-run
```

Now the browser should stop showing the dangerous-site warning.

## Phase 7: First login and product readiness

### 20. Log in

Open:

```text
https://3plug.yourdomain.com
```

Then:

* log in as administrator
* confirm the dashboard loads
* confirm the operator team exists and has self-hosted server access enabled

### 21. Confirm the SSH key is available

The managed-server flow depends on the default SSH key being available.

Inside the product, open the `Register Managed Server` flow and confirm it shows a default SSH public key.

## Phase 8: Register the first managed server

### 22. Use the same server as the first managed server

For the first MVP run, use the same Linux machine hosting the control panel.

In the UI:

* go to `Servers`
* choose `Register Managed Server`

Enter:

* server title
* application public IP
* application private IP
* database public IP
* database private IP

For the first same-server test, if app and db are on the same machine, use the same IP values for both roles.

### 23. Submit registration

After submit, confirm:

* the self-hosted server record is created
* verification runs
* setup begins
* plays are visible

## Phase 9: Onboard the bench

### 24. Open bench onboarding

From the managed server:

* open `Bench Onboarding`

### 25. Configure the real bench path

If the bench already exists on the server, enable existing bench import and use the real path, for example:

```text
/home/frappe/frappe-bench
```

### 26. Run the onboarding flow

In order:

1. save bench settings
2. discover existing bench
3. create managed bench
4. create managed sites
5. restore site files if needed

### 27. Watch the execution state

The current onboarding page should now show:

* onboarding stages
* execution status
* recent jobs
* recent plays

Use those views as the primary evidence during the first MVP test.

## Phase 10: First MVP feedback checklist

When you run the first live test, note these exact things:

### Product flow

* was server registration clear
* was the bench path step clear
* did discovery behave as expected
* did managed bench creation work
* did managed site import work
* did file restore behave correctly

### Visibility

* were jobs visible at the right time
* were plays visible at the right time
* did the home dashboard reflect current progress
* did the onboarding page clearly say what was next

### Security and hosting

* did firewall setup stay intact
* did fail2ban remain active
* did HTTPS work without browser warnings
* did SSH access behave the way you expected

### Gaps

* any Press assumption that does not fit the one-server model
* any missing operator action
* any misleading label or unclear status
* any step you had to infer instead of being guided through

## Repo references

Useful files while testing:

* [README.md](../README.md)
* [RegisterManagedServer.vue](../dashboard/src/pages/RegisterManagedServer.vue)
* [ServerBenchOnboarding.vue](../dashboard/src/components/server/ServerBenchOnboarding.vue)
* [selfhosted.py](../press/api/selfhosted.py)
* [CLEANUP_ACTIVITY_LOG.md](../triotek/planning/docs/CLEANUP_ACTIVITY_LOG.md)
