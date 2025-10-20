from __future__ import annotations
from typing import List
from random import randint, random, choice
from ..models import CarListing, SearchRequest
from ..utils.reliability import estimate_reliability

MAKES_MODELS = [
    ("Toyota", ["Camry", "Corolla", "Prius", "Supra"]),
    ("Honda", ["Civic", "Accord", "Fit", "S2000"]),
    ("Ford", ["Mustang", "Focus", "F-150", "Fusion"]),
    ("BMW", ["3 Series", "5 Series", "M3", "M4"]),
    ("Chevrolet", ["Camaro", "Malibu", "Impala", "Corvette"]),
    ("Subaru", ["Impreza", "WRX", "Outback", "Forester"]),
]


class MockProvider:
    name = "mock"

    def search(self, query: SearchRequest) -> List[CarListing]:
        # Generate synthetic listings within basic constraints
        results: List[CarListing] = []
        for i in range(40):
            make, models = choice(MAKES_MODELS)
            model = choice(models)
            year = randint(2005, 2024)
            horsepower = randint(90, 600)
            base_price = randint(4000, 95000)
            price = float(base_price)
            reliability = estimate_reliability(make, year)

            # Basic filtering according to query
            if query.price_min is not None and price < query.price_min:
                continue
            if query.price_max is not None and price > query.price_max:
                continue
            if query.horsepower_min is not None and horsepower < query.horsepower_min:
                continue
            if query.reliability_min is not None and reliability < query.reliability_min:
                continue

            listing = CarListing(
                id=f"mock-{i}",
                title=f"{year} {make} {model}",
                make=make,
                model=model,
                year=year,
                price=price,
                mileage=randint(5000, 180000),
                horsepower=horsepower,
                reliability_score=reliability,
                location=query.location,
                url=None,
                vin=None,
                source=self.name,
                image_url=None,
            )
            results.append(listing)
        return results
