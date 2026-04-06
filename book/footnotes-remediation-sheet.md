# Footnotes Remediation Sheet (`[^1]` to `[^111]`)

## How these footnotes were created (fact-check agent)

The **`skills/fact-check-agent`** workflow (see `skills/fact-check-agent/SKILL.md`) adds footnotes when a sentence contains **numbers, sweeping assertions, or named research**. It:

1. Checks `research/` first (`book-research-claude.md`, `chapter-*-web-research.md`, chapter briefs).
2. If needed, uses targeted web discovery and records findings in research files.
3. Writes footnotes as: `Organisation, "Report or Article Title", Year`.

That process optimises for **coverage and readable attribution**, not always for **publisher-grade traceability** (stable URL, exact publication title, primary PDF). **`REPLACE`** here means: the citation is *plausible and research-backed*, but for strict publishing we should swap to a **primary document** or **tighten the claim** to match what the source *actually* says.

---

## Compact index

Legend:

- `KEEP`: a **usable public URL** is identified; you should still spot-check the claim in the source body.
- `REPLACE`: needs a **stronger primary** (exact report page/PDF), or **claim edit**, or **split footnotes** if one citation covers multiple independent stats.
- `NOT_VERIFIED`: quote/number not yet checked line-by-line in the primary source.
- `VERIFIED_QUOTE`: quote text confirmed in the linked source.
- `PARTIAL_SECONDARY_QUOTE`: quote appears in secondary coverage; prefer OEM press or report.

Format: `footnote | action | support_status | source_url | current_citation`

`[^1]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | MIT, "NANDA Report", 2025
`[^2]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", September/October 2025
`[^3]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "CEO Playbook", June 2025
`[^4]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era | McKinsey, "The Agentic Organization: Contours of the Next Paradigm for the AI Era", September 2025
`[^5]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", October 2025
`[^6]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | EU Commission, "Agentic AI Venture Capital Report", January 2026
`[^7]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte Global, "Governance of AI: A Critical Imperative for Today's Boards, 2nd Edition", 2025
`[^8]` | KEEP | NOT_VERIFIED | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | EU, "AI Act", 2024
`[^9]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Eurostat, "AI in Enterprises", December 2025
`[^10]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | World Economic Forum, "Europe's AI adoption lag analysis", 2025
`[^11]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Radar", January 2026
`[^12]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | S&P Global Market Intelligence, "Outlook on Generative AI", 2025
`[^13]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", October 2025
`[^14]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era | McKinsey, "The Agentic Organization", September 2025
`[^15]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte Global, "Governance of AI: A Critical Imperative for Today's Boards, 2nd Edition", 2025
`[^16]` | KEEP | NOT_VERIFIED | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | EU, "AI Act", 2024
`[^17]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Superagency in the Workplace", January 2025
`[^18]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Writer / Workplace Intelligence, "State of AI at Work", 2025
`[^19]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "CEO Playbook for AI Transformations", June 2025
`[^20]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "AI Maturity and Business Outcomes Survey", Q4 2024
`[^21]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Cisco, "AI Readiness Index", 2025
`[^22]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte, "Tech Trends 2025", 2025
`[^23]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Capgemini Research Institute, "AI Agents in the Enterprise", 2025
`[^24]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | PwC, "AI Agent Survey", 2025
`[^25]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "Hype Cycle for Artificial Intelligence", 2025
`[^26]` | KEEP | VERIFIED_QUOTE | https://www.bobsguide.com/ing-turns-ai-strategy-into-tangible-results/ | Yilmaz, World Economic Forum, Davos, 2025
`[^27]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "From Potential to Profit: Closing the AI Impact Gap", 2025
`[^28]` | KEEP | VERIFIED_QUOTE | https://www.weforum.org/stories/2025/12/how-to-rebuild-enterprise-for-age-of-agentic-ai/ | Habib, World Economic Forum, Davos, January 2025
`[^29]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Sarkar, "AI Agents and Software Productivity", SSRN, November 2025
`[^30]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Stanford / World Bank, "AI Impact on Work Productivity Survey", 2024
`[^31]` | REPLACE | PARTIAL_SECONDARY_QUOTE | https://completeaitraining.com/news/after-the-storm-faster-payouts-allianzs-project-nemo-clears/ | Allianz, "Project Nemo", 2025
`[^32]` | KEEP | NOT_VERIFIED | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | EU, "AI Act", 2024
`[^33]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Germany, "Works Constitution Act (Betriebsverfassungsgesetz)", 2021
`[^34]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deutsche Telekom, "AI Guidelines", 2023
`[^35]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Nanterre Tribunal Judiciaire, ruling on AI workplace consultation, February 2025
`[^36]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Allianz, "EU AI Pact", November 2024
`[^37]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", October 2025
`[^38]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Huble, "AI Readiness Report", 2024
`[^39]` | KEEP | NOT_VERIFIED | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | EU, "AI Act", 2024
`[^40]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Harvard Business School / BCG, "Navigating the Jagged Technological Frontier", 2023
`[^41]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Typeface, "Signal Report", 2025
`[^42]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Google, "Project Aristotle", 2016
`[^43]` | KEEP | NOT_VERIFIED | https://www.infosys.com/newsroom/press-releases/2025/psychological-safety-driving-ai-initiatives.html | MIT Technology Review / Infosys, "AI and Psychological Safety Survey", December 2025
`[^44]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Slack, "Workforce Index", Fall 2024
`[^45]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BearingPoint, "AI Adoption in the Enterprise", 2025
`[^46]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Kore.ai, "Agentic Wealth Management Case Study", 2025
`[^47]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Airbus / GitHub, "GitHub Copilot at Airbus", 2024
`[^48]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | EY, "European AI Barometer", 2025
`[^49]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | IDC, "AI Project Deployment Survey", 2024
`[^50]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Agents for Growth", November 2025
`[^51]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Why Digital Trust Truly Matters", September 2022
`[^52]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Rewired", 2023
`[^53]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Center of Excellence Research", 2024
`[^54]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Radar", January 2026
`[^55]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", October 2025
`[^56]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte, "Tech Trends 2025", 2025
`[^57]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Capgemini Research Institute, "AI Agents in the Enterprise", 2025
`[^58]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Rewired", 2023
`[^59]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^60]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era | McKinsey, "The Agentic Organization", September 2025
`[^61]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | The Digital Bloom, "2025 Organic Traffic Crisis Report"; Click-Vision, "Zero Click Search Statistics 2026"
`[^62]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Bain & Company, "Goodbye Clicks, Hello AI: Zero-Click Search Redefines Marketing", 2025
`[^63]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | Netflix and Amazon figures widely cited in industry reporting; see e.g. McKinsey, "State of AI", 2025
`[^64]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Medallia, "How Brands Using AI Personalization Drive Customer Experience", 2025
`[^65]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^66]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, press release, August 2025
`[^67]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "Agents Accelerate the Next Wave of AI Value Creation", 2025
`[^68]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2024
`[^69]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era | McKinsey, "The Agentic Organization", September 2025
`[^70]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | European Trade Union Institute, "Collective Bargaining and AI", 2025
`[^71]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Talent and Training", 2025
`[^72]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | CNBC / Financial Times, "Accenture ties promotions to AI tool usage", February 2026
`[^73]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Harvard Data Science Review, "The Agent-Centric Enterprise", Winter 2026
`[^74]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^75]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "Data Readiness for AI", July 2024
`[^76]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte, "Trustworthy AI", 2025
`[^77]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | MIT Sloan, "GenAI Divide: State of AI in Business 2025", August 2025
`[^78]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^79]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "Building the AI Muscle of Your Business Leaders", 2025
`[^80]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Everworker AI, "Team Enablement for AI Agent Platforms", 2026
`[^81]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | European Parliament / Lexology, "GDPR and EU AI Act Compliance Overlap", 2025
`[^82]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "AI Maturity and Trust Survey", June 2025
`[^83]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Accenture / AWS / Stanford, "Responsible AI from Risk to Value", 2025
`[^84]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^85]` | KEEP | NOT_VERIFIED | https://digital-strategy.ec.europa.eu/en/policies/ai-pact | European Commission, "EU AI Pact", 2024
`[^86]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | McKinsey, "European VC and AI Investment Report", 2024
`[^87]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Pew Research Center, "Global Trust in AI Governance", 2025
`[^88]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Deloitte, "European Trust Survey", 2025
`[^89]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Accenture, "AI Achievers: Designing AI Responsibly", 2025
`[^90]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Capgemini, "Rise of Agentic AI", 2025
`[^91]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Edelman, "Trust Barometer", 2026
`[^92]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Auxilion, "EU AI Act Compliance Benefits Analysis", 2025
`[^93]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Eurostat / Accenture, "Nordic AI Adoption and Scaling", 2025
`[^94]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Radar", January 2026
`[^95]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Klarna, "Customer Service Research", 2024
`[^96]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Accenture, "AI Achievers: Designing AI Responsibly", 2025
`[^97]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | MIT Sloan, "GenAI Divide: State of AI in Business 2025", August 2025
`[^98]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | S&P Global, "Outlook on Generative AI", 2025
`[^99]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "Data Readiness for AI", July 2024
`[^100]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI at Work", 2024
`[^101]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Bain & Company, "AI in Private Equity", 2025
`[^102]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Cisco, "AI Readiness Index", 2025
`[^103]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | MIT CISR, "Enterprise AI Maturity Model", 2024
`[^104]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^105]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | Gartner, "Data Readiness for AI", July 2024
`[^106]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "Measuring AI Impact", 2025
`[^107]` | KEEP | NOT_VERIFIED | https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai | McKinsey, "State of AI", 2025
`[^108]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "The Widening AI Value Gap", October 2025
`[^109]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | BCG, "AI Radar", January 2026
`[^110]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | PwC / European Institute of Innovation and Technology, "AI Jobs Barometer", 2025
`[^111]` | REPLACE | NOT_VERIFIED | NEEDS_PRIMARY_URL | PwC, "Global CEO Survey", 2026

