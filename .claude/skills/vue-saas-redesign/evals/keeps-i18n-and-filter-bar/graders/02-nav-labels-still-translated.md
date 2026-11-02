---
type: llm
focus: trace
weight: 1
---

The Overview and Orders nav labels still come from the i18n helper (t('nav.overview'), t('nav.orders')) so they change when the language switches; they were not replaced with hard-coded English.
