from __future__ import annotations
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict


class CarListing(BaseModel):
    id: str
    title: str
    make: str
    model: str
    year: int
    price: Optional[float] = None
    mileage: Optional[int] = None
    horsepower: Optional[int] = None
    reliability_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    location: Optional[str] = None
    url: Optional[HttpUrl] = None
    vin: Optional[str] = None
    source: str
    image_url: Optional[HttpUrl] = None


class TrianglePoint(BaseModel):
    # Barycentric coordinates (cost, performance, reliability) summing to 1
    cost: float
    performance: float
    reliability: float


class ListingWithPlacement(BaseModel):
    listing: CarListing
    placement: TrianglePoint
    score: float
    summary: Optional[str] = None


class NormalizationInfo(BaseModel):
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    horsepower_min: Optional[int] = None
    horsepower_max: Optional[int] = None


class SearchRequest(BaseModel):
    location: str
    radius_km: int = 50

    # Cost filter
    price_min: Optional[float] = None
    price_max: Optional[float] = None

    # Performance filter
    horsepower_min: Optional[int] = None

    # Reliability filter
    reliability_min: Optional[float] = None

    # User preference point inside the triangle (weights sum to 1)
    desired: TrianglePoint = TrianglePoint(cost=0.33, performance=0.33, reliability=0.34)

    # Whether to include AI summaries in results
    include_summaries: bool = False


class SearchResponse(BaseModel):
    results: List[ListingWithPlacement]
    normalization: NormalizationInfo
    total: int
    providers_used: List[str]
