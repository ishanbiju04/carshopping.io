import React from 'react';
import type { ListingWithPlacement } from '../lib/api';

function MiniTriangle({ w = 80, h = 70, weights }: { w?: number; h?: number; weights: { cost: number; performance: number; reliability: number } }) {
  const pad = 6;
  const A = { x: pad, y: h - pad };
  const B = { x: w - pad, y: h - pad };
  const C = { x: w / 2, y: pad };
  const x = weights.cost * A.x + weights.performance * B.x + weights.reliability * C.x;
  const y = weights.cost * A.y + weights.performance * B.y + weights.reliability * C.y;
  return (
    <svg width={w} height={h} style={{ background: '#f8fafc', borderRadius: 8, border: '1px solid #e2e8f0' }}>
      <polygon points={`${A.x},${A.y} ${B.x},${B.y} ${C.x},${C.y}`} fill="#fff" stroke="#cbd5e1" />
      <circle cx={x} cy={y} r={5} fill="#2563eb" />
    </svg>
  );
}

export default function ResultItem({ item }: { item: ListingWithPlacement }) {
  const l = item.listing;
  return (
    <div className="card item">
      <div>
        {l.image_url ? <img src={l.image_url} alt={l.title} /> : <div style={{ width: 120, height: 90, background: '#e2e8f0', borderRadius: 8 }} />}
      </div>
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
          <div>
            <div style={{ fontWeight: 800 }}>{l.title}</div>
            <div className="small">{l.location || ''}</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontWeight: 700 }}>{l.price != null ? `$${Math.round(l.price).toLocaleString()}` : 'Price N/A'}</div>
            <div className="small">{l.horsepower ? `${l.horsepower} hp` : 'hp N/A'} · {l.reliability_score != null ? `Rel ${(l.reliability_score * 100).toFixed(0)}%` : 'Rel N/A'}</div>
          </div>
        </div>
        <div className="triRow" style={{ marginTop: 8 }}>
          <MiniTriangle weights={item.placement} />
          <div className="small">
            C {item.placement.cost.toFixed(2)} · P {item.placement.performance.toFixed(2)} · R {item.placement.reliability.toFixed(2)}
          </div>
        </div>
        {item.summary && <div className="summary" style={{ marginTop: 8 }}>{item.summary}</div>}
        <div className="footer">
          <span className="badge">{l.source}</span>
          {l.url && (
            <a className="badge" href={l.url} target="_blank" rel="noreferrer">View listing</a>
          )}
        </div>
      </div>
    </div>
  );
}
