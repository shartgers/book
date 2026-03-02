# Research Brief — Chapter 13 — Measuring What Matters

**Chapter purpose:** Governance, KPIs, measurement, financials, and board accountability. How CEOs can see and drive real progress and avoid "pilot purgatory." Not a framework layer.
**Word budget:** 6% of book (~2,700 words at 45k)
**Key audiences:** European CEOs of mid-to-large organisations; sceptical, data-driven, time-poor.

---

## 1. KPIs That Reveal Real Progress

Evidence supporting the chapter's argument that most organisations measure the wrong things — or nothing at all — and that a structured KPI framework across four categories (Financial, Operational, Adoption, Strategic) is essential for CEO-level visibility.

---

### 1.1 The measurement gap — most companies don't track AI ROI at all

**Claim:** Only 23% of enterprises actively measure AI ROI, despite 78% using AI in at least one function. The gap between deployment and measurement is the single largest blind spot in enterprise AI.
**Source:** Second Talent / enterprise survey analysis, "How Enterprises Are Measuring ROI on AI Investments in 2026," 2026; Dima AI, "How to Measure AI ROI: The 2026 Reality Check," 2026.
**Key details:** Early AI pilots in 2023 reported 31% returns, but as projects scaled, ROI dropped to 7% by 2025 — below most companies' cost-of-capital hurdle rates. This "ROI collapse" is partly a measurement artefact: early pilots cherry-pick use cases; scaling exposes hidden costs (compliance reviews, model retraining, infrastructure, governance overhead) that exceed initial expectations by 40–60%. Organisations with structured ROI measurement achieve **5.2× higher confidence** in AI investments.
**Use for:** Opening hook — the measurement crisis; connect to the "95% failure" argument in Ch 1.

---

### 1.2 Financial KPIs — cost savings, revenue impact, ROAI

**Claim:** Financial KPIs must go beyond simple cost savings to capture revenue growth, risk avoidance, and total economic value — and must be measured against pre-established baselines.
**Source:** AI21, "Key Performance Indicators for Measuring AI ROI in Banking," 2025; Workmate, "How to Measure AI ROI: 4 Frameworks Finance & Ops Leaders Actually Use," 2026; DBS Bank annual disclosures, 2025.
**Key details:** Three primary financial dimensions:
- **Revenue growth:** Enhanced interest income, fees, and commissions through AI-powered solutions (DBS); loan growth accelerated by AI-driven risk and pricing models (BBVA: 16.2% loan growth, 2025).
- **Cost savings:** Reduced contact-centre volume through AI self-service; lower FTE hours on automation-suitable tasks (data entry, reconciliation, document review); decreased manual exception rates. BBVA reduced cost-to-income ratio to 38.8% in 2025.
- **Risk avoidance:** Fraud loss reduction, fewer chargebacks, lower manual-review costs. BBVA reported fraud incidents down 75% over three years.
Recommended formula: **ROAI = (Incremental Revenue + Cost Savings + Risk Avoidance − Total Cost) ÷ Total Cost**.
When benefits span multiple years, apply NPV/DCF analysis at risk-adjusted discount rates (company WACC or higher). Typical AI projects show 12–24 month payback with 10–30% cost savings or 2–5× revenue uplift depending on use case.
**Use for:** Financial KPI section; connect to Ch 8 (Value dimension of Value/Capability/Trust).

---

### 1.3 Operational KPIs — efficiency, cycle time, throughput, error rate

**Claim:** Operational metrics must be function-specific, tied to real process outcomes, and distinguish between leading indicators (adoption, workflow redesign) and lagging indicators (throughput, error rate).
**Source:** BBVA operational metrics disclosures, 2025; Google Cloud, "The KPIs That Actually Matter for Production AI Agents," 2025–2026; Bain, "From Pilots to Payoff," 2025.
**Key details:** BBVA tracks granular operational KPIs:
- Cost per task (model + infrastructure) vs. baseline
- Cycle time and SLA adherence by segment
- First-pass yield and rework rate
- Throughput: items closed per FTE per week
- Employees save an average of 3 hours per week on routine tasks
For agentic AI systems specifically, Google Cloud recommends a three-pillar KPI framework:
1. **Reliability and operational efficiency:** Tool selection accuracy, plan adherence, hallucination rate. A "critic agent" can audit primary agent execution logs, converting subjective behaviours into objective metrics.
2. **Adoption and usage patterns:** How well agents integrate into existing workflows; daily active users; tasks augmented vs. automated.
3. **Business value:** Productivity gains, cost per transaction, new value generated.
A critical nuance: detecting **"silent failures"** — when agents produce correct outputs through flawed processes. Multi-dimensional assessment must cover final results, process trajectory, and trust/safety.
**Use for:** Operational KPI section; connect to Ch 6 (Operating Model layer) and Ch 11 (Playbook phases).

