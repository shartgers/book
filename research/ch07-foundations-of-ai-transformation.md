# Chapter 7 Research: Foundations of the AI Transformation

> **Purpose:** Deep research synthesis for Chapter 7 — the Foundation layer (Data, Technology, Enablement) of the AI Transformation Framework. Covers readiness frameworks, five-pillar diagnostics, Value–Capability–Trust as a diagnostic lens, roadmap design, regulatory/ethical context, and the case for integrated (not isolated) transformation.
>
> **Relation to existing research:** Extends and complements `research/ai-readiness-framework.md`. New frameworks, statistics, and examples are added below; alignment or tension with that file is noted where relevant.

---

## 1. Readiness and Maturity Frameworks (2024–2026)

### 1.1 Cisco AI Readiness Index (2024–2025)

The most comprehensive publicly available benchmark. Surveys 8,000+ senior business and technology leaders across 30 markets using 49 distinct indicators.

**Six pillars:** Strategy, Infrastructure, Data, Governance, Talent, Culture.

**Four maturity levels:**

| Level | Score | Label |
|-------|-------|-------|
| Pacesetters | ≥86 | Fully prepared |
| Chasers | 61–85 | Moderately prepared |
| Followers | 31–60 | Limited preparedness |
| Laggards | 0–30 | Unprepared |

**Key findings (2024–2025):**
- Only **13–14% of organisations qualify as Pacesetters** — unchanged from 2023 to 2025.
- Readiness actually *declined* in 2024 across Infrastructure, Data, Governance, Talent, and Culture pillars despite 98% reporting increased urgency.
- Nearly **50% of respondents reported unmet expectations** from AI investments, despite allocating 10–30% of IT budgets to AI.
- **83% of companies plan to deploy AI agents**, yet most lack foundational readiness.
- Pacesetters are **3× more likely to track AI investment impact** (95% vs 32% overall) and 1.5× more likely to report profitability gains (90%+ vs ~60%).

**European data (2025):**
- Only **23% of EU organisations have robust GPU capacity**; 66% struggle to centralise data.
- Just **9% describe networks as flexible or adaptable**.
- Only **21% of EU organisations can detect or prevent AI-specific threats**.
- Western Europe scores 69.56 (2nd globally after North America at 82.60).
- Country scores: France 79.36, UK 78.88, Netherlands 77.23, Germany 76.90, Finland 76.48.
- **>60% of European firms remain at earliest readiness stages.**

*Source: Cisco AI Readiness Index 2024, 2025; cisco.com*

### 1.2 Gartner AI Maturity Model (2024–2025)

Five-level model assessing organisations across **seven pillars**: Strategy, Product, Governance, Engineering, Data, Operating Models, Culture.

**Five levels:**

| Level | Name | Description |
|-------|------|-------------|
| 1 | Planning/Beginning | Ad hoc, reactive, minimal investment |
| 2 | Emerging | Basic pilots, initial exploration |
| 3 | Developing | Established AI strategy, scalable solutions, measurable ROI |
| 4 | Advanced | AI-driven innovation as core strategy, significant automation |
| 5 | Leadership | AI fully embedded, continuous innovation |

**Key findings (Q4 2024):**
- High-maturity orgs (4.2–4.5) significantly outperform low-maturity (1.6–2.2).
- **45% of high-maturity orgs keep AI projects operational 3+ years** vs only 20% of low-maturity.
- **57% of high-maturity orgs report business unit trust in AI** vs 14% low-maturity.
- **63% of high-maturity orgs implement metrics** to quantify AI benefits.
- Data availability and quality remain the **primary barrier** across all maturity levels.
- **Gartner predicts: through 2026, organisations will abandon 60% of AI projects** unsupported by AI-ready data.

*Source: Gartner AI Maturity Model and Roadmap Toolkit; Gartner press releases 2025*

### 1.3 Microsoft Five-Stage Maturity Model (2024–2025)

**Five stages:**
1. **Exploration** — informal curiosity, unsanctioned pilots, shadow IT risk.
2. **Experimentation** — formal but siloed pilots (Copilot, AI Builder).
3. **Operationalisation** — first production-grade deployments, governance forming.
4. **Integration** — enterprise-wide scaling across functions.
5. **Transformation** — AI-driven enterprise, sustained and responsible.

