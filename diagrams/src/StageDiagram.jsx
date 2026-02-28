/**
 * StageDiagram — Editable React component for 4-stages-style book diagrams.
 * Renders a stair-step progression of stages with blue title boxes and white description boxes.
 * Matches input/4-stages.png style guide.
 */

import React from "react";

// Style constants (from input/4-stages.png)
const STYLE = {
  background: "#F7F9FC",
  primaryBlue: "#3F51B5",
  arrowBlue: "#7B8AB8",
  textDark: "#1F2937",
  textMuted: "#6B7280",
  textWhite: "#FFFFFF",
  borderRadius: 6,
  padding: 12,
  boxWidth: 180,
  titleHeight: 44,
  descMinHeight: 60,
  arrowGap: 24,
  stepHeight: 40, // Vertical rise per stage (stair-step)
};

/**
 * Renders a single stage (blue title box + white description box).
 */
function Stage({ data, x, y }) {
  const { title, description, parenthetical } = data;

  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* Blue title box */}
      <rect
        x={0}
        y={0}
        width={STYLE.boxWidth}
        height={STYLE.titleHeight}
        rx={STYLE.borderRadius}
        ry={STYLE.borderRadius}
        fill={STYLE.primaryBlue}
      />
      <text
        x={STYLE.boxWidth / 2}
        y={STYLE.titleHeight / 2 + 5}
        textAnchor="middle"
        fill={STYLE.textWhite}
        fontFamily="Arial, Helvetica, sans-serif"
        fontSize={13}
        fontWeight="bold"
      >
        {title}
      </text>

      {/* White description box */}
      <rect
        x={0}
        y={STYLE.titleHeight + 4}
        width={STYLE.boxWidth}
        height={STYLE.descMinHeight}
        rx={STYLE.borderRadius}
        ry={STYLE.borderRadius}
        fill={STYLE.textWhite}
        stroke="#E5E7EB"
        strokeWidth={0.5}
      />
      <text
        x={STYLE.padding}
        y={STYLE.titleHeight + 4 + STYLE.padding + 12}
        fill={STYLE.textDark}
        fontFamily="Arial, Helvetica, sans-serif"
        fontSize={11}
      >
        {description.split("\n").map((line, i) => (
          <tspan key={i} x={STYLE.padding} dy={i === 0 ? 0 : 14}>
            {line}
          </tspan>
        ))}
      </text>
      {parenthetical && (
        <text
          x={STYLE.padding}
          y={STYLE.titleHeight + 4 + STYLE.padding + 28}
          fill={STYLE.textMuted}
          fontFamily="Arial, Helvetica, sans-serif"
          fontSize={10}
          fontStyle="italic"
        >
          {parenthetical}
        </text>
      )}
    </g>
  );
}

/**
 * Renders an arrow between two stages (stair-step connector).
 */
function Arrow({ fromX, fromY, toX, toY }) {
  const midX = (fromX + toX) / 2;
  const path = `M ${fromX} ${fromY} L ${midX} ${fromY} L ${midX} ${toY} L ${toX} ${toY}`;

  return (
    <g>
      <path
        d={path}
        fill="none"
        stroke={STYLE.arrowBlue}
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Arrowhead */}
      <polygon
        points={`${toX - 8},${toY - 4} ${toX - 8},${toY + 4} ${toX},${toY}`}
        fill={STYLE.arrowBlue}
      />
    </g>
  );
}

/**
 * StageDiagram — Main component.
 * @param {Object} props
 * @param {string} props.title — Main diagram title (top left)
 * @param {Array<{title: string, description: string, parenthetical?: string}>} props.stages
 */
export default function StageDiagram({ title, stages }) {
  const stageWidth = STYLE.boxWidth + STYLE.arrowGap;
  const totalWidth = stages.length * stageWidth - STYLE.arrowGap + 80;
  const maxStageY = (stages.length - 1) * STYLE.stepHeight;
  const totalHeight = 80 + maxStageY + STYLE.titleHeight + STYLE.descMinHeight + 40;

  const stagePositions = stages.map((_, i) => ({
    x: 40 + i * stageWidth,
    y: 50 + i * STYLE.stepHeight,
  }));

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={totalWidth}
      height={totalHeight}
      viewBox={`0 0 ${totalWidth} ${totalHeight}`}
    >
      {/* Background */}
      <rect width={totalWidth} height={totalHeight} fill={STYLE.background} />

      {/* Main title */}
      <text
        x={40}
        y={32}
        fill={STYLE.textDark}
        fontFamily="Arial, Helvetica, sans-serif"
        fontSize={16}
        fontWeight="600"
      >
        {title}
      </text>

      {/* Arrows between stages */}
      {stages.length > 1 &&
        stagePositions.slice(0, -1).map((pos, i) => (
          <Arrow
            key={i}
            fromX={pos.x + STYLE.boxWidth}
            fromY={pos.y + STYLE.titleHeight / 2}
            toX={stagePositions[i + 1].x}
            toY={stagePositions[i + 1].y + STYLE.titleHeight / 2}
          />
        ))}

      {/* Stages */}
      {stages.map((stage, i) => (
        <Stage key={i} data={stage} x={stagePositions[i].x} y={stagePositions[i].y} />
      ))}
    </svg>
  );
}
