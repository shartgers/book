# Book metadata overrides

Optional overrides for the metadata generator. Used when you run `python skills/book-metadata/scripts/generate_metadata.py`. Lives in `input/` so it is shared across build outputs.

- **Description**: PDF Subject and EPUB dc:description. Book summary/abstract.
- **Keywords**: Comma-separated list for PDF Keywords and EPUB dc:subject. No quotes needed; use plain values (e.g. `AI, transformation, CEO`).
- **Identifier**: Set when you have an ISBN (e.g. `Identifier: 978-0-123456-78-9`).
- **Author**, **Publisher**, **Language**: Override values derived from the book folder.

Description: European businesses are dangerously underprepared for the largest paradigm shift since the industrial revolution. This book is the definitive guide to AI transformation—a practical guidebook for CEOs and leadership teams to benefit from the opportunities AI provides, set in the European context.

Keywords: AI, transformation, CEO, European business, EU AI Act, agentic organisation, leadership, digital transformation