Microsoft emphasises this as a **three-year journey**. The challenge is not technology but "architecting a sustainable foundation for enterprise-wide change." Microsoft Digital (internal IT) used this model to guide its own adoption and published lessons.

Microsoft also offers an **AI Readiness Wizard** assessment tool for organisations to gauge current state.

*Source: Microsoft InsideTrack Blog; Microsoft Cloud Blog 2024*

### 1.4 Deloitte AI Governance Maturity (2024–2025)

Three levels: **Basic → In Progress → Ready**, assessed across 12 indicators and five pillars among ~900 senior leaders.

**Trustworthy AI™ framework — seven dimensions:**
1. Transparent and Explainable
2. Fair and Impartial
3. Robust and Reliable
4. Respectful of Privacy
5. Safe and Secure
6. Responsible
7. Accountable

**Impact data:** Organisations with better AI governance deploy AI in **3 additional business areas**, have **28% more staff using AI**, and report **~5% higher revenue growth**.

*Source: Deloitte Trustworthy AI™; Deloitte Insights 2025*

### 1.5 ServiceNow Enterprise AI Maturity Index (2025)

Measures on a 0–100 scale across five pillars: AI Strategy & Leadership, Workflow Integration, Talent & Workforce, AI Governance, Realising Value.

**Key findings:**
- Average maturity scores **dropped 9 points year-over-year**.
- **Fewer than 1% of executives scored above 50** on a 100-point scale.
- 8 in 10 Pacesetters have AI reskilling programmes vs 54% of non-Pacesetters.
- Half of Pacesetters have the right talent vs 29% of others.
- **55% of Pacesetters report improved gross margins** vs 22% of non-Pacesetters.
- Estimated **$113 billion in total gross margins** if all Forbes Global 2000 matched Pacesetter performance.

*Source: ServiceNow Enterprise AI Maturity Index 2025*

### 1.6 Comparative Alignment with Book's Five Pillars

| Book Pillar | Cisco | Gartner | Microsoft | Deloitte | ServiceNow |
|-------------|-------|---------|-----------|----------|------------|
| Product & Strategy | Strategy | Strategy, Product | Exploration → Transformation stages | (within governance) | AI Strategy & Leadership |
| People & Skills | Talent, Culture | Culture, Operating Models | (cultural factors) | Fair & Impartial, Accountable | Talent & Workforce |
| Process & Governance | Governance | Governance | Operationalisation stage | All 7 Trustworthy AI dimensions | AI Governance |
| Technology & Infrastructure | Infrastructure | Engineering | Integration stage | Robust & Reliable, Safe & Secure | Workflow Integration |
| Data & Context | Data | Data | (within all stages) | Respectful of Privacy | (within Realising Value) |

**Key tension with existing research:** `ai-readiness-framework.md` uses five pillars (Product, People, Process, Technology, Data) aligned with Cisco's six pillars but with Culture folded into People. External frameworks increasingly add explicit "Culture & Change" and "Ecosystem & Partnerships" as separate dimensions. Consider whether Chapter 7 should acknowledge these as sub-dimensions or keep the five-pillar simplicity for CEO readers.

---

## 2. Five Pillars in Diagnostic Form

### 2.1 Product & Strategy Readiness

**What to assess:**
- Is AI explicitly part of corporate strategy and product roadmap?
- Are use cases prioritised by expected business impact (ROI, customer value)?
- Are there measurable targets tying AI to business outcomes?

**Diagnostic criteria from frameworks:**
- Gartner: "Strategic Alignment & Business Objectives" is the first pillar; asks whether AI projects are linked to measurable performance targets.
- Cisco: 77% of Pacesetters have finalised AI use cases vs <40% of Followers.
- McKinsey: Half of high performers intend to use AI to *transform* their businesses, not just optimise existing ones.

**Common blind spot:** Organisations rate strategy highly ("we have an AI strategy") but lack the operational detail (use-case pipeline, business-case economics, sequenced priorities) to execute.

