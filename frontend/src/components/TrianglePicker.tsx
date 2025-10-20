import React, { useCallback, useMemo, useRef, useState } from 'react';
import type { TrianglePoint } from '../lib/api';

const SQRT3_OVER_2 = Math.sqrt(3) / 2;

export type TrianglePickerProps = {
  width?: number;
  height?: number;
  value: TrianglePoint;
  onChange: (v: TrianglePoint) => void;
};

// Map barycentric weights to 2D point
function baryToXY(b: TrianglePoint, w: number, h: number) {
  const pad = 16;
  const A = { x: pad, y: h - pad }; // Cost (left)
  const B = { x: w - pad, y: h - pad }; // Performance (right)
  const side = Math.min(w, h) - pad * 2;
  const C = { x: w / 2, y: h - pad - side * SQRT3_OVER_2 }; // Reliability (top)
  const x = b.cost * A.x + b.performance * B.x + b.reliability * C.x;
  const y = b.cost * A.y + b.performance * B.y + b.reliability * C.y;
  return { x, y, A, B, C };
}

// Convert 2D point back to barycentric (clamped to simplex)
function xyToBary(x: number, y: number, w: number, h: number): TrianglePoint {
  const pad = 16;
  const A = { x: pad, y: h - pad };
  const B = { x: w - pad, y: h - pad };
  const side = Math.min(w, h) - pad * 2;
  const C = { x: w / 2, y: h - pad - side * SQRT3_OVER_2 };

  const v0 = { x: B.x - A.x, y: B.y - A.y };
  const v1 = { x: C.x - A.x, y: C.y - A.y };
  const v2 = { x: x - A.x, y: y - A.y };

  const dot00 = v0.x * v0.x + v0.y * v0.y;
  const dot01 = v0.x * v1.x + v0.y * v1.y;
  const dot02 = v0.x * v2.x + v0.y * v2.y;
  const dot11 = v1.x * v1.x + v1.y * v1.y;
  const dot12 = v1.x * v2.x + v1.y * v2.y;

  const denom = dot00 * dot11 - dot01 * dot01;
  let v = (dot11 * dot02 - dot01 * dot12) / denom;
  let wght = (dot00 * dot12 - dot01 * dot02) / denom;
  let u = 1 - v - wght;

  // Clamp to simplex and renormalize
  u = Math.max(0, Math.min(1, u));
  v = Math.max(0, Math.min(1, v));
  wght = Math.max(0, Math.min(1, wght));
  const sum = u + v + wght || 1;
  return { cost: u / sum, performance: v / sum, reliability: wght / sum };
}

export default function TrianglePicker({ width = 320, height = 280, value, onChange }: TrianglePickerProps) {
  const [isDragging, setDragging] = useState(false);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const pos = useMemo(() => baryToXY(value, width, height), [value, width, height]);

  const handlePos = useCallback(
    (clientX: number, clientY: number) => {
      const rect = svgRef.current!.getBoundingClientRect();
      const x = clientX - rect.left;
      const y = clientY - rect.top;
      onChange(xyToBary(x, y, width, height));
    },
    [onChange, width, height]
  );

  const onMouseDown = (e: React.MouseEvent) => {
    setDragging(true);
    handlePos(e.clientX, e.clientY);
  };
  const onMouseMove = (e: React.MouseEvent) => {
    if (isDragging) handlePos(e.clientX, e.clientY);
  };
  const onMouseUp = () => setDragging(false);
  const onLeave = () => setDragging(false);

  const pad = 16;
  const side = Math.min(width, height) - pad * 2;
  const baseY = height - pad;
  const A = { x: pad, y: baseY };
  const B = { x: width - pad, y: baseY };
  const C = { x: width / 2, y: baseY - side * SQRT3_OVER_2 };

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      onMouseLeave={onLeave}
      style={{ cursor: 'pointer', userSelect: 'none', background: '#f1f5f9', borderRadius: 12, border: '1px solid #e2e8f0' }}
    >
      {/* Triangle */}
      <polygon points={`${A.x},${A.y} ${B.x},${B.y} ${C.x},${C.y}`} fill="#ffffff" stroke="#cbd5e1" strokeWidth={2} />
      {/* Grid */}
      {[0.25, 0.5, 0.75].map((t) => {
        const p1 = { x: A.x + (B.x - A.x) * t, y: A.y + (B.y - A.y) * t };
        const p2 = { x: A.x + (C.x - A.x) * t, y: A.y + (C.y - A.y) * t };
        const p3 = { x: B.x + (C.x - B.x) * t, y: B.y + (C.y - B.y) * t };
        return (
          <g key={t} stroke="#e2e8f0">
            <line x1={p1.x} y1={p1.y} x2={C.x - (C.x - A.x) * t} y2={C.y - (C.y - A.y) * t} />
            <line x1={p2.x} y1={p2.y} x2={B.x - (B.x - A.x) * t} y2={B.y - (B.y - A.y) * t} />
            <line x1={p3.x} y1={p3.y} x2={A.x - (A.x - B.x) * t} y2={A.y - (A.y - B.y) * t} />
          </g>
        );
      })}

      {/* Labels */}
      <text x={A.x} y={A.y + 16} fontSize={12} fill="#334155">Cost</text>
      <text x={B.x - 28} y={B.y + 16} fontSize={12} fill="#334155">Performance</text>
      <text x={C.x - 28} y={C.y - 8} fontSize={12} fill="#334155">Reliability</text>

      {/* Point */}
      <circle cx={pos.x} cy={pos.y} r={7} fill="#2563eb" stroke="#1d4ed8" strokeWidth={2} />
    </svg>
  );
}
