from dataclasses import dataclass
from typing import Optional


@dataclass
class License:
    id: int
    softwareName: str
    categoryName: str
    seats: int
    minQuantity: int
    productKey: str
    licensedTo: str
    licensedToEmail: str
    orderNumber: str
    purchaseCost: int
    purchaseDate: str
    expirationDate: str
    terminationDate: str
    notes: str
    manufacturer_id: Optional[int]
    manufacturer_name: Optional[str]