### 2.2 People & Skills Readiness

**What to assess:**
- Executive sponsorship and AI literacy at board/C-suite level.
- Availability of AI talent (data scientists, ML engineers, prompt engineers).
- Breadth and depth of upskilling programmes.
- Cultural readiness for AI-augmented work.

**Key statistics:**
- Only **6% of companies have begun meaningful AI upskilling** (BCG 2024, 1,400 C-suite execs).
- **66% of C-suite leaders expressed dissatisfaction** with upskilling progress.
- **62% cite talent and skills shortages** as their biggest challenge.
- Only **51% of frontline employees regularly use AI** vs 75%+ of leaders/managers.
- **5+ hours of training** plus in-person coaching significantly improves adoption (BCG 2025).
- Companies are **missing up to 40% of AI productivity gains** due to talent strategy gaps (EY European AI Barometer 2025).
- Europe faces **up to 12 million occupational transitions by 2030** — double the pre-pandemic pace (McKinsey 2024).

**European talent landscape:**
- EY European AI Barometer 2025 shows improving workforce sentiment ("from concerns to confidence") but persistent gaps in structured training.
- McKinsey: demand rising for technological, critical thinking, creativity, and training skills — all currently in short supply across Europe.

### 2.3 Processes & Governance Readiness

**What to assess:**
- Workflow redesign for AI integration (not just bolting AI onto legacy processes).
- Governance structures: policies, risk management, compliance checks, stage gates.
- Link to EU AI Act requirements (risk classification, human oversight, documentation).
- Internal controls: bias checks, impact assessments, audit trails.

**Key statistics:**
- Only **21% of organisations have fundamentally redesigned at least some workflows** for AI (McKinsey 2025).
- **Workflow redesign has the biggest effect** on generating EBIT impact from gen AI (McKinsey 2025).
- Only **18% of European organisations report being highly prepared** in AI risk and governance (Deloitte/EY surveys).
- Among German organisations, just **36% report being well-prepared for the EU AI Act**; 52% fear regulation will restrict innovation (Deloitte 2025).
- **70% of enterprise AI transformations fail** due to inadequate change management and governance frameworks rather than technical limitations (Augment Code 2025).

**Common blind spot:** Over-rating technology readiness while under-rating governance. Organisations often have the models and platforms but lack the review processes, risk frameworks, and decision rights to deploy responsibly.

### 2.4 Technology & Infrastructure Readiness

**What to assess:**
- Cloud/on-prem platforms, compute capacity (GPUs), networking.
- ML platforms, APIs, integration architecture.
- MLOps tooling: version control, CI/CD, model monitoring.
- Security posture for AI-specific threats.
- Build vs buy readiness.

**Key statistics:**
- Only **21% of organisations have adequate GPU capacity** (Cisco 2024).
- **AI Infrastructure Debt** is now a recognised risk: the accumulation of gaps, shortcuts, and deferred upgrades in compute, networking, data management, security, and talent that compounds as companies rush to deploy AI (Cisco 2025).
- In the EU: 66% struggle to centralise data, 9% have flexible networks, 21% can detect AI-specific threats (Cisco 2025).
- **98% of Pacesetters design infrastructure for future demands** vs peers who build for current needs only.

**"AI Infrastructure Debt" concept (new from Cisco 2025):** The modern evolution of technical debt. Silent accumulation of compromises, deferred upgrades, and underfunded architecture that erodes AI value over time. This is especially acute in Europe where legacy infrastructure and fragmented data landscapes are prevalent. This is a strong concept for the book — mirrors the "Foundation" layer message perfectly.

**Scoring caution:** Frameworks risk over-weighting technology because it is the most visible and measurable dimension. Chapter 7 should emphasise that technology without data, people, and governance is necessary but not sufficient.

### 2.5 Data & Context Readiness

**What to assess:**
- Data quality, completeness, freshness.
- Data governance: catalogues, metadata, lineage, ownership.
- Data integration: siloed vs centralised, real-time vs batch.
- "AI-ready data" criteria: labelled, accessible, governed, contextualised.

