import React, { useState } from 'react';

export type Filters = {
  location: string;
  radius_km: number;
  price_min?: number | null;
  price_max?: number | null;
  horsepower_min?: number | null;
  reliability_min?: number | null;
  include_summaries: boolean;
};

export default function FiltersForm({ initial, onSubmit }: { initial: Filters; onSubmit: (f: Filters) => void }) {
  const [values, setValues] = useState<Filters>(initial);
  function change<K extends keyof Filters>(key: K, val: Filters[K]) {
    setValues((v) => ({ ...v, [key]: val }));
  }

  return (
    <form
      className="card"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(values);
      }}
    >
      <div style={{ display: 'grid', gap: 8 }}>
        <div>
          <div className="label">Location</div>
          <input placeholder="City, State" value={values.location} onChange={(e) => change('location', e.target.value)} />
        </div>
        <div>
          <div className="label">Search radius (km)</div>
          <input type="number" value={values.radius_km} onChange={(e) => change('radius_km', Number(e.target.value || 0))} />
        </div>
        <div className="row">
          <div>
            <div className="label">Min price</div>
            <input type="number" placeholder="e.g. 5000" value={values.price_min ?? ''} onChange={(e) => change('price_min', e.target.value ? Number(e.target.value) : null)} />
          </div>
          <div>
            <div className="label">Max price</div>
            <input type="number" placeholder="e.g. 20000" value={values.price_max ?? ''} onChange={(e) => change('price_max', e.target.value ? Number(e.target.value) : null)} />
          </div>
        </div>
        <div className="row">
          <div>
            <div className="label">Min horsepower</div>
            <input type="number" placeholder="e.g. 200" value={values.horsepower_min ?? ''} onChange={(e) => change('horsepower_min', e.target.value ? Number(e.target.value) : null)} />
          </div>
          <div>
            <div className="label">Min reliability (0.0 - 1.0)</div>
            <input type="number" step="0.01" min={0} max={1} placeholder="e.g. 0.7" value={values.reliability_min ?? ''} onChange={(e) => change('reliability_min', e.target.value ? Number(e.target.value) : null)} />
          </div>
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <input type="checkbox" checked={values.include_summaries} onChange={(e) => change('include_summaries', e.target.checked)} />
          Include AI summaries
        </label>
        <div>
          <button className="btn" type="submit">Search</button>
        </div>
      </div>
    </form>
  );
}
