from dataclasses import dataclass


@dataclass
class Repair:
    id: int
    repair_date: str
    repair_cost: str
    status: int
    description: int
    notes: int
    performed_by: int
    warranty_covered: int

    asset_id: str
    asset_tag: str
    asset_serial_number: str
    asset_model_name: str
    asset_category_name: str
    checkout_id: str
