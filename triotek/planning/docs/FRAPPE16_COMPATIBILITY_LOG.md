# Frappe 16 Compatibility Log

This log tracks the repo changes made while moving 3plug Control's Press-derived app toward a clean Frappe 16 install path.

## 2026-04-13

### Goal

Start aligning the app with a Frappe 16 bench instead of continuing to patch a mismatched environment by hand.

### Findings

* The current README and runbook pointed bench bootstrap at `https://github.com/balamurali27/frappe`, branch `fc-ci`.
* On the server, that branch resolved to Frappe `16.0.0-dev`.
* The app dependency metadata still reflected an older Press-era stack, which caused install-time conflicts and import failures.
* Confirmed server-side symptoms included:
  * `ModuleNotFoundError: No module named 'urllib3.contrib.appengine'`
  * `ModuleNotFoundError: No module named 'stripe.six.moves'`
  * pip resolver conflicts between `press` pins and `frappe 16.0.0-dev`

### Repo changes made

#### Dependency metadata

Updated [pyproject.toml](./../../../pyproject.toml) to better match a Frappe 16-style dependency baseline:

* `posthog~=5.0.0`
* `PyGithub>=2.5,<3`
* `pyOpenSSL>=23.2.0,<24`
* `requests~=2.32.4`
* `sql_metadata~=2.17.0`
* `stripe>=11,<14`
* `tomli~=2.2.1; python_version < '3.11'`

Fresh-bench retesting later showed the runtime environment still pulled a dependency path that imports `urllib3.contrib.appengine`.

Because that module was removed in `urllib3 2.x`, the compatibility set was corrected to keep:

* `urllib3<2`

During fresh-bench install testing, `pyOpenSSL~=25.1.0` was found to conflict with `oci==2.116.0`, which requires `pyOpenSSL<24.0.0`.

The pin was therefore corrected to:

* `pyOpenSSL>=23.2.0,<24`

This keeps the app compatible with its current OCI dependency while still avoiding the older, looser historical pin.

Another fresh-bench check showed the environment was resolving to:

* `urllib3 2.6.3`
* `requests 2.32.5`
* `PyGithub 2.9.1`
* `oci 2.116.0`

Despite the newer `PyGithub`, one installed dependency path still expected `urllib3.contrib.appengine`, so the app compatibility set continues to require `urllib3<2` for now.

Added:

* `[tool.bench.frappe-dependencies]`
* `frappe = ">=16.0.0-dev,<=17.0.0-dev"`

Aligned [dev-requirements.txt](./../../../dev-requirements.txt):

* `types-requests~=2.32`

#### TOML compatibility

Added [press/utils/toml.py](./../../../press/utils/toml.py) as a shared TOML compatibility shim using:

* `tomllib` on newer Python
* `tomli` fallback on older Python

Switched TOML usage to the shim in:

* [press/api/github.py](./../../../press/api/github.py)
* [press/press/doctype/app_release/app_release.py](./../../../press/press/doctype/app_release/app_release.py)
* [press/marketplace/doctype/marketplace_app_audit/checks/versioning.py](./../../../press/marketplace/doctype/marketplace_app_audit/checks/versioning.py)
* [press/press/doctype/deploy_candidate/utils.py](./../../../press/press/doctype/deploy_candidate/utils.py)

#### Stripe and Razorpay import safety

Made payment-library imports lazy in [press/utils/billing.py](./../../../press/utils/billing.py):

* `stripe` is now imported inside `get_stripe()`
* `razorpay` is now imported inside `get_razorpay_client()`

Added a Stripe exception compatibility helper:

* `get_stripe_exception(name: str)`

Updated call sites to avoid assuming only the older `stripe.error.*` namespace:

* [press/api/billing.py](./../../../press/api/billing.py)
* [press/press/doctype/team_deletion_request/team_deletion_request.py](./../../../press/press/doctype/team_deletion_request/team_deletion_request.py)
* [press/press/doctype/stripe_webhook_log/stripe_webhook_log.py](./../../../press/press/doctype/stripe_webhook_log/stripe_webhook_log.py)

#### PostHog compatibility

Updated [press/utils/telemetry.py](./../../../press/utils/telemetry.py) to avoid a hard import dependency on a single PostHog client class layout.

The telemetry helper now tries:

* `posthog.Posthog`
* then `posthog.Client`

before quietly disabling telemetry initialization.

#### FrappeClient compatibility

Added [press/utils/frappeclient_compat.py](./../../../press/utils/frappeclient_compat.py) as a shared import shim for `FrappeClient` and `FrappeException`.

Switched these files to use the shim:

* [press/frappe_compute_client/frappe_press_client.py](./../../../press/frappe_compute_client/frappe_press_client.py)
* [press/utils/billing.py](./../../../press/utils/billing.py)
* [press/api/partner.py](./../../../press/api/partner.py)
* [press/press/doctype/site/site.py](./../../../press/press/doctype/site/site.py)
* [press/press/doctype/registry_server/registry_server.py](./../../../press/press/doctype/registry_server/registry_server.py)

### Validation done

Ran Python syntax compilation on the touched compatibility files. That local syntax pass succeeded.

### Server handling note

Do not delete the current broken Frappe 16 bench immediately.

When ready for a clean retest:

* rename the current bench to keep it for reference
* create a fresh bench from the updated repo
* retry install on the clean bench

### Open questions

* Whether the updated dependency set is sufficient for a full clean install without further runtime fixes
* Whether any deeper Frappe 16 framework API changes still affect install, migrate, or first boot
* Whether the final proven Python version should remain `3.12` or move higher once a clean install is verified
