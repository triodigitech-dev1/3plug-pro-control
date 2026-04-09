# Single-Server Adaptation

## Why this adaptation exists

Press supports a broader hosting and infrastructure model.

3plug should keep the Press architecture while narrowing the first product shape to Triotek's current real need:

* one 3plug deployment per server
* one managed server
* many benches
* many sites

## What stays from Press

Keep the broad Press structure:

* Frappe app backend
* dashboard SPA
* job and agent execution model
* record-based operations instead of loose scripts

Keep the Press resource mindset:

* server as a first-class record
* bench as a first-class record
* site as a first-class record
* jobs as first-class tracked work

## What changes for 3plug v1

Change the initial operating assumptions:

* each 3plug deployment manages its own server
* default to one active server record
* treat benches as children of that server
* treat sites as children of benches
* focus on Bench-managed application lifecycle on that server

Simplify the first action set:

* register server
* register bench
* create site
* install app on site
* inspect inventory and job history

## What to defer from Press

Defer Press areas that do not help the first operator slice:

* cloud provisioning layers
* multi-region and multi-cluster concerns
* broader billing and subscription models
* large marketplace or partner programs
* infrastructure features that require several servers to make sense

## Design guardrails

Adaptation should not mean flattening Press into ad hoc scripts.

Guardrails:

* keep records and permissions in the backend
* keep user actions flowing through jobs
* keep the dashboard as the main operator surface
* keep Bench as the execution layer for Bench-owned actions
* do not turn one 3plug deployment into a shared multi-server control plane in v1
* avoid building major new behavior first in the coordination repo
