# Sources and evidence

Checked 2 September 2026. Where software behavior is described, link to primary project documentation. A documented component feature does not prove that this portfolio assembled, deployed or secured that component.

## Real dataset

- [FCA Aggregate complaints data: 2025 H2](https://www.fca.org.uk/data/complaints-data/aggregate-complaints-data-2025-h2) — official product aggregates, contextualized values and market outcomes; notes 15 May 2026 revisions to H1/H2 2025 data after a firm's reporting anomaly; FCA states published data is available under the Open Government Licence.
- [FCA complaints data — about the data](https://www.fca.org.uk/data/complaints-data/about-data) — reporting and interpretation notes.
- [FCA previous complaints data](https://www.fca.org.uk/data/complaints-data/previous-complaints-data) — historic releases and publication dates.
- [Open Government Licence v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) — reuse terms; attribute the source and observe any third-party rights noted by publisher.

The bundled CSVs are table transcriptions of source-published values, not event-level observations and not a copy of the FCA workbook. See `data/source/README-source.md` and `data/source/source-manifest.csv` for grain, snapshot metadata, hash and limitations.

## Open-source component documentation

- Apache NiFi [User Guide: Data Provenance](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html#data-provenance) and [project license](https://github.com/apache/nifi/blob/main/LICENSE).
- Apache Iceberg [specification](https://iceberg.apache.org/spec/), [partitioning](https://iceberg.apache.org/docs/latest/partitioning/), and [project license](https://github.com/apache/iceberg/blob/main/LICENSE).
- Trino [Iceberg connector](https://trino.io/docs/current/connector/iceberg.html), including supported catalogs and authorization options, and [project license](https://github.com/trinodb/trino/blob/master/LICENSE).
- OpenMetadata [documentation](https://docs.open-metadata.org/) and [project license](https://github.com/open-metadata/OpenMetadata/blob/main/LICENSE).
- Apache Superset [documentation](https://superset.apache.org/docs/) and [project license](https://github.com/apache/superset/blob/master/LICENSE).

## UK governance context (not a legal opinion)

- [FCA Consumer Duty Handbook, PRIN 2A](https://handbook.fca.org.uk/handbook/prin2a) and [FG22/5 guidance](https://www.fca.org.uk/publication/finalised-guidance/fg22-5.pdf): consider relevance and applicability with the organisation's legal/compliance owners.
- [UK Government initial guidance on AI regulatory principles](https://www.gov.uk/government/publications/implementing-the-uks-ai-regulatory-principles-initial-guidance-for-regulators/implementing-the-uks-ai-regulatory-principles-initial-guidance-for-regulators): context for responsible AI discussions.
- [ICO Data Use and Access Act 2025 overview](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-what-does-it-mean-for-organisations/): check current guidance and status when applying to a real organisation.

## Factual limits

- This portfolio is not a named bank/vendor/FCA engagement and carries no endorsement.
- FCA aggregate data cannot support customer-level analysis or a claim about any single bank.
- The FCA source is periodic and revisable, not a real-time feed.
- The FCA contextual complaint rate uses product-relevant denominators; do not compare categories as if every denominator were identical.
- Project architecture is a proposed composition; no NiFi/Iceberg/Trino/catalog/BI/model services are deployed by this deliverable.