---

### 1.4 Adoption KPIs — usage, sentiment, workflows redesigned

**Claim:** Adoption metrics — beyond simple usage counts — are the strongest leading indicators of whether AI will deliver sustained value. "Workflows redesigned" and "processes AI-enabled" are more meaningful than login counts.
**Source:** Bain, "Executive Survey: AI Moves from Pilots to Production," 2025; McKinsey, "The State of AI," 2025; JPMorgan disclosures, 2025–2026.
**Key details:** Bain reports 80% of generative AI use cases met or exceeded expectations, but only 23% can tie initiatives to tangible business outcomes — suggesting adoption without measurement. JPMorgan now has **200,000 employees using its LLM Suite platform daily**, yet CEO Jamie Dimon acknowledges that "time saved is often too vague to measure concretely" and calls tech ROI "the hardest thing to measure."
Recommended adoption metrics:
- Daily/weekly active users and frequency
- Tasks augmented vs. tasks fully automated
- Workflows redesigned (not just digitised)
- "Processes AI-enabled" as % of total process portfolio
- Employee sentiment and readiness scores
- Superuser and champion metrics (who creates reusable skills, who trains others)
**Quote (Dimon):** "Returns on AI are difficult to quantify initiative by initiative."
**Use for:** Adoption KPI section; connect to Ch 3 (agentic employee) and Ch 4 (compounding across tiers).

---

### 1.5 Strategic KPIs — customer experience, decision quality, innovation velocity

**Claim:** Strategic KPIs connect AI investment to enterprise North Star metrics — customer satisfaction, decision quality, and innovation velocity — and prevent the trap of optimising internal efficiency while ignoring external impact.
**Source:** Allianz AI strategy disclosures, 2025; Business Analytics Institute, "AI's Business Value Playbook," 2025–2026.
**Key details:** Allianz measures AI success across four dimensions: **customer satisfaction, efficiency, effectiveness, and employee satisfaction** — a balanced scorecard approach that prevents over-indexing on cost alone. Over 80% of organisations report not seeing tangible enterprise-level EBIT impact despite deploying AI. The gap is often that organisations measure internal process metrics without linking them to customer outcomes (NPS, CSAT, retention) or strategic goals (market share, innovation pipeline, speed to market).
Recommended strategic metrics:
- NPS/CSAT trajectory post-AI deployment
- Decision quality (accuracy, speed, consistency)
- Innovation velocity (time from idea to production; new product/service launches)
- Competitive positioning indicators
**Use for:** Strategic KPI section; connect to Ch 8 (Value dimension) and Ch 12 (Readiness assessment).

---

### 1.6 The portfolio view — mix of pilots, scaled, and killed

**Claim:** CEOs need a portfolio-level view of AI initiatives — not just individual project metrics — tracking the pipeline from pilot to production, including deliberate kill decisions.
**Source:** Bain, "Executive Survey: AI Moves from Pilots to Production," 2025; GAI Forum, "The Pilot Purgatory Index," 2025.
**Key details:** Bain's 2025 survey shows domain-specific production rates: **software development 40%** of pilots moving to scale, **customer service 32%**, other domains above 20%. Over 90% of commercial executives surveyed have scaled at least one AI use case, with 62% scaling more than two. But these are the leaders — the industry average pilot-to-production rate remains approximately 13–15%.
Portfolio-level metrics should include:
- Number of active pilots vs. scaled vs. killed
- Pipeline: use cases in ideation, pilot, production
- Kill rate and reasons (a healthy portfolio kills decisively)
- Time from pilot launch to scale decision (target: <6 months)
- Resource allocation: % of AI budget on pilots vs. scaled initiatives
**Use for:** Portfolio view section; connect to Ch 11 (Playbook: Foundation → Activation → Scale) and Ch 12 (Readiness diagnostics).

---

## 2. Avoiding Pilot Purgatory

Evidence supporting the chapter's argument that most AI projects stay stuck in pilot because of organisational failures — not technical ones — and that disciplined gating, clear ownership, and upfront success criteria are the escape route.

---

### 2.1 The scale of the problem — 87% never escape