---

## `REPLACE` entries — rationale and alternatives

For each footnote, **why it was attached** (fact-check logic + `research/` trail), **why strict publishing wants a change**, and **one or two stronger alternatives** (URLs already present in project research or official publishers).

---

### `[^1]` — MIT, "NANDA Report", 2025

| Field | Detail |
|--------|--------|
| **Claim in book** | Very high pilot failure / low sustained impact; methodology described (300+ initiatives, 52 orgs, 153 leaders). |
| **Why cited (fact-check origin)** | `research/book-research-claude.md` and `research/ch5 - The AI Transformation Framework.md` anchor the headline statistic to **MIT Project NANDA**, report title commonly shortened to **"NANDA"** / **GenAI Divide** — meets "named report + statistics" rule. |
| **Why REPLACE** | **"NANDA Report"** is shorthand; the public title is **"The GenAI Divide: State of AI in Business 2025"**. You need the **MIT-published PDF / landing page**, not a generic label. |
| **Alternatives** | (1) MIT Sloan / Project NANDA publication page for **GenAI Divide 2025** (use exact CISR/MIT URL from the report footer). (2) If the sentence mixes **two studies** (BCG 5% / 60% appear in the same paragraph), **split footnotes** — `[^2]` already covers BCG; keep MIT claims only under MIT. |

---

### `[^2]` — BCG, "The Widening AI Value Gap", September/October 2025

| Field | Detail |
|--------|--------|
| **Claim** | 5% at scale vs 60% no material value (and related executive-survey framing). |
| **Why cited** | `research/book-research-claude.md` and `research/chapter-01-web-research.md` explicitly tie these figures to **BCG Widening AI Value Gap**. |
| **Why REPLACE** | Title/date variants (**September vs October**) reflect **two BCG releases**; you should cite **one** primary PDF or publication page and match wording. |
| **Alternatives** | (1) PDF: `https://media-publications.bcg.com/The-Widening-AI-Value-Gap-October-2025.pdf` (from `research/chapter-01-web-research.md`). (2) BCG publication hub: `https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap` |

---

### `[^3]` — McKinsey, "CEO Playbook", June 2025

| Field | Detail |
|--------|--------|
| **Claim** | e.g. widespread gen-AI use vs limited enterprise impact ("eight in ten" style stats — check exact sentence in ch01). |
| **Why cited** | McKinsey **global survey** family is the standard bucket for **adoption vs EBIT** patterns; fact-check uses **short internal title "CEO Playbook"** from research notes. |
| **Why REPLACE** | **"CEO Playbook"** may not be the **exact** public article title; McKinsey often titles **"CEO guide" / "The State of AI"** pieces differently by month. |
| **Alternatives** | (1) **McKinsey State of AI** roundup: `https://www.mckinsey.com/featured-insights/mckinsey-global-surveys/the-state-of-ai` (verify the specific percentage in the current edition). (2) Search McKinsey.com for the **June 2025** piece whose executive-summary numbers match your sentence. |

---

### `[^5]` — BCG, "The Widening AI Value Gap", October 2025

| Field | Detail |
|--------|--------|
| **Claim** | Top 5% "future-built" multiples (TSR, revenue, EBIT) and spend vs laggards. |
| **Why cited** | `research/chapter-01-web-research.md` Finding 4–5 maps **exact multiples** to this BCG report. |
| **Why REPLACE** | Same as `[^2]`: pick **one** BCG document and verify each multiple in-table. |
| **Alternatives** | (1) October PDF (above). (2) BCG press snapshot if you prefer non-PDF: `https://www.bcg.com/press/30september2025-ai-leaders-outpace-laggards-revenue-growth-cost-savings` |

---

### `[^6]` — EU Commission, "Agentic AI Venture Capital Report", January 2026

