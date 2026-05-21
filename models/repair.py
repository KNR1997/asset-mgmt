from dataclasses import dataclass


@dataclass
class Repair:
    id: int
    asset_id: str
    checkout_id: str
    repair_date: str
    repair_cost: str
    status: int
    description: int
    notes: int
    performed_by: int
    warranty_covered: int
