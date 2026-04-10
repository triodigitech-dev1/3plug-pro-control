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

### 2. Create the frappe user and switch into it

```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
sudo chown -R frappe:frappe /opt/triotek
sudo su - frappe
cd /opt/triotek
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

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
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

At minimum:

* use SSH keys
* avoid password SSH for privileged access
* confirm the SSH port you intend to use
* keep only intended keys in `authorized_keys`

Quick checks:

```bash
sudo grep -E "^(Port|PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
sudo systemctl status ssh
```

## Phase 3: Prepare the Frappe bench host

### 7. Install Bench using the normal Frappe path

Follow the official Bench host prerequisites first:

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench

After that, confirm Bench is available:

```bash
bench --version
```

### 8. Clone the 3plug product

```bash
cd /opt/triotek
git clone https://github.com/Triotek-Ltd/3plug-pro-control.git control
cd /opt/triotek/control
npm install --legacy-peer-deps
```

### 9. Add the app into the bench

```bash
cd /opt/frappe-bench
bench get-app /opt/triotek/control
```

### 10. Create the real control-panel site

```bash
cd /opt/frappe-bench
bench new-site 3plug.yourdomain.com
bench --site 3plug.yourdomain.com install-app press
```

That site is the actual 3plug control panel.

## Phase 4: Bring up the control panel

### 11. Start it in foreground first

```bash
cd /opt/frappe-bench
bench start
```

This is the easiest first run because you can see immediate errors.

### 12. Verify the site responds

Open the site locally or from the browser once reachable.

If needed:

```bash
curl -I http://127.0.0.1
```

## Phase 5: Enable HTTPS

### 13. Point DNS first

Make sure `3plug.yourdomain.com` resolves to the server's public IP.

Check:

```bash
dig +short 3plug.yourdomain.com
```

### 14. Issue the certificate

```bash
sudo certbot --nginx -d 3plug.yourdomain.com
sudo certbot renew --dry-run
```

Now the browser should stop showing the dangerous-site warning.

## Phase 6: First login and product readiness

### 15. Log in

Open:

```text
https://3plug.yourdomain.com
```

Then:

* log in as administrator
* confirm the dashboard loads
* confirm the operator team exists and has self-hosted server access enabled

### 16. Confirm the SSH key is available

The managed-server flow depends on the default SSH key being available.

Inside the product, open the `Register Managed Server` flow and confirm it shows a default SSH public key.

## Phase 7: Register the first managed server

### 17. Use the same server as the first managed server

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

### 18. Submit registration

After submit, confirm:

* the self-hosted server record is created
* verification runs
* setup begins
* plays are visible

## Phase 8: Onboard the bench

### 19. Open bench onboarding

From the managed server:

* open `Bench Onboarding`

### 20. Configure the real bench path

If the bench already exists on the server, enable existing bench import and use the real path, for example:

```text
/home/frappe/frappe-bench
```

### 21. Run the onboarding flow

In order:

1. save bench settings
2. discover existing bench
3. create managed bench
4. create managed sites
5. restore site files if needed

### 22. Watch the execution state

The current onboarding page should now show:

* onboarding stages
* execution status
* recent jobs
* recent plays

Use those views as the primary evidence during the first MVP test.

## Phase 9: First MVP feedback checklist

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