| Field | Detail |
|--------|--------|
| **Claim** | Europe’s share of VC to agentic AI vs US; hubs named. |
| **Why cited** | Commission **StepUp / digital strategy** materials on **agentic AI** were used in later research synthesis (`research/ch09-europes-distinctive-edge.md` style compilations). |
| **Why REPLACE** | The **exact title** must match the Commission library entry; do not paraphrase series name. |
| **Alternatives** | (1) European Commission digital strategy library (search: **"Agentic AI: Leveraging European AI talent"**). (2) **Eurostat + national VC** statistics if you only need **investment gap**, not "agentic" label. |

---

### `[^7]` — Deloitte, "Governance of AI: Critical Imperative…", 2nd Ed, 2025

| Field | Detail |
|--------|--------|
| **Claim** | Board AI literacy / metrics / policy percentages (Deloitte board pulse). |
| **Why cited** | `research/chapter-01-web-research.md` Finding 11 gives **Deloitte** as source for board statistics. |
| **Why REPLACE** | Footnote line must match **Deloitte’s official report title** on the cover/PDF. |
| **Alternatives** | (1) Deloitte summary page: `https://www.deloitte.com/global/en/issues/trust/progress-on-ai-in-the-boardroom-but-room-to-accelerate.html` (from chapter-01 web research). |

---

### `[^9]` — Eurostat, "AI in Enterprises", December 2025

| Field | Detail |
|--------|--------|
| **Claim** | EU enterprises using AI: **20%** (10+ employees), prior **13.5%**, large firms **55%**. |
| **Why cited** | `research/chapter-01-web-research.md` Finding 2 + Eurostat news release path. |
| **Why REPLACE** | Eurostat footnotes should use **release document + table code**, not a generic title. |
| **Alternatives** | (1) Eurostat news release linked in research: `https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2` (verify percentages in the release body). |

---

### `[^10]` — World Economic Forum, "Europe's AI adoption lag analysis", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Europe’s AI adoption lag as structural challenge. |
| **Why cited** | `research/chapter-01-web-research.md` Finding 3. |
| **Why REPLACE** | Need **exact story title** and date on weforum.org. |
| **Alternatives** | (1) `https://www.weforum.org/stories/2025/09/europe-ai-adoption-lag/` (from chapter-01 web research). |

---

### `[^11]` — BCG, "AI Radar", January 2026

| Field | Detail |
|--------|--------|
| **Claim** | e.g. **6×** sponsorship multiplier, **12×** top-5% odds, CEO-as-owner stats. |
| **Why cited** | `research/book-research-claude.md`, `research/ch12-readiness.md`, `research/ch14-a-leadership-decision.md` repeatedly cite **BCG AI Radar** for CEO/trailblazer statistics. |
| **Why REPLACE** | **"AI Radar"** must point to the **specific year’s bcg.com publication** (2025 vs 2026 editions differ). |
| **Alternatives** | (1) Search `bcg.com` for **"AI Radar 2026"** and use that report’s PDF. (2) If a number is not in Radar, **move** that number to **State of AI** or **Widening Value Gap** with verified tables. |

---

### `[^12]` — S&P Global Market Intelligence, "Outlook on Generative AI", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Rising abandonment of AI initiatives (often **42% vs 17%** style narrative in book research). |
| **Why cited** | `research/book-research-claude.md` bundles **S&P** with RAND/BCG as **failure-rate triangulation**. |
| **Why REPLACE** | Need the **exact S&P report title** and year; many figures circulate via **secondary summaries**. |
| **Alternatives** | (1) S&P Market Intelligence **original briefing** if licensed. (2) **Cite RAND** or **McKinsey** instead if you cannot access S&P primary. |

---

### `[^13]` — BCG, "The Widening AI Value Gap", October 2025

| Field | Detail |
|--------|--------|
| **Claim** | Small minority achieve value at scale; investment/upsell gap. |
| **Why cited** | Same BCG report family as ch01 (`[^2]`, `[^5]`). |
| **Why REPLACE** | Consolidate duplicate BCG Value Gap citations into **one** canonical footnote + PDF. |
| **Alternatives** | Same PDF as `[^2]`. |

---

### `[^15]` — Deloitte board governance (2nd edition), 2025

| Field | Detail |
|--------|--------|
| **Claim** | Board AI governance gap in ch02. |
| **Why cited** | Same Deloitte pulse as `[^7]`. |
| **Why REPLACE** | Match **exact edition title**; ch02 may need **page/figure** for "policies / every meeting" percentages. |
| **Alternatives** | Deloitte page as `[^7]`. |

---

### `[^17]` — McKinsey, "Superagency in the Workplace", January 2025

| Field | Detail |
|--------|--------|
| **Claim** | **91%** employee gen-AI use vs **1%** maturity-style gap (exact wording in ch02). |
| **Why cited** | McKinsey **workforce + gen AI** survey line is the standard home for adoption/maturity contrasts. |
| **Why REPLACE** | Verify **both numbers** in one McKinsey piece; if split across two surveys, **split footnotes**. |
| **Alternatives** | (1) McKinsey State of AI 2025 PDF. (2) Dedicated McKinsey **"Superagency"** article on mckinsey.com — use **that** URL. |

---

### `[^18]` — Writer / Workplace Intelligence, "State of AI at Work", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Policy non-compliance / generational splits in ch02. |
| **Why cited** | Vendor + Workforce Intelligence surveys are common for **shadow AI** stats. |
| **Why REPLACE** | Prefer **PDF report** from Writer or WI with **methodology appendix**. |
| **Alternatives** | (1) McKinsey on shadow AI / risk. (2) Gartner employee surveys if percentages align. |

---

### `[^19]` — McKinsey, "CEO Playbook for AI Transformations", June 2025

| Field | Detail |
|--------|--------|
| **Claim** | **6%** companies with meaningful domain-leader role. |
| **Why cited** | McKinsey CEO / transformation series often contains **role adoption** metrics. |
| **Why REPLACE** | Confirm **6%** appears in the cited article; **title must match** McKinsey’s headline. |
| **Alternatives** | (1) Same McKinsey article URL as `[^3]` if numbers live there. (2) BCG Radar if the statistic is actually from Radar. |

---

### `[^20]` — Gartner, "AI Maturity and Business Outcomes Survey", Q4 2024

| Field | Detail |
|--------|--------|
| **Claim** | **57%** vs **14%** trust/use across maturity bands. |
| **Why cited** | Gartner surveys are used in `research/ch13-measuring-what-matters.md` for **maturity vs duration** stats. |
| **Why REPLACE** | Gartner requires **exact survey name + n=**; often need **Gartner client** access. |
| **Alternatives** | (1) Public Gartner press release that contains the same percentages. (2) McKinsey State of AI for close-enough *directional* trust stats (edit text if needed). |

---

