# Project Guide — UK Data & AI Fabric Engineering Lab

## Case brief

### Portfolio scenario

You are the Data & AI Fabric Lead in a consulting delivery team working with a **hypothetical UK retail bank**. The bank wants repeatable onboarding, consistent definitions, lineage and reuse across domains. Start with a public regulatory dataset so the engineering design can be demonstrated without inventing customer data or claiming access to a bank's private estate.

The prototype uses the FCA's aggregate complaints publication as one governed source product. It demonstrates the engineering operating model; it is not evidence about the hypothetical bank's complaint volumes, systems or controls.

### Problem statement

The target organisation needs a controlled way to bring external and internal sources into shared analytical products without losing source provenance or relying on undocumented point-to-point pipelines. Teams need repeatable contracts, quality gates, lineage, access controls, reliable refresh/replay, and controlled AI access to approved data. The engagement will establish a thin vertical slice that proves the path from published source through curated data product to analyst and AI consumption.

This is a synthesized portfolio problem statement, not a quote or attributed engagement from a named bank or consultancy.

### Outcomes and success measures

Agree targets during discovery, rather than present invented performance baselines. Candidate measures:

- Source onboarding lead time and percentage of feeds with approved contracts.
- Percentage of published data products with accountable owner, lineage, classification and freshness metadata.
- Pipeline success, recovery time, freshness against source cadence, and quality-gate pass rate.
- Consumer reuse and reduction in duplicate transformations.
- Cost per product/run and storage growth.
- AI evidence coverage, unsupported answer rate, policy block rate, access-control pass rate, and human feedback.

## A-to-Z delivery plan

### Phase 0 — Mobilise and frame

**Do:** identify executive sponsor, source owner, platform/security/privacy/legal stakeholders, analytics users, operations, architecture board and AI risk owner. Agree scope, decision rights, dependencies, assumptions register, delivery cadence and escalation path.

**Deliver:** one-page charter, RACI, stakeholder map, RAID log, discovery questions, definition of done.

**Exit:** sponsor approves a bounded data-product pilot, accountable owners are named, and no internal data is onboarded without authorization.

### Phase 1 — Discover sources and consumers

**Do:** inventory systems, APIs/files/events, owners, formats, cadence, volume, sensitivity, lawful/contractual use, quality issues, existing pipelines, target consumers, and AI use cases. Map the current flow and duplicate copies. Classify each integration as batch, CDC or streaming according to source behavior and business latency need.

**Deliver:** source inventory, current-state flow, consumer journeys, use-case prioritisation, data classification, source constraints and decision log.

**Exit:** the pilot source, product grain, refresh expectations and permitted use are confirmed by owners.

### Phase 2 — Define domain/data-product contracts

**Do:** assign domain owner and technical custodian. Define schema, grain, keys, measures, semantics, source-of-truth, publication version, freshness, null behavior, permitted purposes, classification, access groups, retention, quality thresholds, support and change policy. Separate opened volumes from closed market outcomes. Record product-specific denominator meaning for the FCA context rates.

**Deliver:** versioned source and output contracts, glossary terms, product ownership record, data classification, change-control plan.

**Exit:** business/data owner signs off definitions and consumers accept the contract.

### Phase 3 — Select the platform and guardrails

**Do:** assess existing standards first. Evaluate NiFi for flow control/provenance, object store, Iceberg and compatible catalog, Trino, catalog/lineage, BI and model gateway. Review version compatibility, deployment model, identity integration, network boundaries, secrets, encryption, recovery, cost, support and licence. Decide which capabilities already exist and which are net-new.

**Deliver:** target architecture, ADRs, threat model, access matrix, environment plan, non-functional requirements, migration and cost model.

**Exit:** architecture/security approvals and service owners before production access.

### Phase 4 — Build ingestion and source fidelity

**Do:** create an idempotent acquisition job, verify publisher identity and licence, capture source snapshot/hash/retrieval metadata, stage an immutable Bronze copy, and route bad/missing/schema-changed files to quarantine. Configure retries, rate limits, alerting and controlled replay. Keep secrets out of code and logs.

**Deliver:** version-controlled flow/configuration, source manifest, run records, failure/replay runbook.

**Exit:** repeat-run and correction scenarios retain evidence and cannot silently duplicate or overwrite accepted source versions.

### Phase 5 — Transform and publish Silver/Gold

**Do:** standardise names/types, normalize period layout, preserve source nulls, enforce keys and semantics, derive reviewed metrics, and add tests as deploy-time data quality controls. Keep SQL/Python transformations in version control. Make the context rate's denominator basis visible. Never merge opened and closed measures as if they were event rows.

**Deliver:** curated tables, SQL/model code, data-product docs, rejected-record policy, lineage and reconciliation report.