**Key statistics:**
- **63% of organisations lack AI-ready data practices** (Gartner, July 2024, 1,203 data management leaders).
- **Fewer than 1 in 5 organisations consider themselves data-ready** (WEF 2026).
- **Gartner predicts 60% of AI projects will be abandoned** through 2026 due to lack of AI-ready data.
- **42% of enterprises report more than half of AI initiatives delayed, underperformed, or failed** primarily due to data readiness (Fivetran 2024).
- **68% of companies with less than half data centralised** report lost revenue opportunities from AI delays (Fivetran 2024).
- Mature data practices deliver **3.2× higher ROI on AI investments** (Agentic AI Solutions 2025).

**Cross-pillar dependencies:** Data readiness is the most critical dependency. Without it, models are "blind"; without governance, they are "untrustworthy"; without people who understand the data, they are "misapplied." The diagnostic must score data harshly and honestly — it is the pillar most likely to be under-invested.

---

## 3. Value–Capability–Trust as a Diagnostic Lens

### 3.1 Using the Three Lenses for Readiness Assessment

The Value–Capability–Trust framework (Ch 8) can serve as a diagnostic overlay on the five pillars:

| Lens | What it asks | Pillar mapping |
|------|-------------|----------------|
| **Value** | Where can we create value? What is the pipeline of use cases and their expected impact? | Product & Strategy, Data & Context |
| **Capability** | Do we have the people, process, and technology to deliver? | People & Skills, Technology & Infrastructure, Processes & Governance |
| **Trust** | Can we govern, comply, and maintain stakeholder confidence? | Processes & Governance, Data & Context |

### 3.2 Presenting the Three-Lens View to the Board

The three lenses translate technical readiness into language boards understand:

- **Value:** "We have identified 12 use cases worth an estimated €X million in annual impact. Seven are ready to pilot; five require data or capability work first."
- **Capability:** "We are Level 2 on the maturity scale. Our gaps are in data integration (critical), talent depth (urgent), and workflow redesign (important). Here is the investment needed to reach Level 3 within 12 months."
- **Trust:** "Three of our seven priority use cases are classified as high-risk under the EU AI Act. We need governance structures, impact assessments, and human oversight mechanisms in place before August 2026."

### 3.3 Handling Tensions

Common tension patterns and how to prioritise gap-closing:

| Tension | Example | Recommended action |
|---------|---------|-------------------|
| High Value + Low Capability | Strong business case for AI in customer service, but no ML ops pipeline | Invest in capability; defer full deployment until foundation is ready |
| High Value + Low Trust | Profitable use case in HR screening, but high regulatory risk | Build governance first; compliance is non-negotiable under EU AI Act |
| High Capability + Low Value | Technical team has built sophisticated models but no clear business case | Redirect capability toward value-creating use cases; avoid "technology in search of a problem" |
| Low Trust across all | Organisation has no AI governance, no ethical framework, no compliance mapping | Foundation phase must prioritise trust infrastructure before any scaled deployment |

**Evidence supporting this approach:**
- McKinsey (2025): CEO oversight of AI governance is the element most correlated with higher EBIT impact (28% of orgs have this, and they significantly outperform).
- Gartner (Q4 2024): 57% of high-maturity orgs report business-unit trust in AI vs 14% low-maturity — trust is a leading indicator of sustainable value.
- Deloitte (2025): Better AI governance → 3 more business areas using AI, 28% more staff engagement, ~5% higher revenue growth.

---

## 4. From Diagnostic to Roadmap

### 4.1 Turning Readiness Scores into a Phased Roadmap

**Step 1 — Baseline and gap analysis:**
- Run the diagnostic across all five pillars × three lenses.
- Score each dimension on a 1–5 maturity scale.
- Identify the largest gaps between current state and the minimum required for first AI deployments.

**Step 2 — Prioritise by dependency and impact:**
- Data and governance are prerequisite pillars — score these first and harshly.
- Technology without data is wasteful; use cases without governance are risky.
- Sequence: (1) data foundations, (2) governance and trust, (3) technology and infrastructure, (4) people and skills, (5) strategy and product pipeline.
- Adjust sequencing based on where the organisation's largest gaps are.

