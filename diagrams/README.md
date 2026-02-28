# Book Diagrams — Editable 4-Stages Style

React components that generate SVG diagrams in the book's visual style. Edit the config files and export to `images/`.

## Quick Start

```bash
cd diagrams
npm install
npm run export
```

Output: `images/agentic-systems.svg`, `images/ai-adoption-stages.svg`

## Adding a New Diagram

1. Create `src/diagrams/your-diagram-name.js`:

```js
export default {
  title: "Your diagram title",
  stages: [
    { title: "Stage 1", description: "Description.", parenthetical: "(Note)" },
    { title: "Stage 2", description: "Description.", parenthetical: "(Note)" },
  ],
};
```

2. Add it to `src/export.js` in the `DIAGRAMS` array:

```js
["your-diagram-name", () => import("./diagrams/your-diagram-name.js")],
```

3. Run `npm run export`

## Editing

- **Content:** Edit the `.js` files in `src/diagrams/`
- **Style:** Edit `STYLE` constants in `src/StageDiagram.jsx`
- **Layout:** Adjust `boxWidth`, `stepHeight`, etc. in `StageDiagram.jsx`

## Watch Mode

```bash
npm run export:watch
```

Rebuilds on file changes. Run `node dist/export.js` after edits to regenerate images.