**Claim:** 87% of enterprise AI projects never move beyond the pilot stage. The failure is systematic across five organisational domains, not primarily technical.
**Source:** GAI Forum, "The Pilot Purgatory Index: Why 87% of Enterprise AI Projects Never Escape the Lab," 2025; McKinsey, "Overcoming Two Issues That Are Sinking Gen AI Programs," 2025.
**Key details:** Five critical gaps drive pilot purgatory: **intelligence** (wrong use-case selection), **implementation** (underestimating production complexity), **governance** (compliance as bottleneck), **ecosystem** (no platform or integration), and **capital allocation** (underestimating cost by 250–400%). McKinsey's analysis of 150+ companies identified two recurring failure modes: (1) Failure to innovate — 30–50% of teams' AI development time spent on compliance or waiting for compliance decisions; (2) Failure to scale — risk concerns and cost overruns prevent crossing from prototype to production.
The cost-misestimation trap is severe: a $50,000 proof-of-concept typically becomes $200,000–$300,000 in production. The "last 10–20%" contains all real complexity: legacy integration, error handling, security, compliance.
**Use for:** Root causes section; connect to Ch 1 (95% failure) and Ch 11 (Playbook — what to do differently).

---

### 2.2 Industry variation — financial services leads, healthcare lags

**Claim:** Financial services achieves 15–20% pilot-to-production rates (best in class) because of strong executive sponsorship, clear ROI metrics, and robust compliance frameworks. Healthcare and automotive lag due to infrastructure gaps and risk-averse cultures.
**Source:** GAI Forum, "The Pilot Purgatory Index," 2025; Bain, "Executive Survey," 2025.
**Key details:** Financial services' advantage comes from three factors: (1) measurable unit economics (cost per transaction, fraud savings, revenue per customer), (2) executive-level AI sponsorship (CEO/COO, not CTO alone), and (3) pre-existing compliance infrastructure that can be extended to AI governance rather than built from scratch. Bain confirms the domain effect: software development (40% to scale) and customer service (32%) outperform other functions, likely because both have clear, measurable baselines and rapid feedback loops.
**Use for:** Industry variation and sector benchmarks; connect to Ch 9 (European context — banking, insurance, manufacturing).

---

### 2.3 Kill criteria and gating — define success before you pilot

**Claim:** The most important decision in AI scaling is made before the pilot begins: defining upfront success criteria and kill criteria prevents pilots from drifting into purgatory.
**Source:** Eric D. Brown, "AI Pilot Purgatory," 2025; William Flaiz, "The Executive's Guide to AI Strategy: Beyond Pilots to Production," 2025–2026; Agility at Scale, "Scaling AI from Pilots to Enterprise-Wide Deployment," 2025.
**Key details:** Kill a pilot if:
- It lacks measurable business-value metrics defined upfront
- It has been running >6 months without production commitment
- It depends on manual workarounds, individual champions, or constant model tuning
- It tests only technical feasibility, not behavioural change and workflow integration
- Cost projections have diverged significantly from reality
Scale a pilot if:
- It delivers measurable business value with a clear production pathway
- It has defined success metrics and executive support
- It demonstrates adoption and process change, not just model accuracy
- It can operate systematically without constant human intervention
The gap between successful and failed pilots is execution discipline, not technology. A "success matrix" should cover four dimensions: business impact (quantified), risk tolerance (regulatory compliance), resource requirements (budget, timeline, team), and scalability indicators (architecture, org readiness).
**Use for:** Gating and kill-criteria section; practical guidance for CEOs. Connect to Ch 11 (decision gates in the Playbook).

---

### 2.4 ING — the 90% production rate case study

**Claim:** ING achieves a 90% pilot-to-production rate — three times the industry average — through a centralised AI platform, standardised governance, and large-scale employee training.
**Source:** Ziptone, "90% of ING's AI Pilot Projects Go Into Production," 2025; Computer Weekly, "Interview: How ING Reaps Benefits of Centralising AI," 2025; ING THINK, "AI Monthly: From Experimentation to Integration," 2025.
**Key details:** ING's three success factors:
1. **Centralised platform:** A single, standardised AI platform used globally for all applications (including generative and agentic AI), managed with risk controls, guardrails, and real-time monitoring.
2. **Governance integration:** Risk and compliance built into the platform from the start — not bolted on as an afterthought. This eliminates the 30–50% compliance time drain McKinsey identifies as a root cause of pilot purgatory.
3. **Employee training at scale:** 5,000 employees trained in data skills and generative AI, ensuring adoption and the ability to challenge AI decisions.
Production applications: KYC, call centres, customer due diligence, retail personalisation, engineering. Generative AI chatbots automate 75% of customer queries across several countries. Agentic AI in mortgage processing augments human capabilities.
**Use for:** Primary case study for "escaping pilot purgatory"; connect to Ch 10 (What the Leaders Did).

