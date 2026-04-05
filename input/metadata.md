# Book metadata overrides

Optional overrides for the metadata generator. Used when you run `python skills/book-metadata/scripts/generate_metadata.py`. Lives in `input/` so it is shared across build outputs.

- **Description**: PDF Subject and EPUB dc:description. Book summary/abstract.
- **Keywords**: Comma-separated list for PDF Keywords and EPUB dc:subject. No quotes needed; use plain values (e.g. `AI, transformation, CEO`).
- **BISAC**: Up to 3 BISAC subject codes (e.g. `COM004000, BUS063000, BUS071000`). Used by KDP, IngramSpark, and other distributors.
- **Identifier**: Set when you have an ISBN (e.g. `Identifier: 978-0-123456-78-9`).
- **Author**, **Publisher**, **Language**: Override values derived from the book folder.
- **Date** (or **Publication date**): Publication date for EPUB `dc:date` (use `YYYY-MM-DD`, or a phrase such as `April 15, 2026`, which the build normalises).

Publisher: Agentic Press
Date: 2026-04-15

Description: European businesses are dangerously underprepared for the largest paradigm shift since the industrial revolution. 

**AI is no longer a technology question. It is a leadership question.**

The Agentic Organisation gives CEOs, boards, and management teams a practical framework for navigating this transformation. Built around five core elements: products, people, process, technology, and data, the book shows how organisations can integrate human and AI agents to operate at a scale previously unimaginable.

Drawing on 25 years of digital transformation experience grounded in the European business context, the book addresses what other AI guides ignore: regulation as competitive advantage, the role of works councils, GDPR as a trust asset, and the pragmatic approach that distinguishes European leadership from Silicon Valley hype.

This is not a book about AI tools. It is a guide to becoming an organisation that is fundamentally built for the agentic era.

**For leaders who want to act, not just understand.**

Keywords: AI; AI transformation;agentic organisation;agentic AI;agentic employee;CEO guide;European business;EU AI Act;digital transformation;AI strategy;management framework;organisational change;AI adoption;future of work;AI leadership;business transformation Europe


BISAC: COM004000, BUS063000, BUS071000
Identifier: 978-90-836902-2-3
