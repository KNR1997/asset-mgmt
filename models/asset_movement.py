from dataclasses import dataclass


@dataclass
class AssetMovement:
    checkout_id: int
    asset_id: int
    asset_tag: str
    asset_name: str
    model_name: str
    category_name: str
    employee_id: int
    employee_name: str
    checkout_date: str
    expected_checkin_date: str
    actual_checkin_date: str
    is_active: bool
    return_condition: str
    checkout_notes: str
    return_notes: str