---

### 2.5 The micro-productivity trap — Bain's warning

**Claim:** Grassroots AI experimentation creates a "micro-productivity trap" — many small efficiency gains that feel like progress but never compound into enterprise-wide impact without top-down direction.
**Source:** Bain & Company, "AI Survey: Four Themes Emerging," 2025; Bain, "Executive Survey: AI Moves from Pilots to Production," 2025.
**Key details:** AI is now a top-three priority for 74% of companies (up from 60% a year earlier), and 21% call it their top priority. Yet despite this strategic priority, only 23% can tie AI initiatives to tangible business outcomes. The disconnect: proliferation of proofs of concept and isolated use cases delivers modest, localised efficiency gains that fail to scale. Bain's assessment: "Grassroots experimentation with AI tools sparks innovation and cultural momentum — all good — but it does not self-organise into enterprise-wide impact. Without clear direction from the top, these efforts remain fragmented, siloed, and ultimately shallow."
Real value requires applying AI across entire workflows — not just isolated functions — and ensuring organisational processes can support rapid AI-generated outputs.
**Use for:** Anti-patterns section; connect to Ch 2 (Leadership Is Not Optional) and Ch 4 (compounding across tiers).

---

## 3. Board Governance: Role and Metrics

Evidence supporting the chapter's argument that the board has an evolving, critical role in AI governance — and that most boards are dangerously unprepared to fulfil it.

---

### 3.1 The board knowledge and oversight gap

**Claim:** 66% of board directors report limited, minimal, or no AI knowledge — yet boards are now expected to govern AI at the highest level of corporate accountability.
**Source:** McKinsey, "The AI Reckoning: How Boards Can Evolve," 2025; NACD, "2025 Public Company Board Practices & Oversight Survey," 2025; NACD, "Why AI Literacy Must Precede Deployment," 2025.
**Key details:** The gap is stark:
- **66% of directors** report limited to no AI knowledge or experience
- Only **15% of boards** receive AI-related metrics
- Fewer than **25% have board-approved AI policies**
- Only **14% discuss AI at every meeting**
- Only **39% of Fortune 100 companies** have formal board-level AI oversight
Yet **88% of organisations use AI in at least one function**.
The performance gap is measurable: companies with AI-savvy boards outperform peers by **10.9 percentage points in ROE**; those without lag 3.8% below industry average. NACD emphasises that AI literacy must precede AI deployment — a foundational requirement for effective governance.
**Use for:** Current state diagnosis; connect to Ch 2 (Leadership Is Not Optional).

---

### 3.2 McKinsey's four board archetypes and recommended metrics

**Claim:** McKinsey identifies four AI board archetypes — Pragmatic Adopters, Functional Reinventors, Internal Transformers, Business Pioneers — each requiring different governance postures and metrics.
**Source:** McKinsey, "The AI Reckoning: How Boards Can Evolve," 2025.
**Key details:**
- **Pragmatic adopters:** Wait for evidence before scaling. Board should scan adjacent industries to anticipate competitive shifts.
- **Functional reinventors:** Focus on high-ROI targeted workflows (scheduling, forecasting, logistics). Board must prevent fragmentation and ensure scaling.
- **Internal transformers:** Rebuild operating models with AI as core infrastructure. Board must verify structural gains and system resilience.
- **Business pioneers:** Use AI to create new markets and revenue streams. Board must assess data moats and regulatory exposure.
McKinsey recommends boards demand specific metrics: ROI by business unit, % of processes AI-enabled, workforce reskilling progress, regulatory alignment, override rates, and CEO oversight correlation with EBIT impact.
**Quote (McKinsey):** AI is "an 80 percent business transformation and 20 percent tech transformation."
**Use for:** Board archetype and recommended metrics section; connect to Ch 8 (Value/Capability/Trust) and Ch 11 (Playbook phases).

---

### 3.3 Board-level accountability metrics and dashboards