**Step 3 — Design phases with milestones:**

| Phase | Focus | Typical duration | Example milestones |
|-------|-------|------------------|--------------------|
| **Foundation** (Phase 1) | Data, governance, initial skills | 3–6 months | Data catalogue live, AI policy approved, EU AI Act risk mapping complete, 100% leadership AI literacy |
| **Activation** (Phase 2) | First pilots, CoE setup, workflow redesign | 3–6 months | 3 pilots in production, CoE operational, first workflow redesigned, initial KPIs tracked |
| **Scale** (Phase 3) | Enterprise-wide rollout, agentic workflows | 6–12 months | 10+ use cases live, workforce upskilling at >50% completion, governance embedded, EBIT impact measurable |

**Step 4 — Assign ownership and budget:**
- Roadmap owner: CEO or designated transformation lead (CDO/CTO/CAO).
- McKinsey finding: CEO governance oversight is the single element most correlated with EBIT impact.
- CoE (Centre of Excellence) as operational hub for execution, standards, and best practices.
- Budget: EU AI Risk estimates €50K–€200K for SMEs, €200K–€1M for mid-size, €1M+ for enterprise (compliance alone).

### 4.2 Readiness KPIs (Not Just Project KPIs)

A critical distinction: foundation KPIs measure *organisational readiness* to absorb and scale AI, not just individual project outcomes.

**Foundation-level KPIs:**

| Category | Example KPIs |
|----------|-------------|
| **Data readiness** | % of data assets catalogued, % AI-ready (labelled, governed, accessible), data quality score, time-to-data for new use cases |
| **Governance maturity** | Number of governed use cases, % high-risk use cases with completed impact assessments, EU AI Act compliance score |
| **Workforce literacy** | % leadership AI-literate, % workforce trained (5+ hours), adoption rate (% regularly using AI tools) |
| **Technology foundation** | Infrastructure utilisation rate, MLOps pipeline coverage, mean time to deploy a new model, security posture score |
| **Strategic alignment** | Number of use cases in pipeline, % linked to measurable business outcomes, portfolio review cadence |
| **Value realisation** | % pilots graduating to production, EBIT impact attributable to AI, cost avoidance from automation |

**Evidence:**
- Pacesetters (Cisco 2025): 95% track and measure AI investment impact vs 32% overall.
- Gartner (2024): 63% of high-maturity orgs implement metrics to quantify AI benefits.
- ServiceNow (2025): fewer than 1% score above 50 on maturity — measurement itself is a rare capability.

### 4.3 EU AI Act Deadlines as Fixed Milestones

The regulatory timeline creates non-negotiable milestones for any AI roadmap in Europe:

| Deadline | Requirement | Roadmap implication |
|----------|-------------|---------------------|
| Feb 2025 (passed) | Prohibited AI systems banned; AI literacy training required | Immediate: ensure staff training and audit for prohibited uses |
| May 2025 (passed) | Transparency obligations | Ensure AI-generated content is labelled; user disclosure in place |
| Aug 2025 | General-purpose AI model requirements | Documentation, copyright compliance, incident reporting for foundation models |
| Sep 2025 | Systemic risk management for GPAI | Risk frameworks for large models |
| **Aug 2026** | **Full high-risk AI system compliance** | Impact assessments, quality management, risk management, data governance, transparency, human oversight, accuracy testing |

These dates should appear as fixed milestones on any European AI transformation roadmap. The August 2026 deadline is the critical "must-be-ready-by" date for high-risk use cases.

### 4.4 Roadmap Ownership

**Who owns the roadmap:**
- **CEO** — ultimate accountability, governance oversight, strategic direction. McKinsey: CEO oversight most correlated with EBIT impact.
- **CDO/CTO/CAO** — operational ownership of data, technology, and AI platforms.
- **CoE (Centre of Excellence)** — execution hub, standards, best practice dissemination, pilot management.
- **CHRO** — workforce strategy, upskilling, culture change.
- **CLO/DPO** — regulatory compliance, EU AI Act readiness, ethical framework.

