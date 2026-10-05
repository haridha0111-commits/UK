# FCA public complaints tables: source and data contract

## Files and grain

- `fca_product_complaints.csv`: 50 FCA product-category rows, each with complaint volumes for 2024 H1, 2024 H2, 2025 H1 and 2025 H2.
- `fca_product_complaints_context.csv`: 49 FCA product-category rows with complaint rates per 1,000 relevant accounts, balances, policies or agreements. The denominator is product-specific.
- `fca_market_complaints_summary.csv`: four reporting-period rows for market-wide complaint closure, upheld and redress measures.
- `source-manifest.csv`: FCA URL, publication/update/extraction metadata, licence, table grain and SHA-256 for each source CSV.

The values and labels are transcribed from official FCA published tables to CSV form. These are actual public aggregates, not synthetic records or complaint events. FCA-published figures were revised on 15 May 2026 after the regulator investigated a reporting anomaly in one firm's return. The CSVs capture this publication snapshot and should be treated as versioned. The original FCA XLSX is available from the linked official page but is not bundled here.

## Contract and handling rules

- Product table key: `product`; contextual table key: `product`; market key: `reporting_period` after normalization.
- Period columns: `2024_H1`, `2024_H2`, `2025_H1`, `2025_H2`.
- Empty contextual-rate cells remain null. A product absent from the contextual source is not fabricated to fill the gap.
- Zero counts remain zero. Complaint volumes opened and market outcomes closed are distinct measures.
- Context rate comparison across product categories requires care because denominator types vary.
- Source is periodic, not real-time, and does not contain identifiable customers, complaint narratives, account rows or transactions.
- Attribution: FCA, link to the publication, reuse under the Open Government Licence v3 subject to publisher/third-party rights.

Official source: [FCA Aggregate complaints data: 2025 H2](https://www.fca.org.uk/data/complaints-data/aggregate-complaints-data-2025-h2). More detail and software/source links: [`../../sources.md`](../../sources.md).
