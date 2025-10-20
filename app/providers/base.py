from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ..models import CarListing, SearchRequest


class Provider(ABC):
    name: str

    @abstractmethod
    def search(self, query: SearchRequest) -> List[CarListing]:
        raise NotImplementedError
