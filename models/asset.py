from dataclasses import dataclass
from typing import Optional


@dataclass
class Asset:
    id: int
    tag: str
    name: str
    serial_number: str
    model_name: Optional[str]
    category_name: Optional[str]
    status: str
    description: str
