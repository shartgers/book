# Anthropic: Don't Build Agents, Build Skills Instead — Key Insights

## Source

- **Video:** [Don't Build Agents, Build Skills Instead](https://www.youtube.com/watch?v=CEvIs9y1uog)
- **Speakers:** Barry Zhang & Mahesh Murag (Anthropic)
- **Event:** AI Engineer Conference
- **Duration:** ~16 minutes
- **Date Captured:** 2026-02-28
- **Keywords:** agent skills, SKILL.md, domain expertise, MCP, progressive disclosure, composable knowledge

---

## Core Thesis

The future of AI isn't more agents — it's **one universal agent powered by a library of domain-specific skills**. Agents today have impressive reasoning and broad connectivity, but they consistently fail at tasks requiring deep, procedural domain expertise. The fix isn't more scaffolding or smarter models — it's smaller, composable units of expertise called **Skills**.

---

## Main Insight 1: Intelligence Alone Is Not Enough — Domain Expertise Matters

Today's agents behave like a 300 IQ generalist — brilliant at improvisation, but missing the deep, stable knowledge that real workflows require. Every task is a fresh improvisation. That looks impressive in demos but is not reliable in production.

**The "Barry vs. Mahesh" Analogy:** *"Who do you want doing your taxes? Mahesh, the 300 IQ mathematical genius, or Barry, the experienced tax professional? I would pick Barry every time."* Agents are Mahesh — spectacularly capable, but lacking the domain expertise of Barry. **Stable, encoded domain expertise** is what drives reliable real-world performance.

**Core failure modes of agents without skills:**
- Missing context upfront — agents don't know what they don't know about your domain
- Poor expertise absorption — hard to embed procedural knowledge into general-purpose prompts
- No learning over time — the same mistakes are made repeatedly with no compounding improvement

---

## Main Insight 2: Skills Are Composable, Procedural Knowledge Packages

**Skills** are organized collections of files that package composable, procedural knowledge that agents can dynamically load on demand. At minimum, a skill is a directory with a `SKILL.md` file containing YAML frontmatter (name, description). Skills can also include scripts, executables, binaries, and assets — evolving from simple markdown to full software packages.

> *"Skills provide composable, procedural knowledge in organized folders with scripts as tools, enabling agents to acquire domain expertise on demand."*

---

## Main Insight 3: Progressive Disclosure Keeps Context Lean

Skills load information only when needed — like a well-organized manual that starts with a table of contents, then specific chapters, then a detailed appendix.

| Level | Content | When Loaded |
|-------|---------|-------------|
| 1 | Metadata (name + description) | Always in context |
| 2 | Full SKILL.md instructions | When skill is selected |
| 3 | Scripts and assets | On demand |

The **amount of context that can be bundled into a skill is effectively unbounded**, while keeping the active context window lean. This is the key design principle that makes skills scalable.

---

## Main Insight 4: Code as the Universal Interface

Skills treat **code and the file system as the universal interface** between models and digital environments. Bash and file systems serve as thin, scalable scaffolding. Scripts act as self-documenting, modifiable tools — far better than static instruction strings. Code provides **deterministic reliability** for operations where LLM token generation is too expensive or unpredictable (sorting, arithmetic, API calls).

> Give an LLM file system access and code execution, and suddenly one agent loop can handle everything — data analysis, API calls, automation — without custom builds for each use case.

---

## Main Insight 5: Skills vs. MCP — Different Layers, Complementary Roles

| Layer | Tool | Purpose |
|-------|------|---------|
| **Connectivity** | MCP Servers | Access to external data, APIs, services |
| **Expertise** | Skills | Domain knowledge, procedural workflows |

> *"Use MCP servers for connectivity, and Skills for expertise."* — Mahesh Murag

Developers are building skills that **orchestrate workflows of multiple MCP tools** to handle complex, multi-step tasks. Don't conflate the two.

---

## Main Insight 6: The Stack Analogy — Skills Are the Application Layer

| Layer | Analogy | Component |
|-------|---------|-----------|
| Hardware | Processor | The Model (Claude) |
| OS | Operating System | The Agent Runtime |
| Applications | Apps | Skills (where real value lives) |

Just as a few companies build chips and OSes but millions of developers build software, **Skills open up the application layer** for everyone — enabling domain experts to encode their knowledge and solve concrete problems "just by putting stuff in the folder."

---

## Main Insight 7: Where the Real Leverage Is

> *"Intelligence will keep getting cheaper. High-quality skills — well-written SKILL.md files that encode real expertise — are where the real leverage is."*

The skills ecosystem is growing rapidly across three categories: **Foundational Skills** (Anthropic), **Third-Party Skills** (partners, community), and **Enterprise/Team Skills** (internal). Some skills take weeks or months to develop and are actively maintained. **Network effects** — each new skill makes every agent more capable.

---

## Practical Takeaways for Builders

1. **Stop obsessing over agent architecture** — focus on encoding domain expertise instead
2. **Write SKILL.md files** that define how an agent should think, act, and analyze in your domain
3. **Shift the question** from *"How do I build a smarter agent?"* to *"How do I capture my domain in clear, transferable skills?"*
4. **Use Skills for expertise, MCP for connectivity** — don't conflate the two
5. **Version your skills in Git** — they are artifacts of knowledge, treat them like code
6. **Let the agent be the execution engine** — discover the right skill, load it, follow the playbook, keep a human in the loop where judgment is required

---

## Future Vision

- Agents that **autonomously create their own Skills** from accumulated experience
- Single agents that gain capabilities across **multiple domains** by loading different skill libraries
- **Network effects** as the Skills ecosystem grows

---

## Summary for Book Use

Strong source for **skills-over-agents strategy**, **domain expertise framing**, and **progressive disclosure** as a design principle. The Barry vs. Mahesh analogy is memorable for explaining why intelligence alone fails. The stack analogy (model = processor, runtime = OS, skills = apps) clarifies the architectural vision. Practical takeaways and the "where the real leverage is" quote are reusable for any audience considering agent vs. skill investment. Cross-reference with `agent-skills-research-topics.md` for deeper exploration of enterprise skills management and adoption.
