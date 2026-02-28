# Don't Build Agents, Build Skills Instead

**Speakers:** Barry Zhang & Mahesh Murag (Anthropic)
**Source:** AI Engineer Conference
**Video:** https://www.youtube.com/watch?v=CEvIs9y1uog
**Duration:** ~16 minutes
**Date Captured:** 2026-02-28

---

## Core Thesis

The future of AI isn't more agents — it's **one universal agent powered by a library of domain-specific skills**.

Agents today have impressive reasoning and broad connectivity, but they consistently fail at tasks requiring deep, procedural domain expertise. The fix isn't more scaffolding or smarter models — it's smaller, composable units of expertise called **Skills**.

---

## The Problem: Agents Are Smart but Not Expert

Today's agents behave like a 300 IQ generalist — brilliant at improvisation, but missing the deep, stable knowledge that real workflows require. Every task is a fresh improvisation. That looks impressive in demos but is not reliable in production.

The core failure modes:
- **Missing context upfront** — agents don't know what they don't know about your domain
- **Poor expertise absorption** — hard to embed procedural knowledge into general-purpose prompts
- **No learning over time** — the same mistakes are made repeatedly with no compounding improvement

### The "Barry vs. Mahesh" Analogy

> *"Who do you want doing your taxes? Mahesh, the 300 IQ mathematical genius, or Barry, the experienced tax professional? I would pick Barry every time."*

Agents are Mahesh — spectacularly capable, but lacking the domain expertise of Barry. Intelligence alone is not enough; **stable, encoded domain expertise** is what drives reliable real-world performance.

---

## The Solution: Skills

**Skills** are organized collections of files that package composable, procedural knowledge that agents can dynamically load on demand.

### What a Skill Looks Like

At its simplest, a skill is a directory containing a `SKILL.md` file:

```
your_project/
├── skills_agent.py
└── skills/
    └── weather_checker/
        ├── SKILL.md
        └── weather_checker.py
```

The `SKILL.md` file must begin with **YAML frontmatter** containing at minimum:
- `name` — the skill's identifier
- `description` — what the skill does

At startup, the agent pre-loads the `name` and `description` of every installed skill into its system prompt. This is the **first level of progressive disclosure**: just enough information for the agent to know *when* to use each skill, without loading the full content into context.

---

## The Key Design Principle: Progressive Disclosure

Skills load information only when needed — like a well-organized manual that starts with a table of contents, then specific chapters, then a detailed appendix.

- **Level 1:** Metadata (name + description) — always in context
- **Level 2:** Full `SKILL.md` instructions — loaded when the skill is selected
- **Level 3:** Scripts and assets — executed or loaded on demand

This means the **amount of context that can be bundled into a skill is effectively unbounded**, while keeping the active context window lean.

---

## Code as the Universal Interface

Skills treat **code and the file system as the universal interface** between models and digital environments:

- Bash and file systems serve as thin, scalable scaffolding for agents
- Scripts act as self-documenting, modifiable tools — far better than static instruction strings
- Code provides **deterministic reliability** for operations where LLM token generation is too expensive or unpredictable (e.g., sorting, arithmetic, API calls)

> Give an LLM file system access and code execution, and suddenly one agent loop can handle everything — data analysis, API calls, automation — without custom builds for each use case.

---

## Skills vs. MCP Servers

Skills complement rather than replace MCP (Model Context Protocol) servers:

| Layer | Tool | Purpose |
|---|---|---|
| **Connectivity** | MCP Servers | Access to external data, APIs, services |
| **Expertise** | Skills | Domain knowledge, procedural workflows |

> *"Use MCP servers for connectivity, and Skills for expertise."* — Mahesh Murag

Developers are already building skills that **orchestrate workflows of multiple MCP tools** to handle more complex, multi-step tasks.

---

## The Skills Ecosystem

Since launch, the design has produced a rapidly growing ecosystem of thousands of skills across three categories:

1. **Foundational Skills** — general or domain-specific capabilities built by Anthropic
2. **Third-Party Skills** — created by partners and the broader community
3. **Enterprise/Team Skills** — internal skills built within organizations

Skills are evolving from simple markdown prompt files to packaging **software, executables, binaries, code, scripts, and assets**. Some skills being built today take weeks or months to develop and are actively maintained.

---

## The Bigger Architectural Vision

Anthropic frames the stack as:

| Layer | Analogy | Component |
|---|---|---|
| Hardware | Processor | The Model (Claude) |
| OS | Operating System | The Agent Runtime |
| Applications | Apps | Skills (where real value lives) |

Just as a few companies build chips and OSes but millions of developers build software, **Skills open up the application layer** for everyone — enabling domain experts to encode their knowledge and solve concrete problems "just by putting stuff in the folder."

---

## Future Vision

- Agents that **autonomously create their own Skills** from accumulated experience
- Single agents that gain capabilities across **multiple domains** by loading different skill libraries
- **Network effects** as the Skills ecosystem grows — each new skill makes every agent more capable
- Intelligence gets cheaper over time; **high-quality Skills are where the real leverage is**

---

## Practical Takeaways for Builders

1. **Stop obsessing over agent architecture** — focus on encoding domain expertise instead
2. **Write SKILL.md files** that define how an agent should think, act, and analyze in your domain
3. **Shift the question** from *"How do I build a smarter agent?"* to *"How do I capture my domain in clear, transferable skills?"*
4. **Use Skills for expertise, MCP for connectivity** — don't conflate the two
5. **Version your skills in Git** — they are artifacts of knowledge, treat them like code
6. **Let the agent be the execution engine** — discover the right skill, load it, follow the playbook, keep a human in the loop where judgment is required

---

## Key Quotes

> *"Agents have intelligence and capabilities, but not always the expertise we need for real work."*

> *"Skills provide composable, procedural knowledge in organized folders with scripts as tools, enabling agents to acquire domain expertise on demand."*

> *"Intelligence will keep getting cheaper. High-quality skills — well-written SKILL.md files that encode real expertise — are where the real leverage is."*

---

## Sources

- [Video: Don't Build Agents, Build Skills Instead (YouTube)](https://www.youtube.com/watch?v=CEvIs9y1uog)
- [Class Central: Free Video Listing](https://www.classcentral.com/course/youtube-don-t-build-agents-build-skills-instead-barry-zhang-mahesh-murag-anthropic-510545)
- [Lilys.ai: Full Insight Notes](https://lilys.ai/en/notes/agent-skills-20251225/build-skills-not-agents)
- [Medium: Don't Build Agents, Build Skill](https://medium.com/@yanqing_j/dont-build-agents-build-skill-62b97b4eae30)
- [Anthropic Engineering: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Stop Building Agents, Start Building Skills – brgr.one](https://www.brgr.one/blog/stop-building-agents-build-skills)
- [Anthropic Says Build Skills, Not Agents – OutcomeOps](https://www.outcomeops.ai/blogs/anthropic-says-build-skills-not-agents)
