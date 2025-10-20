from __future__ import annotations
from typing import List, Tuple
from ..models import CarListing, SearchRequest
from ..config import settings
from ..providers.mock import MockProvider


def get_providers():
    providers = []
    if settings.enable_mock_provider:
        providers.append(MockProvider())
    # Real providers (optional)
    try:
        if settings.enable_serpapi_provider and settings.serpapi_key:
            from ..providers.serpapi import SerpApiProvider  # lazy import
            providers.append(SerpApiProvider(api_key=settings.serpapi_key))
    except Exception:
        # If provider import/init fails, skip it silently
        pass
    return providers


def aggregate(query: SearchRequest) -> Tuple[List[CarListing], List[str]]:
    results: List[CarListing] = []
    providers = get_providers()
    used: List[str] = []
    for provider in providers:
        try:
            res = provider.search(query)
            results.extend(res)
            used.append(getattr(provider, "name", provider.__class__.__name__))
        except Exception:
            # Skip failing provider (could add logging)
            continue
    return results, used
