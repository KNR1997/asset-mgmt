from dataclasses import dataclass
from typing import Optional


@dataclass
class Model:
    id: int
    name: str
    modelNumber: str
    description: str
    category_id: Optional[int]
    category_name: Optional[str]