**Connection to strategic planning:** The AI roadmap should integrate with the annual strategic planning and budget cycle, not run as a separate workstream. Quarterly reviews with the ExCo ensure alignment and course correction.

---

## 5. Regulatory and Ethical Context

### 5.1 EU AI Act as a Foundation Input

The EU AI Act creates a risk-based compliance regime that directly shapes what "ready" looks like:

**Risk classification (four tiers):**
1. **Unacceptable risk** — banned (social scoring, real-time biometric surveillance with exceptions).
2. **High risk** — strict requirements (finance, HR, critical infrastructure, health, education).
3. **Limited risk** — transparency obligations (chatbots, AI-generated content).
4. **Minimal risk** — no specific requirements.

**High-risk compliance requirements (by Aug 2026):**
- Risk management system
- Data governance practices
- Technical documentation
- Record-keeping and logging
- Transparency and information provision
- Human oversight mechanisms
- Accuracy, robustness, and cybersecurity testing
- Quality management system

**Key implication:** Any use case classified as high-risk triggers a *mandatory* foundation-readiness requirement across data governance, technical documentation, human oversight, and risk management. The diagnostic must flag these use cases and ensure the foundation supports compliance.

**Pre-existing system exemption:** AI systems deployed before August 2026 only need to comply if they undergo "significant changes in design" after that date. However, new deployments must be compliant from day one.

### 5.2 Trustworthy AI Frameworks

Multiple frameworks define what "trustworthy" means in practice:

| Framework | Key dimensions |
|-----------|---------------|
| **EU High-Level Expert Group** | Lawful, Ethical, Robust; human oversight, privacy, transparency, fairness, well-being, accountability |
| **NIST AI RMF 1.0** (2023) | Voluntary; addresses risks to individuals, orgs, society; Playbook, Roadmap, and Crosswalks for implementation |
| **NIST Generative AI Profile** (AI-600-1, July 2024) | Extension for gen AI risks: hallucination, bias, misuse, IP issues |
| **ISO/IEC 42001:2023** | World's first certifiable AI management system standard; covers policy, risk management, data governance, lifecycle controls, transparency, performance evaluation |
| **Deloitte Trustworthy AI™** | 7 dimensions: transparent, fair, robust, privacy-respecting, safe, responsible, accountable |
| **Microsoft Responsible AI** | Fairness, reliability, safety, privacy, inclusiveness, transparency, accountability |

**ISO 42001 as a practical tool:** The first international *certifiable* standard for AI management. Applies to orgs of all sizes; covers ethical considerations, bias management, safety, security, and misuse prevention. Certification is voluntary but increasingly valued by regulators and customers. Strong fit for the "Foundation" layer — provides a concrete governance framework.

### 5.3 Sector-Specific Regulatory Dimensions

Beyond the AI Act, specific sectors face additional readiness requirements:

- **Financial services:** DORA (Digital Operational Resilience Act), MiFID II algorithmic trading rules, EBA/EIOPA guidelines on AI in insurance/banking.
- **Healthcare:** Medical Device Regulation (MDR) for AI diagnostics, EHDS (European Health Data Space).
- **Critical infrastructure:** NIS2 Directive cybersecurity requirements.
- **Public sector:** Algorithmic transparency requirements, procurement rules for AI.

The diagnostic should include a sector-specific compliance checklist as an overlay on the standard five pillars.

---

## 6. Avoiding "Deploy in Isolation"

### 6.1 The Pilot Purgatory Crisis

The data is stark:
- **88–90% of companies use AI** in at least one function (McKinsey 2025).
- But only **6% report meaningful bottom-line impact** (McKinsey 2025).
- **60%** evaluate AI tools → **20%** implement pilots → only **5%** reach production with measurable P&L impact — a **92% attrition rate** from evaluation to production.
- Nearly **8 in 10 companies report no significant bottom-line impact** despite gen AI adoption — McKinsey calls this the "gen AI paradox."
- **95% of enterprise AI initiatives deliver zero measurable ROI** (ServiceNow/Augment Code surveys).

### 6.2 Why Isolated Pilots Fail