### `[^21]` — Cisco, "AI Readiness Index", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **>60%** European firms at earliest maturity (ch02). |
| **Why cited** | `research/ch4 - The Four Tiers of Transformation.md` references Cisco Readiness Index + Eurostat. |
| **Why REPLACE** | Cisco index may **not** label "earliest stages" the same way — **risk of category mismatch**. |
| **Alternatives** | (1) Cisco AI Readiness Index **methodology PDF** on cisco.com. (2) **Eurostat ICT usage** tables for simpler "adoption %" claims. |

---

### `[^22]` — Deloitte, "Tech Trends 2025", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Effort spent on data engineering / integration vs model (ch03). |
| **Why cited** | Deloitte Tech Trends commonly used for **integration tax** narratives. |
| **Why REPLACE** | Cite **chapter/page** from Deloitte report; title may be **"Tech Trends 2025"** but verify region. |
| **Alternatives** | (1) Gartner on data integration costs. (2) McKinsey on data readiness as bottleneck. |

---

### `[^23]` — Capgemini, "AI Agents in the Enterprise", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Agent deployment vs data readiness / "AI-ready data" minority. |
| **Why cited** | Capgemini Research Institute series is standard for **enterprise agent** surveys. |
| **Why REPLACE** | Use **Capgemini PDF** with **exact chart** for each percentage. |
| **Alternatives** | (1) Gartner Hype Cycle if claim is about **hype vs production**. |

---

### `[^24]` — PwC, "AI Agent Survey", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Majority of execs adopting agents; budget increases (ch03). |
| **Why cited** | PwC agent survey fits **agent adoption** percentages. |
| **Why REPLACE** | Confirm PwC **published** title (may differ slightly). |
| **Alternatives** | (1) McKinsey State of AI **agent** section. |

---

### `[^25]` — Gartner, "Hype Cycle for Artificial Intelligence", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Many agent projects predicted to fail without operating model (ch03). |
| **Why cited** | Hype Cycle supports **expectations vs delivery** narrative. |
| **Why REPLACE** | Gartner hype cycle is **paywalled** — public footnote should be **press release** + quote **Gartner’s wording** carefully. |
| **Alternatives** | (1) Gartner **public** press release for AI Hype Cycle 2025. |

---

### `[^27]` — BCG, "From Potential to Profit: Closing the AI Impact Gap", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **10/20/70** style effort split (ch03). |
| **Why cited** | BCG **10/20/70** is explicitly used across `research/` for org design. |
| **Why REPLACE** | Cite the **exact BCG publication** that states the rule (title varies). |
| **Alternatives** | (1) BCG **potential to profit** PDF on bcg.com. (2) Any BCG article that **defines** 10/20/70 with a footnote to original. |

---

### `[^29]` — Sarkar, SSRN, November 2025

| Field | Detail |
|--------|--------|
| **Claim** | **39%** output lift; experience vs junior effects (ch03). |
| **Why cited** | Academic working paper fits **fine-grained empirical** claims. |
| **Why REPLACE** | SSRN must be **exact paper ID**; verify **abstract vs your numbers**. |
| **Alternatives** | (1) Peer-reviewed version if published. (2) Different MIT/arxiv study if SSRN link unstable. |

---

### `[^30]` — Stanford / World Bank, "AI Impact on Work Productivity Survey", 2024

| Field | Detail |
|--------|--------|
| **Claim** | Legal trial **41%** productivity; **65–86%** time savings band (ch03). |
| **Why cited** | Research briefs often bundle **World Bank + Stanford** surveys for productivity ranges. |
| **Why REPLACE** | These numbers may come from **different** studies — **split** if needed. |
| **Alternatives** | (1) Cite each study separately with **one stat per footnote**. |

---

### `[^31]` — Allianz, "Project Nemo", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Direct quote from **Maria Janssen** on human responsibility. |
| **Why cited** | Fact-check attaches **company programme name** when quote is about a named initiative. |
| **Why REPLACE** | Quote should be tied to **Allianz official press/mediacenter** or **executive interview**, not training-site summaries. |
| **Alternatives** | (1) `https://www.allianz.com/en/mediacenter/news/articles/250205-smarter-claims-management-smoother-settlements.html` (check quote presence). (2) Allianz **storm / Nemo** article from `research/chapter-01-web-research.md`: `https://www.allianz.com/en/mediacenter/news/articles/251103-when-the-storm-clears-so-should-the-claim-queue.html` |

---

### `[^33]` — Germany, Works Constitution Act (BetrVG), 2021

| Field | Detail |
|--------|--------|
| **Claim** | Co-determination / consultation rules for AI (ch03). |
| **Why cited** | Legal footnotes often point to **statute** not a blog. |
| **Why REPLACE** | Use **official German law text** (BGBl) or **EUR-Lex** if translated; **year** may be wrong if citing consolidated law. |
| **Alternatives** | (1) gesetze-im-internet.de **BetrVG**. (2) EU policy explainer if claim is EU-level. |

---

### `[^34]` — Deutsche Telekom, "AI Guidelines", 2023

| Field | Detail |
|--------|--------|
| **Claim** | Co-created AI guidelines with works council (ch03). |
| **Why cited** | Named company document is appropriate for **single-company** practices. |
| **Why REPLACE** | Link to **Telekom press release or PDF** of AI manifesto / guidelines. |
| **Alternatives** | (1) Substitute a **neutral** source (industry association) if purpose is general European pattern. |

---

### `[^35]` — Nanterre Tribunal, February 2025

| Field | Detail |
|--------|--------|
| **Claim** | French court suspended AI project; daily penalties (ch03). |
| **Why cited** | Legal rulings require **docket/court identification**. |
| **Why REPLACE** | Add **case number**, **court**, **neutral legal database** link. |
| **Alternatives** | (1) French legal press with **primary court PDF** citation. |

---

### `[^36]` — Allianz, "EU AI Pact", November 2024

| Field | Detail |
|--------|--------|
| **Claim** | Allianz signed EU AI Pact (ch03). |
| **Why cited** | Commission **AI Pact** list is the authoritative proof. |
| **Why REPLACE** | Company PDF is optional; **Commission pledge list** is better as primary. |
| **Alternatives** | (1) `https://digital-strategy.ec.europa.eu/en/policies/ai-pact` + Commission pledge publications. |

---

### `[^37]` — BCG, "The Widening AI Value Gap", October 2025

| Field | Detail |
|--------|--------|
| **Claim** | Pilot / value capture failure pattern (ch04). |
| **Why cited** | Same BCG report cluster as ch01. |
| **Why REPLACE** | De-duplicate with `[^2]`/`[^5]` — one canonical BCG cite. |
| **Alternatives** | October PDF (chapter-01 web research). |

---

### `[^38]` — Huble, "AI Readiness Report", 2024

