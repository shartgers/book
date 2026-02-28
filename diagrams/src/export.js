/**
 * Export script — renders diagram configs to SVG files in images/.
 * Run: npm run export
 * Run with watch: npm run export:watch
 */

import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import { createElement } from "react";
import { writeFileSync, mkdirSync, existsSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

import StageDiagram from "./StageDiagram.jsx";

// Resolve images/ relative to project root (diagrams/ is one level down)
const __dirname = dirname(fileURLToPath(import.meta.url));
const IMAGES_DIR = join(__dirname, "..", "..", "images");

// Diagram configs: filename (without .svg) -> config module
const DIAGRAMS = [
  ["agentic-systems", () => import("./diagrams/agentic-systems.js")],
  ["ai-adoption-stages", () => import("./diagrams/ai-adoption-stages.js")],
];

async function exportAll() {
  // Ensure images/ exists
  if (!existsSync(IMAGES_DIR)) {
    mkdirSync(IMAGES_DIR, { recursive: true });
  }

  for (const [name, loadConfig] of DIAGRAMS) {
    const mod = await loadConfig();
    const config = mod.default;
    const svg = renderToStaticMarkup(
      createElement(StageDiagram, { title: config.title, stages: config.stages })
    );
    const outPath = join(IMAGES_DIR, `${name}.svg`);
    writeFileSync(outPath, `<?xml version="1.0" encoding="UTF-8"?>\n${svg}`, "utf8");
    console.log(`Exported: images/${name}.svg`);
  }
}

exportAll().catch((err) => {
  console.error(err);
  process.exit(1);
});