**Claim:** Traditional performance metrics (accuracy, adoption, cost savings) are insufficient for board oversight. Boards need a governance dashboard covering value, risk, and operations — with ownership clarity and escalation speed.
**Source:** EC-Council, "Board-Level Metrics for Measuring AI Accountability," 2025; Gend.co, "AI Governance for Boards: Strategy, Risk & Compliance," 2025; NovaEdge Digital Labs, "AI Governance in 2026," 2026.
**Key details:** Effective board-level AI accountability requires metrics beyond traditional KPIs:
- **Ownership clarity:** Who owns AI risk at the executive level?
- **Decision rights:** Clear authority chains when issues arise
- **Escalation speed:** How fast do problems surface to the board?
- **Alignment to intent:** Are initiatives staying true to approved purpose?
Recommended board KPI dashboard tracks three dimensions:
1. **Value:** Cycle time improvement, quality uplift, revenue lift
2. **Risk:** Error rate, bias metrics, compliance incidents, override rates
3. **Operations:** Incident response time, retraining cadence, model drift
Implementation timeline: a 90-day action plan — Days 0–30: AI governance baseline and board literacy; Days 31–60: policy approval, DPIA completion, model inventory; Days 61–90: KPI dashboard implementation and independent assurance review.
**Use for:** Board metrics and dashboard section; practical guidance for what a board should actually receive.

---

### 3.4 Committee structures and governance frameworks

**Claim:** Effective AI governance requires dedicated committee structures — whether through existing audit/risk committees or new AI-specific committees — with clear ownership, a model inventory, and multi-dimensional controls.
**Source:** Gend.co, "AI Governance for Boards," 2025; NovaEdge Digital Labs, "AI Governance in 2026," 2026; Medium (Piyush Sharma), "The Board's Reckoning: Stewardship in the Age of AI," 2026.
**Key details:** Governance requires:
- **Clear ownership structure** with defined roles and accountability at executive and board level
- **Model inventory system** with documented system owners, data lineage, and human-in-the-loop checkpoints
- **Multi-dimensional controls:** data governance, access controls, procurement protocols, security
- **Standards alignment:** ISO 42001, NIST AI Risk Management Framework, EU AI Act compliance
Three committee options: (1) Extend existing audit/risk committee remit to include AI; (2) Create a technology/digital committee; (3) Establish a dedicated AI committee. Leading practice is a hybrid: a standing AI agenda item on the risk or audit committee, with quarterly deep-dives by a technology sub-committee.
**Use for:** Committee structures section; connect to European two-tier board context.

---

### 3.5 Board literacy and what boards that "get it" do differently

**Claim:** Boards that invest in AI literacy produce measurably better outcomes — and the CEO plays the critical role in board education.
**Source:** McKinsey, "The AI Reckoning," 2025; NACD, "Why AI Literacy Must Precede Deployment," 2025; NACD, "Critical Factors for Effective AI Oversight at the Board Level," 2025.
**Key details:** AI-savvy boards differ in three ways:
1. **They demand metrics, not demos.** Boards that receive structured AI dashboards make better governance decisions than those who see technology demonstrations.
2. **They appoint AI-literate directors.** Some leading boards now require at least one director with hands-on AI/technology experience.
3. **They invest in board education.** Quarterly briefings, external expert sessions, and structured AI literacy programmes.
NACD identifies AI literacy as a precondition for deployment — boards cannot govern what they don't understand. The CEO's role: translate AI complexity into business language the board can govern, present AI as strategic transformation (not technology), and ensure the board receives the right metrics at the right cadence.
**Use for:** Board literacy section; connect to Ch 2 (Leadership Is Not Optional) and Ch 14 (A Leadership Decision).

---

## 4. Baselines, Attribution, and Rigour

Evidence supporting the chapter's argument that measurement rigour — starting with baselines, applying proper attribution, and using appropriate time horizons — is the difference between knowing your AI works and hoping it does.

---

### 4.1 The baseline problem — most projects fail to prove impact because they never measured the starting point

**Claim:** The single biggest measurement mistake is failing to establish a baseline before AI implementation. Without baselines, organisations make subjective claims instead of documenting concrete incremental impact.
**Source:** Dima AI, "How to Measure AI ROI: The 2026 Reality Check," 2026; Second Talent, "How Enterprises Are Measuring ROI on AI Investments," 2026.
**Key details:** With baselines: "Response time dropped from 8 minutes to 45 seconds — saving 7.5 minutes per ticket, worth $4,375/month in labour savings." Without baselines: "Our AI tool is great." The difference is the difference between a funded programme and a cancelled experiment.
Establishing baselines requires measuring the current state of every process targeted for AI augmentation — before deployment: cycle time, error rate, cost per unit, throughput, customer satisfaction. This baseline becomes the denominator in all subsequent ROI calculations.
**Use for:** Baselines section; connect to Ch 12 (Readiness assessment — "measure before you start").

---

### 4.2 Attribution — isolating AI's incremental impact

