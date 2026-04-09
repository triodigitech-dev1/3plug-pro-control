# Forensic Layer Plan

## Purpose

Define the first post-cleanup implementation task for 3plug.

That task is a forensic reporting and logging layer.

## Decision

After the current cleanup phase, the first implementation task should be:

* a forensic layer for reporting
* operational logging
* action traceability
* incident and audit evidence collection

## Why it comes first

3plug is being positioned as an operator control plane for one managed server.

That makes traceability a first-order feature:

* every important operator action should be attributable
* every important system action should be reconstructable
* every important change should leave an evidence trail

## First scope

The first forensic layer should cover:

* job execution history
* operator-triggered actions
* site and bench lifecycle changes
* server readiness and environment checks
* security-relevant changes and failures

## First outputs

The first forensic layer should produce:

* structured event logs
* searchable audit records
* incident-oriented reports
* exportable summaries for investigations and review

## Relationship to cleanup

This is a post-cleanup task.

Cleanup comes first so the forensic layer is built around the actual 3plug scope, not around deferred Press product areas.
