from __future__ import annotations
from typing import Optional
from ..models import CarListing, TrianglePoint
from ..config import settings

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


def generate_fallback_summary(listing: CarListing, placement: TrianglePoint) -> str:
    traits: list[str] = []
    if listing.price is not None:
        traits.append(f"priced around ${int(listing.price):,}")
    if listing.horsepower is not None:
        traits.append(f"~{listing.horsepower} hp")
    if listing.reliability_score is not None:
        traits.append(f"reliability ~{int(listing.reliability_score*100)}%")
    tri = f"C:{placement.cost:.2f} / P:{placement.performance:.2f} / R:{placement.reliability:.2f}"
    parts = ", ".join(traits) if traits else "key specs unavailable"
    return f"{listing.title} emphasizes triangle {tri}; {parts}."


def generate_ai_summary(listing: CarListing, placement: TrianglePoint) -> str:
    if not settings.openai_api_key or OpenAI is None:
        return generate_fallback_summary(listing, placement)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "You are helping a user choose a used car using a triangle of Cost, Performance, Reliability. "
        "Given the listing details and the car's placement weights that sum to 1, write a crisp 1-2 sentence summary "
        "highlighting strengths and explaining why the car sits near those triangle sides. Avoid fluff."
    )
    content = (
        f"Listing: {listing.title}\n"
        f"Make: {listing.make}, Model: {listing.model}, Year: {listing.year}\n"
        f"Price: {listing.price}, Horsepower: {listing.horsepower}, Reliability: {listing.reliability_score}\n"
        f"Triangle placement (Cost, Performance, Reliability): {placement.cost:.2f}, {placement.performance:.2f}, {placement.reliability:.2f}\n"
    )
    try:
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content},
            ],
            max_tokens=90,
            temperature=0.4,
        )
        return (resp.choices[0].message.content or "").strip() or generate_fallback_summary(listing, placement)
    except Exception:
        return generate_fallback_summary(listing, placement)
