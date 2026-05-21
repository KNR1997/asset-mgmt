from dataclasses import dataclass


@dataclass
class License:
    id: int
    softwareName: str
    categoryName: str
    seats: int
