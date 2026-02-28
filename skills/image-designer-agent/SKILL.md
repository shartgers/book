---
name: image-designer-agent
description: Creates diagrams and visual frameworks for the book in a professional, minimalist, corporate style. Called by the Writer Agent during Wave 2 to produce the chapter framework diagram. Also used standalone when a diagram is requested directly.
---

# Book Diagram Style

Generate images for the management book in the book's established visual style (described below). Use the **GenerateImage** tool when the user requests a diagram, framework visualization, or book illustration.

---

## Output Location

**Always write generated images to the `images/` folder.**

- Use the `filename` parameter with path: `images/[descriptive-name].png`
- Example: `images/ai-adoption-stages.png`, `images/ch02-framework.png`
- Create the `images/` folder if it does not exist before generating.
- Use descriptive, kebab-case filenames (e.g., `agentic-maturity-model.png`).

---

## When to Use

- User asks for a diagram, image, or illustration for the book
- User requests a framework visualization, maturity model, or stage diagram
- User mentions "4-stages style," "book style," or "match the reference"
- Creating visual content for chapters (agentic systems, transformation stages, etc.)

---

## Style Specification

Apply these specifications to every generated diagram:

### Color Palette

| Element | Color | Notes |
|---------|-------|-------|
| **Background** | Very light grey, off-white | Clean, unobtrusive canvas |
| **Primary accent** | Muted dark blue (#3F51B5, deep indigo, slate blue) | Title boxes, arrows |
| **Text on blue** | White | High contrast |
| **Text on white** | Black or very dark grey | Body text, descriptions |

### Shapes and Layout

- **Stage/title boxes:** Solid dark blue rectangles, slightly rounded corners
- **Description boxes:** White rectangles, slightly rounded corners, below title boxes
- **Arrows:** Thin solid blue lines, triangular arrowheads, indicate flow
- **Stair-step layout:** For multi-stage diagrams, each stage slightly elevated from the previous (left-to-right, upward progression)

### Typography

- **Main title:** Black sans-serif, medium weight, slightly larger
- **Stage titles:** White sans-serif, bold/semi-bold, centered in blue boxes
- **Body text:** Black/dark grey sans-serif, regular weight, smaller
- **Parenthetical notes:** Italicized, slightly smaller than body
- **Font family:** Clean sans-serif (Arial, Helvetica, or similar)

### Visual Principles

- Minimalist, uncluttered
- Generous white space
- No gradients, shadows, or complex illustrations
- Corporate, professional, highly legible
- Text-based with geometric shapes only

---

## Prompt Template for GenerateImage

When calling GenerateImage, use this structure. Replace placeholders with actual content.

### For Stage/Progression Diagrams (like 4-stages)

```
Professional management book diagram. [N]-stage progression from left to right in stair-step layout. Each stage: solid dark blue rounded rectangle with white bold title; white rounded rectangle below with black body text and italic parenthetical note. Thin blue arrows connecting stages. Very light grey background. Main title at top left in black sans-serif. Minimalist, corporate, no icons. Clean geometric shapes only.
```

### For Flowcharts or Process Diagrams

```
Professional management book diagram. Flowchart with dark blue rounded rectangles for key nodes, white rectangles for descriptions. Thin blue arrows showing flow. Very light grey background. Black sans-serif text. Minimalist, corporate style. No icons or illustrations.
```

### For Framework or Model Diagrams

```
Professional management book diagram. [Framework name] framework. Dark blue title boxes, white description boxes, rounded corners. Thin blue connecting arrows. Very light grey background. Clean sans-serif typography. Minimalist corporate style suitable for executive audience.
```

---

## Content Structure (Per Stage/Box)

When generating multi-stage diagrams, each stage should have:

1. **Title** — Short, bold label (goes in blue box)
2. **Description** — One sentence or bullet points (goes in white box)
3. **Parenthetical** — Optional note in italics, e.g., "(Key consideration or capability)"

---

## Example: Adapting for New Content

**User request:** "Create a 3-stage diagram for AI adoption readiness"

**Prompt to use:**
```
Professional management book diagram. 3-stage progression from left to right in stair-step layout. Stage 1: "Assessment" - blue box; "Evaluate current capabilities and gaps" - white box; "(Baseline metrics, stakeholder mapping)" - italic. Stage 2: "Pilot" - blue box; "Run controlled experiments with agentic tools" - white box; "(Proof of value, learning cycles)" - italic. Stage 3: "Scale" - blue box; "Expand across functions with governance" - white box; "(Operating model redesign)" - italic. Thin blue arrows between stages. Very light grey background. Main title "AI adoption readiness" at top left. Minimalist, corporate, no icons.
```

---

## Editable Diagrams (React Components)

For editable, version-controlled diagrams, use the React component approach:

- **Location:** `diagrams/` — React components + config files
- **Edit:** Change `src/diagrams/*.js` for content; `src/StageDiagram.jsx` for style
- **Export:** `cd diagrams && npm run export` → writes SVG to `images/`
- **Add diagram:** Create new config in `src/diagrams/`, add to `src/export.js` DIAGRAMS array

See [diagrams/README.md](../diagrams/README.md) for full instructions.

---

## Reference

- **Editable source:** `diagrams/` — React components for SVG export
- **Book context:** European CEO AI transformation book, executive audience, ~100 pages

---

## Summary

1. Use **GenerateImage** when diagrams are requested.
2. **Save to `images/`** — use filename `images/[descriptive-name].png`; create folder if needed.
3. Apply the style spec: muted blue + white, rounded rectangles, stair-step layout.
4. Use the prompt templates; adapt placeholders for the specific content.
5. Keep diagrams minimalist—geometric shapes, no icons, generous white space.
6. Match the corporate, professional tone of the 4-stages reference.
