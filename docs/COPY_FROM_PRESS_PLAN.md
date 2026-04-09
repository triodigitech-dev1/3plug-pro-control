# Copy From Press Plan

## Purpose

Use the local Press repo as the implementation base without blindly dragging all of Press into 3plug.

Reference:

* `../frappe-press`

## Rule

Define the target first.

Copy or port only the Press slices that serve the defined 3plug v1 scope.

## Source areas to use first

Backend reference:

* `../frappe-press/press`
* `../frappe-press/press/hooks.py`
* `../frappe-press/press/agent.py`
* `../frappe-press/press/press/doctype/server`
* `../frappe-press/press/press/doctype/bench`
* `../frappe-press/press/press/doctype/site`
* `../frappe-press/press/press/doctype/app_source`
* `../frappe-press/press/press/doctype/agent_job`

Dashboard reference:

* `../frappe-press/dashboard/src`

## First copy strategy

Start with a selective port, not a raw full-repo copy.

Recommended order:

1. extract the minimum backend structures needed for server, bench, site, app source, and job flows
2. extract the minimum dashboard shell and operator inventory views
3. extract the minimum job execution pieces needed for tracked actions
4. rename and reshape records only where Triotek-specific naming or one-server assumptions require it

## What not to copy first

Do not pull these areas into the first implementation unless they directly unblock the first slice:

* broad cloud-provider orchestration
* billing-heavy modules
* partner and marketplace breadth
* unrelated infrastructure modules
* advanced distributed operations features

## Execution note

Before any substantial copy work:

* identify the exact Press files and folders to bring over
* record whether each one is copied, ported, or only referenced
* keep the one-server adaptation explicit in follow-up docs and commits