Five failure patterns (Augment Code / Duvo.ai analysis, 2025):
1. **Single-system solutions** ignoring cross-system workflows.
2. **No governance or audit trails** built in from day one.
3. **Hidden maintenance costs** consuming 60% of total spend.
4. **18-month implementation cycles** outlasting business relevance.
5. **Misalignment** between deployment and value creation.

The root cause: **technology-first thinking without business context**. Organisations chase "AI projects" instead of solving well-scoped business problems. The fix is organisational, not technological.

**BCG's value-creation breakdown (2025):**
- **70% of AI value comes from people, processes, and change management.**
- Only **10% from algorithms.**
- Only **20% from technology infrastructure.**

This directly supports the book's thesis that "AI transformation is really organisational transformation."

### 6.3 What "Absorb and Act on AI" Means

Successful organisations (the 5–6% that achieve value at scale) share these characteristics:
- **Start with business problems**, not technology — every use case tied to measurable outcomes.
- **Deploy in weeks, not years** — target production value over proof-of-concept.
- **Build governance into day one** — not retrofitted after deployment.
- **Orchestrate across systems** — AI integrated into workflows, not siloed.
- **Redesign workflows** — 21% have done this, and they see the biggest EBIT impact (McKinsey 2025).
- **Enable business users while maintaining IT governance** — democratise access, centralise standards.

### 6.4 How Diagnostics Prevent Isolation

Structured diagnostics have been used to stop or redirect projects:
- **"Not ready on data"**: Organisation discovers 63% of data is not AI-ready; redirects investment from model building to data platform work (common finding; Gartner).
- **"Not ready on trust"**: High-value HR screening use case flagged as high-risk under EU AI Act; governance foundation built before deployment.
- **"Not ready on people"**: Only 6% meaningful upskilling; roadmap prioritises workforce training before scaling.
- **"Not ready on process"**: Only 21% have redesigned workflows; transformation paused to redesign core processes first.

**Evidence that diagnostics improve outcomes:**
- Pacesetters (who by definition have mature, balanced readiness) are **3× more likely to measure AI impact** and **1.5× more likely to report profitability gains**.
- Gartner: high-maturity orgs keep AI projects operational **2.25× longer** (45% vs 20% at 3+ years).
- Mature data practices deliver **3.2× higher ROI** on AI investments.
- **Expert-guided change management reduces AI failures by 40%** (Agentic AI Solutions analysis).

### 6.5 Connection to the Book's Playbook (Ch 11)