| Field | Detail |
|--------|--------|
| **Claim** | Leaders overestimate readiness vs reality (ch04). |
| **Why cited** | `research/ch4 - The Four Tiers of Transformation.md` uses **Huble** for **57% say ready / 8% are** style gap. |
| **Why REPLACE** | Huble’s **public** asset may be **2025** "AI Data Readiness Report" — **year mismatch** risk. |
| **Alternatives** | (1) `https://huble.com/ai-data-readiness-report` (verify percentages + year). (2) Gartner data readiness survey as backup. |

---

### `[^40]` — HBS / BCG, "Navigating the Jagged Technological Frontier", 2023

| Field | Detail |
|--------|--------|
| **Claim** | **758 consultants** study outcomes (ch04). |
| **Why cited** | Landmark BCG/HBS working paper — default cite for **frontier** study. |
| **Why REPLACE** | Use **original HBS Working Paper** or **official BCG PDF** with **exact stats** (your chapter may round). |
| **Alternatives** | (1) SSRN/HBS working paper link. |

---

### `[^41]` — Typeface, "Signal Report", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **61%** AI use remains individual / not collaborative (ch04). |
| **Why cited** | Vendor **Signal Report** used in research for **collaboration** stats. |
| **Why REPLACE** | Vendor reports need **PDF** and **methodology**; consider swapping to **neutral** survey. |
| **Alternatives** | (1) McKinsey State of AI on **adoption patterns**. (2) Gartner on collaboration platforms. |

---

### `[^42]` — Google, "Project Aristotle", 2016

| Field | Detail |
|--------|--------|
| **Claim** | Psychological safety as team effectiveness driver (ch04). |
| **Why cited** | Classic Google re:Work summary is the standard cite. |
| **Why REPLACE** | Prefer **Google re:Work** page URL + **Harvard Business Review** article if you need academic traceability. |
| **Alternatives** | (1) Google re:Work **Project Aristotle** page. |

---

### `[^44]` — Slack, "Workforce Index", Fall 2024

| Field | Detail |
|--------|--------|
| **Claim** | Permission / training multipliers for experimentation (ch04). |
| **Why cited** | Slack Workforce Index is a common **employee sentiment** source. |
| **Why REPLACE** | Confirm **6× / 19×** (or whatever your text says) appears in **that** edition. |
| **Alternatives** | (1) Microsoft Work Trend Index if Slack numbers cannot be verified. |

---

### `[^45]` — BearingPoint, "AI Adoption in the Enterprise", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **35%** with structured change management for managers (ch04). |
| **Why cited** | EU consultancies often provide **Europe-weighted** enterprise surveys. |
| **Why REPLACE** | Need **report PDF**; verify sample and geography. |
| **Alternatives** | (1) McKinsey State of AI on **change management**. |

---

### `[^46]` — Kore.ai case study

| Field | Detail |
|--------|--------|
| **Claim** | Wealth-management workflow metrics (ch04). |
| **Why cited** | `research/Global-Bank-Kore-AI-Agentic-Wealth-Management.md` supports Kore.ai **case** narrative. |
| **Why REPLACE** | Vendor case study should be **PDF** + **client-permitted** claims; otherwise label as **vendor-reported**. |
| **Alternatives** | (1) Kore.ai official case PDF. (2) Replace with **industry** benchmark if too promotional. |

---

### `[^47]` — Airbus / GitHub, "GitHub Copilot at Airbus", 2024

| Field | Detail |
|--------|--------|
| **Claim** | **10k engineers**, **40%** simulation cycle time improvement (ch04). |
| **Why cited** | GitHub customer story pattern fits **engineering productivity** claims. |
| **Why REPLACE** | Use **GitHub blog / Airbus joint** primary; verify **40%** wording. |
| **Alternatives** | (1) GitHub Copilot customer blog search **Airbus**. |

---

### `[^48]` — EY, "European AI Barometer", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **56%** profits/costs; **€6M** average impact (ch04). |
| **Why cited** | Big4 barometer surveys used for **EU-wide** averages. |
| **Why REPLACE** | EY must publish **exact question wording** for € and %. |
| **Alternatives** | (1) Eurostat + national stats if EY numbers are too aggregated. |

---

### `[^49]` — IDC, "AI Project Deployment Survey", 2024

| Field | Detail |
|--------|--------|
| **Claim** | **33 PoCs → 4 production** style funnel (ch04). |
| **Why cited** | IDC funnel ratios appear in multiple **industry summaries** — fact-check may have used **secondary citations**. |
| **Why REPLACE** | Find **IDC Doc #** or **public excerpt**; if only available via paywall, **soften** claim in text. |
| **Alternatives** | (1) Gartner on PoC abandonment. (2) McKinsey on scaling. |

---

### `[^50]` — McKinsey, "Agents for Growth", November 2025

| Field | Detail |
|--------|--------|
| **Claim** | Marketing / insurer conversion examples (ch04). |
| **Why cited** | McKinsey **agents** marketing use-cases. |
| **Why REPLACE** | Match **exact McKinsey title** and verify examples are **illustrative** not averages. |
| **Alternatives** | (1) McKinsey.com search **agents insurance marketing** publications. |

---

### `[^51]` — McKinsey, "Why Digital Trust Truly Matters", September 2022

| Field | Detail |
|--------|--------|
| **Claim** | Digital trust leaders outperform on revenue/EBIT (ch04). |
| **Why cited** | McKinsey trust work is standard for **trust → performance** bridge. |
| **Why REPLACE** | Confirm metrics and **definitions** of "leaders". |
| **Alternatives** | (1) Newer McKinsey trust work if definitions changed. |

---

### `[^52]` — McKinsey, "Rewired", 2023

| Field | Detail |
|--------|--------|
| **Claim** | Transformation captures only partial value (ch04). |
| **Why cited** | **Rewired** book is the canonical McKinsey digital transformation reference. |
| **Why REPLACE** | Prefer **book citation + page** for specific percentages; or cite **article summary** with URL. |
| **Alternatives** | (1) McKinsey **Rewired** excerpt on mckinsey.com. |

---

### `[^53]` — BCG, "AI Center of Excellence Research", 2024

| Field | Detail |
|--------|--------|
| **Claim** | **~37%** CoE prevalence (ch04). |
| **Why cited** | BCG CoE research notes in internal research memos. |
| **Why REPLACE** | Find **named BCG publication** containing **37%** (title may differ). |
| **Alternatives** | (1) Gartner on AI CoEs. (2) McKinsey on federated governance. |

---

### `[^54]` — BCG, "AI Radar", January 2026

| Field | Detail |
|--------|--------|
| **Claim** | Sponsors improve scaling odds (ch04). |
| **Why cited** | Same Radar line as `[^11]`. |
| **Why REPLACE** | Same as `[^11]` — **one** Radar footnote per chapter cluster. |
| **Alternatives** | bcg.com **AI Radar 2026** PDF. |

---

### `[^55]` — BCG, "The Widening AI Value Gap", October 2025

