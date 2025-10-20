from __future__ import annotations
from typing import List, Optional
import re
import httpx

from ..models import CarListing, SearchRequest
from ..utils.reliability import estimate_reliability

CAR_MAKES = [
    "Toyota", "Honda", "Subaru", "Ford", "Chevrolet", "BMW", "Audi", "Mercedes", "Nissan", "Hyundai",
    "Kia", "Volkswagen", "Volvo", "Mazda", "Lexus", "Acura", "Infiniti", "Porsche", "Jaguar", "Mini",
]

PRICE_RE = re.compile(r"\$\s*([0-9][0-9,]*)")
YEAR_RE = re.compile(r"(19\d{2}|20\d{2})")
HP_RE = re.compile(r"(\d{2,4})\s*(?:hp|horsepower)", re.IGNORECASE)


class SerpApiProvider:
    name = "serpapi"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _parse_price(self, text: str) -> Optional[float]:
        m = PRICE_RE.search(text)
        if not m:
            return None
        try:
            return float(m.group(1).replace(",", ""))
        except Exception:
            return None

    def _parse_year(self, text: str) -> Optional[int]:
        m = YEAR_RE.search(text)
        if not m:
            return None
        year = int(m.group(1))
        if 1990 <= year <= 2026:
            return year
        return None

    def _parse_make_model(self, title: str) -> tuple[Optional[str], Optional[str]]:
        make = None
        for mk in CAR_MAKES:
            if re.search(rf"\b{re.escape(mk)}\b", title, re.IGNORECASE):
                make = mk
                break
        model = None
        if make:
            # naive: take words after make
            parts = title.split()
            try:
                idx = next(i for i, w in enumerate(parts) if w.lower() == make.lower())
                if idx + 1 < len(parts):
                    model = parts[idx + 1].strip("-,:|•·•\u00b7")
            except StopIteration:
                pass
        return make, model

    def search(self, query: SearchRequest) -> List[CarListing]:
        q_parts = [
            "(site:cars.com OR site:carvana.com OR site:autotrader.com OR site:cargurus.com OR site:autotempest.com)",
            f"\"{query.location}\"",
            "\"for sale\"",
        ]
        if query.price_min is not None:
            q_parts.append(f"${int(query.price_min)}+")
        if query.price_max is not None:
            q_parts.append(f"under ${int(query.price_max)}")
        if query.horsepower_min is not None:
            q_parts.append(f"{int(query.horsepower_min)} hp")

        q = " ".join(q_parts)
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google",
            "q": q,
            "num": 20,
            "api_key": self.api_key,
            "hl": "en",
            "safe": "active",
        }
        listings: List[CarListing] = []

        with httpx.Client(timeout=12.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            org = data.get("organic_results", [])
            for i, r in enumerate(org):
                title: str = r.get("title", "")
                link: str = r.get("link", "")
                snippet: str = r.get("snippet", "")
                thumb: Optional[str] = r.get("thumbnail")

                year = self._parse_year(title) or self._parse_year(snippet) or 2020
                make, model = self._parse_make_model(title)
                price = self._parse_price(title) or self._parse_price(snippet)
                hp_match = HP_RE.search(title) or HP_RE.search(snippet)
                horsepower = int(hp_match.group(1)) if hp_match else None

                if not make:
                    # skip if we can't identify make; prevents bad matches
                    continue

                reliability = estimate_reliability(make, year)

                listings.append(
                    CarListing(
                        id=f"serpapi-{i}",
                        title=title,
                        make=make,
                        model=model or "",
                        year=year,
                        price=price,
                        mileage=None,
                        horsepower=horsepower,
                        reliability_score=reliability,
                        location=query.location,
                        url=link,
                        vin=None,
                        source=self.name,
                        image_url=thumb,
                    )
                )

        return listings
