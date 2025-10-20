import axios from 'axios';

export type TrianglePoint = {
  cost: number;
  performance: number;
  reliability: number;
};

export type CarListing = {
  id: string;
  title: string;
  make: string;
  model: string;
  year: number;
  price?: number | null;
  mileage?: number | null;
  horsepower?: number | null;
  reliability_score?: number | null;
  location?: string | null;
  url?: string | null;
  vin?: string | null;
  source: string;
  image_url?: string | null;
};

export type ListingWithPlacement = {
  listing: CarListing;
  placement: TrianglePoint;
  score: number;
  summary?: string | null;
};

export type NormalizationInfo = {
  price_min?: number | null;
  price_max?: number | null;
  horsepower_min?: number | null;
  horsepower_max?: number | null;
};

export type SearchRequest = {
  location: string;
  radius_km?: number;
  price_min?: number | null;
  price_max?: number | null;
  horsepower_min?: number | null;
  reliability_min?: number | null;
  desired: TrianglePoint;
  include_summaries?: boolean;
};

export type SearchResponse = {
  results: ListingWithPlacement[];
  normalization: NormalizationInfo;
  total: number;
  providers_used: string[];
};

const API_BASE = (import.meta.env.VITE_API_BASE as string) || '';

export async function searchCars(req: SearchRequest): Promise<SearchResponse> {
  const { data } = await axios.post<SearchResponse>(`${API_BASE}/api/search`, req, {
    headers: { 'Content-Type': 'application/json' },
  });
  return data;
}