| Field | Detail |
|--------|--------|
| **Claim** | Adoption vs impact gap; pilots stuck (ch05). |
| **Why cited** | BCG Value Gap cluster. |
| **Why REPLACE** | Consolidate duplicates. |
| **Alternatives** | October PDF. |

---

### `[^56]` — Deloitte, "Tech Trends 2025", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Deployment effort in integration/data work (ch05). |
| **Why cited** | Same as `[^22]`. |
| **Why REPLACE** | Same as `[^22]`. |

---

### `[^57]` — Capgemini, "AI Agents in the Enterprise", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Minority have AI-ready data (ch05). |
| **Why cited** | Same as `[^23]`. |
| **Why REPLACE** | Capgemini PDF chart-level verification. |

---

### `[^58]` — McKinsey, "Rewired", 2023

| Field | Detail |
|--------|--------|
| **Claim** | Workflow redesign correlation with impact (ch05). |
| **Why cited** | Rewired supports **operating model** change. |
| **Why REPLACE** | Prefer **specific Rewired chapter** or **McKinsey article** with the exact statistic. |

---

### `[^61]` — Digital Bloom + Click-Vision (zero-click)

| Field | Detail |
|--------|--------|
| **Claim** | Zero-click / mobile / AI overview rates (ch06). |
| **Why cited** | `research/chapter-06p-web-research.md` explicitly lists **Digital Bloom + Click-Vision** for SEO/zero-click stats. |
| **Why REPLACE** | These are **industry blogs** — ok for colour, **not** for hard percentages without **Similarweb/Ahrefs** primary. |
| **Alternatives** | (1) `https://click-vision.com/zero-click-search-statistics` — then **cross-check** against Similarweb or Google IO data. (2) Bain article `[^62]` for **strategic** framing (not every %). |

---

### `[^62]` — Bain, "Goodbye Clicks…", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Bain quote on **"most consequential shift…"** (ch06). |
| **Why cited** | Bain marketing insights are used for **zero-click narrative**. |
| **Why REPLACE** | Link **exact Bain publication**; verify quote **verbatim**. |
| **Alternatives** | (1) Search `bain.com` + article title keywords. |

---

### `[^64]` — Medallia, personalization / CX

| Field | Detail |
|--------|--------|
| **Claim** | Brands with high AI personalisation → **2×** likelihood of **10%+** revenue growth (ch06). |
| **Why cited** | Vendor whitepaper / blog line fits **personalisation ROI**. |
| **Why REPLACE** | Prefer **Medallia PDF** or **third-party** retail study. |
| **Alternatives** | (1) McKinsey consumer AI personalisation reports. |

---

### `[^66]` — Gartner press release, August 2025

| Field | Detail |
|--------|--------|
| **Claim** | **40%** enterprise apps with task-specific agents by **2026** (ch06). |
| **Why cited** | Gartner press releases are used for **predictions**. |
| **Why REPLACE** | Must be **exact headline** + **Gartner ID**; predictions are easy to mis-quote. |
| **Alternatives** | (1) gartner.com newsroom search **"task-specific AI agents" August 2025**. |

---

### `[^67]` — BCG, "Agents Accelerate…", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **10/20/70** + redesign lift bands (ch07). |
| **Why cited** | BCG agent economics papers in internal research. |
| **Why REPLACE** | One BCG PDF should contain **all** banded percentages; otherwise **split**. |
| **Alternatives** | (1) bcg.com search **agents accelerate value**. |

---

### `[^70]` — ETUI, "Collective Bargaining and AI", 2025

| Field | Detail |
|--------|--------|
| **Claim** | EU social dialogue / collective bargaining on AI (ch07). |
| **Why cited** | ETUI is appropriate for **trade union** coverage. |
| **Why REPLACE** | Link **ETUI report PDF** and **table** for any **% unions** claims (case study duplicates statistics). |
| **Alternatives** | (1) Eurofound publications on AI and industrial relations. |

---

### `[^71]` — BCG, "AI Talent and Training", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Threshold hours for training + coaching; tiny fraction scaling upskilling (ch07). |
| **Why cited** | BCG talent reports map to **skills** chapter. |
| **Why REPLACE** | Verify **"5 hours"** (or similar) threshold inside BCG report; may actually be **McKinsey** elsewhere — **high mismatch risk**. |
| **Alternatives** | (1) McKinsey upskilling publications. (2) World Economic Forum Future of Jobs. |

---

### `[^72]` — CNBC / FT, Accenture promotions + tokens

| Field | Detail |
|--------|--------|
| **Claim** | Accenture ties promotions / advancement to AI usage and token consumption (ch07). |
| **Why cited** | Journalism footnote used when **internal HR policy** isn’t public as PDF. |
| **Why REPLACE** | Prefer **Accenture press release** or **official interview**; journalism is secondary. |
| **Alternatives** | (1) FT/CNBC article URL + date. (2) Accenture leadership blog if available. |

---

### `[^73]` — Harvard Data Science Review, "The Agent-Centric Enterprise", Winter 2026

| Field | Detail |
|--------|--------|
| **Claim** | Outcome-driven process redesign vs bolt-on (ch07). |
| **Why cited** | Academic outlet fits **agent-centric enterprise** framing. |
| **Why REPLACE** | Confirm article exists, **volume/issue**, and that **your statistics** are in that article (not confused with BCG). |
| **Alternatives** | (1) HDSR search on **hdsr.mitpress.mit.edu**. (2) Use BCG/McKinsey redesign stats instead if HDSR doesn’t contain the numbers. |

---

### `[^75]` — Gartner, "Data Readiness for AI", July 2024

| Field | Detail |
|--------|--------|
| **Claim** | Data readiness + abandonment risk (ch08). |
| **Why cited** | Gartner **Data Readiness** recurring theme; often used for **60% abandon** style claims in drafts. |
| **Why REPLACE** | Quote **exact Gartner stat** — many drafts mis-cite **"60% abandoned"**; verify year/edition. |
| **Alternatives** | (1) Gartner **press release** that matches the stat. |

---

### `[^76]` — Deloitte, "Trustworthy AI", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Governance → broader deployment / revenue effects (ch08). |
| **Why cited** | Deloitte Trustworthy AI reports bundle **ISO 42001** + outcomes. |
| **Why REPLACE** | Provide **Deloitte PDF** and verify **28% / 5%** (or whatever your text uses) inside. |
| **Alternatives** | (1) ISO/IEC 42001 official + separate outcome study. |

---

### `[^77]` — MIT Sloan, "GenAI Divide…", August 2025

| Field | Detail |
|--------|--------|
| **Claim** | **95%** P&L impact framing (ch09) tied back to NANDA/MIT work. |
| **Why cited** | Same underlying report as `[^1]`, but **correct public title**. |
| **Why REPLACE** | Align `[^77]` with `[^1]` — **one MIT cite** unless two different claims. |
| **Alternatives** | (1) MIT Sloan CISR **GenAI Divide** publication page / PDF. |

---

