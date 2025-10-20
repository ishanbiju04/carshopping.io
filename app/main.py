from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os

from .config import settings
from .models import SearchRequest, SearchResponse, ListingWithPlacement
from .services.aggregator import aggregate
from .services.scoring import compute_normalization, listing_to_barycentric, score_against_preference
from .services.summary import generate_ai_summary

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}


@app.post("/api/search", response_model=SearchResponse)
async def search(req: SearchRequest) -> SearchResponse:
    listings, providers_used = aggregate(req)
    norm = compute_normalization(listings)

    items: List[ListingWithPlacement] = []
    for l in listings:
        placement = listing_to_barycentric(l, norm)
        score = score_against_preference(placement, req.desired)
        items.append(
            ListingWithPlacement(
                listing=l,
                placement=placement,
                score=score,
            )
        )

    # Optionally attach summaries
    if req.include_summaries:
        for item in items:
            item.summary = generate_ai_summary(item.listing, item.placement)

    # Sort by score descending
    items.sort(key=lambda x: x.score, reverse=True)

    return SearchResponse(
        results=items,
        normalization=norm,
        total=len(items),
        providers_used=providers_used,
    )


# Serve built frontend if available (frontend/dist). Try a few common locations.
def _try_mount_frontend() -> None:
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"),  # repo root sibling
        os.path.join(os.getcwd(), "frontend", "dist"),  # CWD/frontend/dist
    ]
    for path in candidates:
        abs_path = os.path.abspath(path)
        if os.path.isdir(abs_path):
            app.mount("/", StaticFiles(directory=abs_path, html=True), name="static")
            return


try:
    _try_mount_frontend()
except Exception:
    # Frontend not built yet; ignore
    pass