**Claim:** Attributing financial impact to AI requires rigorous methods — control groups, staggered rollouts, A/B testing — because multiple initiatives and external factors are always at play.
**Source:** DBS Bank methodology (Forrester analysis), 2025; Everworker AI, "AI ROI for Marketing: A Board-Ready Framework for 2026," 2026; Workmate, "How to Measure AI ROI," 2026.
**Key details:** DBS Bank sets the gold standard: it attributes AI value by comparing outcomes between customers offered AI-driven solutions and control groups — ensuring tangible measurement rather than theoretical estimates. This is how DBS validated its S$1 billion AI economic value figure for 2025 (up from S$750 million in 2024, a 33% year-over-year increase).
Best-practice attribution methods:
- **Geo-holdouts:** Deploy in some regions, hold back others, compare
- **Staggered rollouts:** Phase deployments and measure difference between early and late adopters
- **Matched markets / A/B testing:** Control for confounding variables
- **Proxies:** When direct measurement is impossible, use time saved, throughput increase, or error reduction as proxies — but always disclose the proxy
The five-dimension attribution framework: time savings, revenue impact, cost avoidance, risk reduction, and strategic benefits.
**Use for:** Attribution section; DBS as primary case study for rigorous measurement.

---

### 4.3 Measurement time horizon — the 6-month trap

**Claim:** Most AI projects are measured far too early. MIT's "95% failure" finding measured ROI at only 6 months. Gartner data shows high-maturity organisations sustain AI projects for 3+ years, while low-maturity organisations abandon them prematurely.
**Source:** Gartner, "Survey Finds 45% of Organizations With High AI Maturity Keep AI Projects Operational for at Least Three Years," June 2025 (432 respondents across U.S., U.K., France, Germany, India, Japan); MIT NANDA Report, 2025.
**Key details:** Key findings:
- **45% of high-maturity organisations** keep AI projects operational for 3+ years vs. only **20% of low-maturity** organisations
- High-maturity organisations score 4.2–4.5 on Gartner's 5-level AI Maturity Model
- **63% of high-maturity organisations** run financial analysis on AI projects (vs. far fewer at low maturity)
- **57% of high-maturity organisations** have business units that trust and are ready to use new AI solutions, vs. only **14%** in low-maturity organisations
The 6-month measurement window is a trap: many AI projects need 12–24 months to show full ROI (process change, adoption curve, feedback loops). Organisations that kill projects at 6 months systematically destroy value that would have materialised in months 7–24.
Recommendation: minimum 12-month measurement horizon for initial ROI assessment; 3-year operational horizon as the benchmark for sustained value.
**Use for:** Measurement rigour section; connect to Ch 1 (95% failure — partly a measurement failure) and the CEO's time horizon.

---

### 4.4 Full-cost accounting — hidden costs exceed expectations by 40–60%

**Claim:** AI projects' hidden costs — compliance reviews, model retraining, infrastructure scaling, governance overhead — routinely exceed initial expectations by 40–60%, making accurate cost accounting essential for honest ROI.
**Source:** Second Talent, 2026; Dima AI, 2026; GAI Forum, "Pilot Purgatory Index," 2025.
**Key details:** A $50,000 proof-of-concept typically becomes $200,000–$300,000 in production. The cost escalation comes from: data platforms, network access, and storage (more expensive than LLM token costs); legacy system integration; error handling and edge cases; security and compliance requirements; ongoing monitoring and model retraining.
Proper frameworks separate **build costs** (one-time: development, integration, training) from **run costs** (recurring: compute, monitoring, retraining, governance) and capture total cost of ownership over the project's expected life. 62% of banks face significant pressure from shareholders to show immediate ROI, while only 26% have experienced high revenue contribution from AI — creating a dangerous incentive to undercount costs for short-term optics.
**Use for:** Full-cost accounting section; connect to Ch 8 (Value assessment — realistic cost modelling).

---

## 5. European Context: Governance, Regulation, and Board Accountability

Evidence supporting the chapter's argument that the European regulatory and corporate governance context creates distinctive obligations — and opportunities — for boards governing AI.

---

### 5.1 EU AI Act — board accountability and directors' duties