### `[^79]` — McKinsey, "Building the AI Muscle of Your Business Leaders", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Few senior leaders have technical background to steer AI (ch09). |
| **Why cited** | McKinsey leadership upskilling article family. |
| **Why REPLACE** | Match **exact article title** on mckinsey.com. |
| **Alternatives** | (1) McKinsey **Organization** blog search. |

---

### `[^80]` — Everworker AI, "Team Enablement…", 2026

| Field | Detail |
|--------|--------|
| **Claim** | **<50%** AI projects reach production; **8 month** prototype timelines (ch09). |
| **Why cited** | `research/ch08-value-capabilities-trust.md` and `research/ch13-measuring-what-matters.md` cite **Everworker** as a **supporting** benchmark for production rates. |
| **Why REPLACE** | Vendor blog citing **Gartner** second-hand — prefer **Gartner primary** or label **vendor summary**. |
| **Alternatives** | (1) Gartner press release cited in same research (`Survey Finds 45%...`) — verify n and timeframes. |

---

### `[^81]` — Lexology / EP, GDPR + AI Act overlap

| Field | Detail |
|--------|--------|
| **Claim** | **87%** high-risk cases need GDPR + AI Act overlap (ch09). |
| **Why cited** | Law-firm **Lexology** articles often quantify **overlap** for compliance decks. |
| **Why REPLACE** | Legal percentages must be **traceable** to named **survey** or **regulatory analysis** with methodology. |
| **Alternatives** | (1) EDPS/EC guidance. (2) Peer-reviewed law article. |

---

### `[^82]` — Gartner, "AI Maturity and Trust Survey", June 2025

| Field | Detail |
|--------|--------|
| **Claim** | Trust vs usage across maturity bands; project duration (ch09). |
| **Why cited** | `research/ch13-measuring-what-matters.md` references **Gartner June 2025** trust survey. |
| **Why REPLACE** | Use **official Gartner press release** for the **exact percentages** in your sentence. |
| **Alternatives** | (1) Public press release: match headline to your stats. |

---

### `[^83]` — Accenture / AWS / Stanford, "Responsible AI from Risk to Value", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Many paused AI projects due to risk (ch09). |
| **Why cited** | Big-brand **responsible AI** PDFs are common for **pause rates**. |
| **Why REPLACE** | Multi-sponsor PDFs: verify **page + question**; avoid duplicate counting. |
| **Alternatives** | (1) McKinsey risk survey. (2) Gartner on AI governance stalls. |

---

### `[^86]` — McKinsey, "European VC and AI Investment Report", 2024

| Field | Detail |
|--------|--------|
| **Claim** | EU VC vs US / spend gap (ch10). |
| **Why cited** | Internal research memos often shorthand **"European VC report"** to McKinsey **Europe AI opportunity** materials. |
| **Why REPLACE** | That **exact title** may not exist — use the **real McKinsey publication title**. |
| **Alternatives** | (1) `https://www.mckinsey.com/capabilities/quantumblack/our-insights/time-to-place-our-bets-europes-ai-opportunity` (common canonical page). (2) McKinsey MGI investment reports. |

---

### `[^87]` — Pew Research Center, "Global Trust in AI Governance", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Global adults trust EU more than US/China on AI regulation (ch10). |
| **Why cited** | Pew global attitudes surveys fit **cross-country trust** claims. |
| **Why REPLACE** | Pew question wording is sensitive — cite **exact survey wave** + **question**. |
| **Alternatives** | (1) pewresearch.org search **AI regulation EU trust**. |

---

### `[^88]` — Deloitte, "European Trust Survey", 2025

| Field | Detail |
|--------|--------|
| **Claim** | EU users want regulation to increase adoption (ch10). |
| **Why cited** | Deloitte consumer trust surveys for Europe. |
| **Why REPLACE** | Deloitte PDF + **sample** + **question**. |
| **Alternatives** | (1) Eurobarometer digital topics if you need public-sector neutrality. |

---

### `[^89]` — Accenture, "AI Achievers: Designing AI Responsibly", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **AI Achievers** revenue uplift vs peers (ch10/11). |
| **Why cited** | Accenture segmentation is a standard **Achievers** framework. |
| **Why REPLACE** | Match **Accenture report year** and **exact uplift %** (11% vs 50% claims differ across chapters — **must reconcile**). |
| **Alternatives** | (1) accenture.com search **AI Achievers**. |

---

### `[^90]` — Capgemini, "Rise of Agentic AI", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Consumers pay premium for safety / want stricter rules (ch10). |
| **Why cited** | Capgemini consumer surveys for **agentic AI** trust. |
| **Why REPLACE** | Cite **Capgemini PDF**; verify **countries** and **question**. |

---

### `[^91]` — Edelman, "Trust Barometer", 2026

| Field | Detail |
|--------|--------|
| **Claim** | Workforce trust / leadership transparency (ch10). |
| **Why cited** | Edelman Trust Barometer is standard for **employer trust** claims. |
| **Why REPLACE** | Edelman: use **global report + section**; don’t mix **special editions**. |
| **Alternatives** | (1) edelman.com trust barometer **2026** downloads. |

---

### `[^92]` — Auxilion, "EU AI Act Compliance Benefits Analysis", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Governance tooling market growth; productivity boost ranges (ch10). |
| **Why cited** | **`research/ch09-europes-distinctive-edge.md`** explicitly notes **Auxilion** productivity uplift ranges tied to governance tooling. |
| **Why REPLACE** | Consultancy blog is **weak** for hard economics — prefer **market research** (Gartner/IDC) for **market size**, and **independent** studies for **productivity**. |
| **Alternatives** | (1) Gartner **AI governance** market forecasts. (2) EU reports on compliance tooling demand. |

---

### `[^93]` — Eurostat / Accenture, "Nordic AI Adoption…", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Nordic adoption **35–42%** vs low scaling investment (ch10). |
| **Why cited** | **`research/ch09-europes-distinctive-edge.md`** mixes **Eurostat** + Nordic reports. |
| **Why REPLACE** | **Accenture+Eurostat** hybrid title is **not** a real single report — **split**: Eurostat for adoption %, separate source for spend. |
| **Alternatives** | (1) Pure Eurostat country tables. (2) Nordic State of AI 2025 if cited in research file. |

---

### `[^94]` — BCG, "AI Radar", January 2026

| Field | Detail |
|--------|--------|
| **Claim** | CEO ownership impact on success rates (ch11). |
| **Why cited** | `research/ch10-what-the-leaders-did.md` / leadership decision research uses **Radar** for sponsorship stats. |
| **Why REPLACE** | Same as `[^11]` — **one** Radar PDF; verify **wording** ("success rates" definitions). |

---

### `[^95]` — Klarna, "Customer Service Research", 2024