**Exit:** data owner signs off reconciliation and downstream consumer validates useful outputs.

### Phase 6 — Catalog, access and data mesh/fabric operating model

**Do:** register service/datasets, owners, glossary, classification, schemas, quality, freshness, lineage and support details. Integrate enterprise identity; use least privilege and scoped views. Define domain platform boundaries, central standards, reusable components, exception process and change notification.

**Deliver:** catalog entry, access policies, lineage view, operational ownership, product lifecycle and support model.

**Exit:** a new consumer can discover product meaning, request access through the approved process and trace output back to source.

### Phase 7 — Enable analytics and AI safely

**Analytics:** publish stable Gold products and documented SQL; provide a sample dashboard; validate with users.

**AI:** begin with a read-only assistant for approved aggregate questions. Ground retrieval in catalog metadata and governed views. Require parameterized query tools, allowed-view policy, source period, citations, caveats, refusal on gaps, human review and audit. Test prompt injection, unsupported answers, stale data, no-access requests, ambiguous metrics, malformed queries, PII leakage (in the real internal-data case), model/provider changes and cost.

**Deliver:** AI use-case assessment, data access map, prompt/tool contract, evaluation plan, audit design, human fallback and rollback.

**Exit:** risk owner approves limited pilot after measurable evaluation; high-impact customer decisions remain out of scope.

### Phase 8 — Operate and scale

**Do:** define service SLOs with consumers; monitor freshness, flow status, schema drift, quality, access denials, query latency, cost and AI behavior. Reconcile counts/values; maintain incident, replay, retention, restore and change runbooks. Review product usage and archive obsolete data under policy.

**Deliver:** runbooks, dashboards, incident and problem process, recovery evidence, capacity/cost review, onboarding playbook, quarterly product review.

**Exit:** named teams accept operations and evidence-based expansion criteria.

## Role expectations — Lead/Manager

- Turn business outcomes into prioritized platform capabilities and data-product milestones.
- Facilitate decisions across domains, platform engineering, security, architecture, risk, legal and analytics.
- Balance reusable central controls with domain ownership; resolve ownership and semantic disputes.
- Manage delivery plan, dependencies, vendor choices, budget, capacity, risks, benefits and executive reporting.
- Set engineering standards for contracts, CI/CD, lineage, quality, access, observability and resilience.
- Put AI within data access and governance controls; sponsor evaluation and operational monitoring.
- Demonstrate decisions with trade-offs, ADRs, evidence, measurable acceptance criteria and a clear handover.

## Interview walkthrough (5 minutes)

1. **Situation:** present the bounded hypothetical-bank problem and clarify it is a portfolio scenario.
2. **Why a fabric:** explain distributed source ownership but shared discovery, policy, orchestration, interoperability and observability; avoid describing one vendor product as “the fabric.”
3. **Why this source:** real FCA aggregate tables offer a UK regulatory reporting example with known cadence, revisions and semantic caveats, while avoiding invented consumer data.
4. **Walk the flow:** source manifest/hash → immutable Bronze → schema/quality gates → long-form Silver → reviewed Gold product → catalog/lineage → Trino/BI.
5. **Show engineering judgment:** batch cadence matches source, nulls stay null, source corrections are versioned, opened and closed measures remain separate, rejected inputs quarantine.
6. **AI:** demonstrate read-only grounded access to an approved product with citation, period, query evidence and caveats; say clearly there is no live model in this lab.
7. **Management:** show phase gates, owners, controls, risks, operating metrics and what is needed before expansion into private bank data.

### Sample answer: “What would you deliver in the first 90 days?”

“I would establish ownership and architecture decisions first, then take one source through contract, versioned landing, automated quality checks, curated data product, catalog lineage and an analyst use case. In parallel I would define access, operations and AI guardrails so the pilot is supportable. I would agree baseline and target measures with consumers rather than inventing benefit numbers. I would only scale after source owners, security and operations accept the evidence and runbook.”

## Risks and responses

| Risk | Response |
|---|---|
| Vendor/tool choice precedes requirements | Inventory existing estate, define decision criteria, time-box proof of compatibility, record ADR |
| Source corrections rewrite history | Version snapshot, checksum, publish date, correction/supersession relation |
| Attractive but incorrect joins/metrics | Contracts, grain-aware review, separate measures, owner sign-off |
| Data quality issues pass silently | Fail closed for critical gates; quarantine with evidence; controlled replay |
| Catalog becomes stale documentation | Automate metadata extraction; assign owner; gate release on required metadata |
| AI invents an explanation or uses unauthorized data | Allow-list, read-only tools, cited evidence, access enforcement, abstention and evals |
| Demo is mistaken for a production deployment | Label local MVP and target architecture separately; no compliance/client claims |

