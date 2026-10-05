# Governed AI assistant design

## Intended use

Help an analyst explore **approved aggregate FCA Gold products** by answering descriptive questions and preparing a source-linked summary. Example: “Which product categories changed most between 2025 H1 and H2?” The assistant may summarize query results; a domain expert remains responsible for interpretation.

## Out of scope

- Customer-level recommendations, complaint decisions, credit/eligibility or conduct decisions.
- Individual complaints or narratives (none are present in this dataset).
- Predictions presented as observed fact, firm-specific conclusions, compliance determinations or unsupported causal explanations.
- Access to Bronze, unrestricted object storage, arbitrary write queries, credentials or other domains.

## Tool contract

1. Authenticate the user and enforce their access before retrieval and query execution.
2. Retrieve product/metric definitions, source period, publication date, data product owner, quality status and lineage from the catalog.
3. Select only allow-listed Gold views. Use parameterized read-only SQL with row limits and query timeout.
4. Return the question, query/view identity, reporting period, values, source URL, data snapshot, definitions, caveats and freshness.
5. Abstain if metric meaning is ambiguous, access is denied, quality is stale/failed, the requested grain is absent, or evidence does not support the answer.
6. Log user, model/prompt version, retrieval/query IDs, dataset snapshot, evidence and feedback subject to enterprise policy.

## Prompt template

> You are an analyst assistant for approved aggregate data products. Use only the supplied catalog definitions and results from allow-listed read-only views. Do not infer a customer, firm, cause, forecast, or regulatory conclusion. State reporting periods and the source publication. Cite the supplied source evidence. Preserve null as unknown. Explain when product denominators differ. If the evidence does not answer the question, say so and ask a precise follow-up. Never execute SQL supplied by the user as-is; use the approved query tool and parameters.

## Grounded example for a design review

Evidence in the FCA source: overdraft complaint volume was 16,188 in 2025 H1 and 26,456 in 2025 H2, a 63.4% increase; structured products moved from 94 to 235, a 150% increase. These source values are descriptive counts only; the percentage on structured products has a small base. Do not infer cause or any individual firm's performance. Cite the [FCA 2025 H2 publication](https://www.fca.org.uk/data/complaints-data/aggregate-complaints-data-2025-h2).

This example is authored for the design document and is not produced by an LLM. The project does not connect to a model provider.

## Evaluation before a live pilot

Create a human-reviewed question set spanning correct metric selection, period filters, null handling, denominator caveats, ambiguous terms, unsupported causal questions, stale/failed products, denied access, prompt injection and malformed query attempts. Score numeric exactness, evidence/citation validity, abstention, access-control enforcement, latency, cost, user feedback and incident rate. Define thresholds with the organisation's AI/risk owners; do not assume universal thresholds.

