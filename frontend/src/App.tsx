import React, { useMemo, useState } from 'react';
import TrianglePicker from './components/TrianglePicker';
import FiltersForm, { type Filters } from './components/FiltersForm';
import ResultItem from './components/ResultItem';
import { type ListingWithPlacement, type SearchResponse, type TrianglePoint, searchCars } from './lib/api';

const DEFAULT_TRI: TrianglePoint = { cost: 0.33, performance: 0.33, reliability: 0.34 };

export default function App() {
  const [desired, setDesired] = useState<TrianglePoint>(DEFAULT_TRI);
  const [filters, setFilters] = useState<Filters>({
    location: 'San Francisco, CA',
    radius_km: 50,
    price_min: null,
    price_max: null,
    horsepower_min: null,
    reliability_min: null,
    include_summaries: false,
  });
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function doSearch(values: Filters) {
    setFilters(values);
    setLoading(true);
    setError(null);
    try {
      const data = await searchCars({
        location: values.location,
        radius_km: values.radius_km,
        price_min: values.price_min ?? undefined,
        price_max: values.price_max ?? undefined,
        horsepower_min: values.horsepower_min ?? undefined,
        reliability_min: values.reliability_min ?? undefined,
        desired,
        include_summaries: values.include_summaries,
      });
      setResp(data);
    } catch (e: any) {
      setError(e?.message || 'Search failed');
    } finally {
      setLoading(false);
    }
  }

  const title = useMemo(() => {
    const parts = [] as string[];
    if (filters.price_min != null || filters.price_max != null) {
      parts.push(`$${filters.price_min?.toLocaleString?.() || '0'} - $${filters.price_max?.toLocaleString?.() || '∞'}`);
    }
    if (filters.horsepower_min != null) parts.push(`${filters.horsepower_min}+ hp`);
    if (filters.reliability_min != null) parts.push(`Reliability ≥ ${(filters.reliability_min * 100).toFixed(0)}%`);
    return parts.join(' · ');
  }, [filters]);

  return (
    <div className="container">
      <div className="header">
        <h2 style={{ margin: 0 }}>Car Finder</h2>
        <div className="small">Triangle of Cost, Performance, Reliability</div>
      </div>

      <div className="grid">
        <div style={{ display: 'grid', gap: 12 }}>
          <TrianglePicker value={desired} onChange={setDesired} />
          <div className="card small">
            Desired weights — C {desired.cost.toFixed(2)} · P {desired.performance.toFixed(2)} · R {desired.reliability.toFixed(2)}
          </div>
          <FiltersForm initial={filters} onSubmit={doSearch} />
        </div>

        <div style={{ display: 'grid', gap: 12 }}>
          <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <div style={{ fontWeight: 700 }}>Results</div>
              <div className="small">{filters.location} · {title || 'No extra filters'}{resp ? ` · ${resp.total} matches` : ''}</div>
            </div>
            <div>
              <button className="btn" onClick={() => doSearch(filters)} disabled={loading}>{loading ? 'Searching…' : 'Search'}</button>
            </div>
          </div>

          {error && <div className="card" style={{ color: '#b91c1c' }}>{error}</div>}

          <div className="results">
            {resp?.results.map((item: ListingWithPlacement) => (
              <ResultItem key={`${item.listing.source}:${item.listing.id}`} item={item} />
            ))}
          </div>

          {resp && (
            <div className="card small">Providers used: {resp.providers_used.join(', ') || 'None'}</div>
          )}
        </div>
      </div>
    </div>
  );
}
