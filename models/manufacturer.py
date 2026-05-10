from dataclasses import dataclass


@dataclass
class Manufacturer:
    id: int
    name: str
    url: str
    supportURL: str
    supportPhone: str
    warrantyLookupUrl: str
    supportEmail: str
    notes: str
