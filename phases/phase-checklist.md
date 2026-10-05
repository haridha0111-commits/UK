# Delivery phase gate checklist

Use this as a lightweight workboard. A blank checkbox is an action to complete for an organisation; the portfolio lab is not evidence that production approvals occurred.

## 0. Mobilise
- [ ] Sponsor, product owner, data owner, engineering owner and risk contacts named
- [ ] Scope, decision rights, RACI, assumptions and dependencies approved
- [ ] Definition of done and acceptance evidence agreed

## 1. Discover
- [ ] Source inventory: owner, interface, cadence, grain, volume, sensitivity, use rights
- [ ] Consumer and AI use cases prioritized by value, risk and readiness
- [ ] Current flows, copies, semantic conflicts and pain points mapped

## 2. Contract
- [ ] Source schema and output data-product contracts versioned
- [ ] Grain, keys, semantics, nulls, freshness, revision and quality rules explicit
- [ ] Owner, steward, access, purpose, classification, retention and support recorded

## 3. Architecture
- [ ] Existing enterprise platform/standards reviewed before selecting tools
- [ ] Compatibility, security, privacy, resilience, cost and licence decisions documented
- [ ] Threat model, access matrix, ADRs and NFRs approved by relevant owners

## 4. Ingest
- [ ] Acquisition is repeatable/idempotent and source bytes are retained by version
- [ ] Checksums, run identity, timestamps and source metadata captured
- [ ] Retries, rate limits, alerts, quarantine and replay procedures demonstrated

## 5. Transform
- [ ] Reconciliation checks and quality gates implemented
- [ ] Null, duplicate, schema drift, boundary and revised-source cases handled
- [ ] Curated metrics approved by business/data owner; lineage emitted

## 6. Publish and secure
- [ ] Catalog lists owner, definition, classification, freshness, lineage and quality
- [ ] Least-privilege access and consumer path demonstrated
- [ ] Change notification, deprecation and incident routes documented

## 7. Analytics and AI
- [ ] Analyst acceptance confirms usability and semantic clarity
- [ ] AI uses approved views and parameterized read-only queries only
- [ ] Evaluation includes accuracy, citation, stale data, policy, injection, leakage and abstention
- [ ] Risk owner approves scope and human oversight before pilot

## 8. Operate and scale
- [ ] SLOs agreed; freshness, quality, errors, latency, cost and AI controls monitored
- [ ] Incident, restore, replay, retention and escalation runbooks accepted
- [ ] Operational owner, capacity plan, product review and scale criteria approved