| Field | Detail |
|--------|--------|
| **Claim** | **86%** empathy vs speed for hard issues (ch11). |
| **Why cited** | Company **research** label is used when a stat is **Klarna-specific**. |
| **Why REPLACE** | Need **Klarna-published** research PDF or **blog** with methodology. |
| **Alternatives** | (1) Klarna press/newsroom search **customer research empathy**. (2) Academic CX research if Klarna number cannot be verified. |

---

### `[^96]` — Accenture, "AI Achievers…" (repeat)

| Field | Detail |
|--------|--------|
| **Claim** | **11% Achievers**, **50%** revenue growth difference (ch11). |
| **Why cited** | Same as `[^89]`. |
| **Why REPLACE** | **Must match** ch10 numbers — internal consistency check required. |

---

### `[^97]` — MIT Sloan, "GenAI Divide…", August 2025

| Field | Detail |
|--------|--------|
| **Claim** | Majority of implementations fail P&L test (ch12). |
| **Why cited** | Same MIT report cluster as `[^1]`/`[^77]`. |
| **Why REPLACE** | Align with `[^1]` single primary cite. |

---

### `[^98]` — S&P Global, "Outlook on Generative AI", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Rising abandonment / pilot purgatory (ch12). |
| **Why cited** | Same logic as `[^12]`. |
| **Why REPLACE** | Same as `[^12]`. |

---

### `[^99]` — Gartner, "Data Readiness for AI", July 2024

| Field | Detail |
|--------|--------|
| **Claim** | Data maturity minority; not ready at scale (ch12). |
| **Why cited** | Same as `[^75]`. |
| **Why REPLACE** | Same as `[^75]`. |

---

### `[^100]` — BCG, "AI at Work", 2024

| Field | Detail |
|--------|--------|
| **Claim** | Upskilling lag vs acknowledgement; change saturation (ch12). |
| **Why cited** | BCG workforce reports fit **upskilling** + **change saturation** claims. |
| **Why REPLACE** | Confirm **exact BCG title**; saturation stats may belong to **Gartner** or **McKinsey** instead — **verify**. |
| **Alternatives** | (1) Gartner on change saturation. |

---

### `[^101]` — Bain, "AI in Private Equity", 2025

| Field | Detail |
|--------|--------|
| **Claim** | PE budget split **93%** people/training; **2× ROIC**; **70%** funds with AI CoEs (ch12). |
| **Why cited** | Bain PE AI notes in internal playbooks. |
| **Why REPLACE** | Each number must come from **same Bain table**; otherwise split footnotes. |
| **Alternatives** | (1) bain.com publication search **private equity AI**. |

---

### `[^102]` — Cisco, "AI Readiness Index", 2025

| Field | Detail |
|--------|--------|
| **Claim** | **Pacesetters** minority; 3× tracking impact (ch13). |
| **Why cited** | `research/ch12-readiness.md` documents Cisco **Pacesetter** framing. |
| **Why REPLACE** | Use Cisco **methodology PDF**; verify **3×** statistic exactly. |
| **Alternatives** | (1) `https://www.cisco.com/c/en/us/solutions/artificial-intelligence/ai-readiness-index.html` |

---

### `[^103]` — MIT CISR, "Enterprise AI Maturity Model", 2024

| Field | Detail |
|--------|--------|
| **Claim** | Stage 2→3 inflection point; financial performance by stage (ch13). |
| **Why cited** | MIT CISR maturity models are standard for **stage economics**. |
| **Why REPLACE** | Need **CISR publication PDF** with figure cited. |
| **Alternatives** | (1) cisr.mit.edu search **enterprise AI maturity**. |

---

### `[^105]` — Gartner, "Data Readiness for AI", July 2024

| Field | Detail |
|--------|--------|
| **Claim** | Majority estimate data not AI-ready (ch13). |
| **Why cited** | Same as `[^75]`. |
| **Why REPLACE** | Same as `[^75]`. |

---

### `[^106]` — BCG, "Measuring AI Impact", 2025

| Field | Detail |
|--------|--------|
| **Claim** | ROI measured too early post-pilot (ch14). |
| **Why cited** | BCG measurement pieces fit **kill-too-early** narrative. |
| **Why REPLACE** | Exact BCG publication title + URL. |
| **Alternatives** | (1) McKinsey on measurement windows. |

---

### `[^108]` — BCG, "The Widening AI Value Gap", October 2025

| Field | Detail |
|--------|--------|
| **Claim** | Competitive separation metrics (ch15). |
| **Why cited** | `research/ch14-a-leadership-decision.md` ties competitiveness framing to **Widening Value Gap + Radar**. |
| **Why REPLACE** | Consolidate BCG citations; verify matches **latest** BCG edition. |
| **Alternatives** | October PDF + BCG press page. |

---

### `[^109]` — BCG, "AI Radar", January 2026

| Field | Detail |
|--------|--------|
| **Claim** | **Doubling AI spend 2026** (ch15). |
| **Why cited** | `research/ch14-a-leadership-decision.md` explicitly lists **BCG AI Radar Jan 2026** alongside CEO surveys. |
| **Why REPLACE** | Verify whether **doubling** is truly in Radar vs **CEO survey**; split if needed. |
| **Alternatives** | (1) BCG Radar PDF. |

---

### `[^110]` — PwC / EIT, "AI Jobs Barometer", 2025

| Field | Detail |
|--------|--------|
| **Claim** | Talent demand surge in DE/UK/IE (ch15). |
| **Why cited** | PwC Jobs Barometer fits **labour market** claims. |
| **Why REPLACE** | Confirm **EIT co-branding** is correct for that year (title may vary). |
| **Alternatives** | (1) pwc.co.uk **AI Jobs Barometer** download. |

---

### `[^111]` — PwC, "Global CEO Survey", 2026

| Field | Detail |
|--------|--------|
| **Claim** | Half of leaders: job stability; non-CEOs: resignation if AI strategy fails (ch15). |
| **Why cited** | `research/ch14-a-leadership-decision.md` references **PwC 29th Global CEO Survey, Jan 2026**. |
| **Why REPLACE** | Match **survey edition** (29th) and **exact question** for resignation finding. |
| **Alternatives** | (1) pwc.com **Global CEO Survey** microsite for Jan 2026. |

---

## Consistency warnings (cross-chapter)

These are **not** automatically wrong, but they are where **strict** editing usually catches issues:

- **BCG “Widening AI Value Gap”** appears many times (`[^2]`, `[^5]`, `[^13]`, `[^37]`, `[^55]`, `[^108]`) — consolidate to **one** canonical citation + PDF.
- **BCG “AI Radar”** appears many times (`[^11]`, `[^54]`, `[^94]`, `[^109]`) — same.
- **MIT “GenAI Divide / NANDA”** appears as `[^1]`, `[^77]`, `[^97]` — align titles and **do not double-count** the same study.
- **Accenture AI Achievers** appears as `[^89]` vs `[^96]` — reconcile **percentage** claims across chapters.

---

*This file is editorial instrumentation only. It does not change chapter text.*