The diagnostic should run **before or as the first step of the Foundation phase** (Ch 11's three-phase model: Foundation → Activation → Scale).

- If the diagnostic reveals critical gaps (e.g., data not AI-ready, no governance), the Foundation phase must *close these gaps first* before any pilot activation.
- If the diagnostic shows reasonable readiness, some Foundation and Activation activities can run in parallel (e.g., data platform upgrade alongside first pilot).
- The diagnostic should be **repeated** at the end of each phase as a progress check, feeding updated scores into Ch 13's measurement framework.

---

## 7. Key Concepts for Chapter 7

### 7.1 AI Infrastructure Debt (New Concept from Cisco 2025)

The accumulation of gaps, trade-offs, shortcuts, and lags in compute, networking, data management, security, and talent that compounds as companies rush to deploy AI. The modern evolution of technical debt — silent, compounding, and value-destroying.

**Why this matters for the book:** This concept gives a name to the failure to build proper foundations. It is the *cost* of skipping the Foundation layer. European companies are particularly exposed: legacy infrastructure, fragmented data, regulatory complexity, and talent scarcity all accelerate infrastructure debt.

**Recommendation:** Use "AI Infrastructure Debt" as a named concept in Chapter 7 to make the case for investing in foundations before (or alongside) scaling.

### 7.2 The Readiness Paradox

98% of leaders report increased urgency to deploy AI, but readiness *declined* (Cisco 2024). 88% use AI, but only 6% see bottom-line impact (McKinsey 2025). The paradox: urgency drives premature deployment, which drives failure, which drives more urgency.

The diagnostic breaks this cycle by providing an objective, evidence-based view of what is actually ready and what is not.

### 7.3 The 70/10/20 Rule (BCG 2025)

70% of AI value comes from people, processes, and change management. 10% from algorithms. 20% from technology. This directly supports the book's emphasis on the Foundation layer encompassing Data, Technology, *and Enablement* (culture, skills, toolbox).

### 7.4 The CEO Governance Imperative

CEO oversight of AI governance is the single element most correlated with higher EBIT impact from AI (McKinsey 2025). Only 28% of organisations have this. This connects to Ch 2 (Leadership Is Not Optional) and reinforces that Foundation readiness is a *leadership* responsibility, not a technology department task.

---

## 8. Source Summary

| Source | Year | Key contribution |
|--------|------|------------------|
| Cisco AI Readiness Index | 2024, 2025 | 6-pillar framework, Pacesetter data, EU benchmarks, AI Infrastructure Debt concept |
| Gartner AI Maturity Model | 2024–2025 | 5-level/7-pillar model, data readiness warnings, 60% project abandonment prediction |
| Microsoft Five-Stage Maturity | 2024 | Staged adoption model, three-year journey framing |
| Deloitte Trustworthy AI | 2024–2025 | 7-dimension trust framework, governance-value link |
| ServiceNow AI Maturity Index | 2025 | Maturity decline data, Pacesetter vs non-Pacesetter gap, $113B opportunity estimate |
| McKinsey State of AI | 2025 | Gen AI paradox, workflow redesign impact, CEO governance correlation, 8-in-10 no impact |
| McKinsey Future of Work (Europe) | 2024 | 12M European occupational transitions by 2030 |
| BCG AI at Work / Upskilling | 2024–2025 | 6% meaningful upskilling, 70/10/20 value split, 5-hour training threshold |
| EY European AI Barometer | 2025 | 40% productivity loss from talent gaps, European workforce sentiment |
| EU AI Act (Regulation 2024/1689) | 2024–2026 | Risk classification, compliance timeline, high-risk requirements |
| NIST AI RMF 1.0 / Gen AI Profile | 2023–2024 | Voluntary trust framework, gen AI risk extensions |
| ISO/IEC 42001:2023 | 2023 | First certifiable AI management system standard |
| Fivetran Data Readiness Report | 2024 | 42% initiative failure rate, data centralisation impact |
| WEF Data Readiness | 2026 | <20% consider themselves data-ready |
| Umbrex AI Diagnostic Framework | 2025 | 10-domain diagnostic model, evidence-based assessment criteria |
| Various (Duvo.ai, Augment Code, Medium) | 2025–2026 | Pilot purgatory data, 92% attrition rate, failure patterns |

---

## 9. Alignment Notes with Existing Research

**Confirms `ai-readiness-framework.md`:**
- Five pillars (Product, People, Process, Technology, Data) remain well-supported by external frameworks.
- Value/Capability/Trust as diagnostic lenses aligns with how Pacesetters operate.
- EU AI Act timeline and trustworthy AI principles are reinforced with specific compliance deadlines.
- Roadmap phasing (quick wins → foundations → scale) mirrors best practice.

**Extends `ai-readiness-framework.md`:**
- Adds AI Infrastructure Debt as a named concept and risk.
- Adds the "gen AI paradox" / "readiness paradox" as a framing device.
- Adds the 70/10/20 rule (BCG) as evidence for the Enablement component.
- Adds specific European data (Cisco EU stats, EY Barometer, McKinsey European labour market).
- Adds ISO 42001 as a certifiable governance standard.
- Adds ServiceNow maturity decline data (maturity actually *falling* despite investment).
- Adds detailed failure-pattern analysis for pilot purgatory.
- Adds specific diagnostic-to-roadmap methodology with phases, milestones, KPIs.

**Tensions to resolve:**
- External frameworks increasingly use 7–10 dimensions; the book uses 5 pillars. Recommendation: keep 5 for simplicity but acknowledge that Culture and Ecosystem are embedded within them.
- Some frameworks (Gartner, ServiceNow) show maturity *declining* despite investment — this challenges a linear "assess → improve → scale" narrative. The book should address this honestly: readiness is not a one-time gate but a continuous practice.