**Claim:** The EU AI Act does not formally rewrite directors' duties but sharpens what reasonable digital governance looks like — effectively raising the floor for board-level AI oversight. Two novel fiduciary duties have emerged: "AI due care" and "AI loyalty oversight."
**Source:** Directors' Institute, "Digital Governance After the AI Act: What Boards Need to Know," 2025; Oxford Law Blogs, "Fiduciary Duties and the Business Judgment Rule 2.0 in the AI Act Age," January 2026; The Corporate Governance Institute, "The EU's AI Act: Boards Should Feel the Urgency," 2025.
**Key details:** Implementation is phased: AI practices banned early 2025; general-purpose AI obligations from August 2025; high-risk system requirements across 2026–2027. Penalties: up to **7% of global revenue**.
Two novel fiduciary duties:
1. **AI due care:** Directors must exercise informed, technologically literate, and ethically grounded oversight of algorithmic systems. This requires **cognitive adequacy** — the capacity to question, understand, and monitor technological tools shaping corporate choices.
2. **AI loyalty oversight:** Directors must verify that delegated systems remain impartial and aligned with company objectives. Procedural compliance alone is insufficient.
Directors need not become coders but must know which questions to ask about algorithms' design assumptions, data provenance, and bias parameters. Boards are expected to govern systems, information flows, accountability, and risk — not to design models or select algorithms. The Act uses a risk-based approach: minimal risk (unregulated), high-risk (heavy controls), specific transparency risk (disclosure needed), unacceptable risk (banned).
**Warning:** The risk of "AI theatre" — glossy demos substituting for actual governance — is explicitly called out as insufficient under the new regime.
**Use for:** EU AI Act and board accountability section; connect to Ch 9 (Europe's Distinctive Edge).

---

### 5.2 2026: the governance inflection point — "govern or perish"

**Claim:** 2026 marks the inflection point where AI governance has transitioned from optional to mandatory, driven by regulatory enforcement, investor scrutiny, and escalating AI liability.
**Source:** NovaEdge Digital Labs, "AI Governance in 2026: The Board-Level Mandate," 2026; ReadItQuik, "AI Governance in 2026: How Enterprises Can Scale Without Losing Control," 2026.
**Key details:** Three converging forces:
1. **Regulatory tsunami:** EU AI Act penalties up to 7% of global revenue; FTC, SEC enforcement actions increasing; NIST AI Risk Management Framework becoming the de facto negligence standard.
2. **Investor demands:** "AI Governance Maturity" is now a critical valuation and risk factor. Investors increasingly demand transparency on AI governance, regulatory compliance, workforce skills, environmental impacts, and transparency mechanisms.
3. **Standards hardening:** ISO 42001, NIST AI RMF, and the EU AI Act are converging into a baseline governance standard that boards cannot ignore.
The era of "move fast and break things" has been replaced by "govern or perish."
**Use for:** Urgency section; connect to Ch 9 (European advantage — regulation as moat) and Ch 14 (A Leadership Decision).

---

### 5.3 European corporate governance specificities — two-tier boards and stakeholder reporting

**Claim:** European corporate governance structures — particularly two-tier boards (Germany, Netherlands, Austria) and stakeholder-oriented governance codes — create distinctive AI governance dynamics that differ from the Anglo-American model.
**Source:** Directors' Institute, 2025; Oxford Law Blogs, 2026; existing book research on European governance context.
**Key details:** In two-tier systems (e.g. German Vorstand/Aufsichtsrat), the management board (Vorstand) is responsible for AI strategy and implementation, while the supervisory board (Aufsichtsrat) provides oversight — creating a natural separation between execution and governance that can be leveraged for AI accountability. Works councils in Germany and the Netherlands have co-determination rights on matters affecting work conditions, which extends to AI deployment affecting job roles and workflows.
Corporate governance codes across Europe (UK Corporate Governance Code, German Corporate Governance Code, Dutch Corporate Governance Code) are increasingly being interpreted to require digital literacy at board level. The NFRD/CSRD reporting requirements may require disclosure of AI's impact on workforce, environment, and governance — adding a compliance dimension beyond the AI Act itself.
This creates both obligation and opportunity: European boards have a structural advantage in AI governance because the oversight mechanisms already exist. The challenge is equipping those mechanisms with AI literacy and appropriate metrics.
**Use for:** European governance context; connect to Ch 9 (Europe's Distinctive Edge — governance as competitive advantage).

---

## 6. Case Studies: What Leading Companies Measure

Summary of disclosed AI measurement practices from companies referenced across the book.

---

### 6.1 DBS Bank — S$1 billion in validated AI economic value

**Financial:** S$1 billion in AI economic value in 2025 (up 33% from S$750 million in 2024). Value validated through control-group methodology — customers offered AI-driven solutions vs. control groups.
**Attribution method:** Rigorous A/B comparison; not theoretical estimates.
**Source:** Business Times Singapore, 2025; Forrester analysis, 2025.

---

### 6.2 JPMorgan — $2 billion AI investment "paid for itself"

**Financial:** $2 billion AI investment has paid for itself in cost savings. $1.5–2 billion in annual business value from AI. AI-attributed benefits growing 30–40% year-over-year.
**Adoption:** 200,000 employees use LLM Suite platform daily.
**Challenge:** CEO acknowledges ROI is "the hardest thing to measure" initiative by initiative.
**Source:** Business Insider, 2026; Jason Leinart analysis, 2025; Ainvest analysis, 2026.

---

### 6.3 ING — 90% pilot-to-production rate

**Operational:** 90% of AI pilots reach production (industry average ~13–15%). Centralised platform, standardised governance, 5,000 employees trained.
**Customer impact:** AI chatbots automate 75% of customer queries across countries.
**Source:** Ziptone, 2025; Computer Weekly, 2025.

---

### 6.4 BBVA — cost-to-income, loan growth, fraud reduction

**Financial:** Cost-to-income ratio 38.8% (2025); 16.2% loan growth; ROTE 19.3%.
**Operational:** Employees save 3 hours/week on routine tasks; fraud incidents down 75% over three years.
**Governance:** 90-day execution framework with privacy, security, model risk reviews; immutable audit logs; EU AI Act alignment.
**Source:** BBVA disclosures, 2025; OpenAI partnership announcement, 2025; BBVA cloud platform announcement, 2025.

---

### 6.5 Allianz — four-dimensional measurement

**Strategic:** Measures across four balanced dimensions: customer satisfaction, efficiency, effectiveness, and employee satisfaction.
**Approach:** Advancing from predictive to prescriptive analytics and generative AI; measuring real-world business outcomes rather than technology deployment.
**Source:** Allianz media centre, 2025.

---

### 6.6 Schneider Electric — measurable ESG and operational impact

**Operational:** Cost reduction, maintenance optimisation, and carbon emission reduction ranging from 10–60% across manufacturing use cases.
**Example:** Lippulaiva shopping centre achieved 335 tonnes CO₂ annual reduction; five-year payback on €3 million investment.
**Source:** Schneider Electric blog, 2026; Business Analytics Institute, 2025.

---

## 7. Connections to Other Chapters

### Ch 8 (Value/Capability/Trust) → Metrics
Value/Capability/Trust translates directly into measurement categories:
- **Value** → Financial and strategic KPIs (ROAI, revenue impact, NPS)
- **Capability** → Adoption KPIs (skills, workflows redesigned, processes AI-enabled)
- **Trust** → Governance KPIs (compliance incidents, override rates, bias metrics, audit results)

### Ch 11 (Playbook) → KPIs by Phase
- **Foundation phase:** Literacy rates, governance framework completion, baseline establishment
- **Activation phase:** Strategy alignment (AI Transformation Framework applied), pilot success rate, first wins documented with metrics
- **Scale phase:** Enterprise value delivery, portfolio production rate, sustained ROAI

### Ch 12 (Readiness) → Readiness KPIs vs. Transformation KPIs
Readiness KPIs (Ch 12) measure *where you are now*; Transformation KPIs (Ch 13) measure *whether you're making progress*. Roadmap milestones from Ch 12 become measurable outcomes in Ch 13. The handoff: readiness assessment → baseline → pilot metrics → scale metrics → board governance.

---

## 8. Conflicts and Nuances with Existing Research

### ROI figures should be treated with caution
DBS and JPMorgan disclose high-level AI value figures, but both acknowledge attribution is imprecise. Dimon calls it "the hardest thing to measure." These are directional, not precise — useful as evidence that measurement *can* be done, but not as benchmarks.

### The 95% failure rate is partly a measurement failure
MIT's 95% figure measured ROI at only 6 months — well before many AI projects deliver full value. The "failure rate" overstates actual failure and understates premature abandonment. This nuance is important for the CEO audience: the problem may be patience and measurement rigour, not AI capability.

### "Pilot purgatory" figures vary by source
Different sources cite 80%, 87%, or 90% of pilots stuck. The exact figure matters less than the consistent finding across all sources: the vast majority of AI pilots do not reach production, and the causes are organisational, not technical.

### Board governance recommendations are converging
McKinsey, NACD, EU regulators, and governance institutes are converging on similar recommendations: board-level literacy, structured metrics, regular AI agenda items, and dedicated committee oversight. The consensus is strong enough to present as settled best practice, not contested opinion.

---

*Research compiled: March 2026. Sources from 2025–2026 consultancy reports, board surveys, governance guidelines, regulatory analysis, and company disclosures.*
