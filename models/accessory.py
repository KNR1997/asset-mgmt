from dataclasses import dataclass


@dataclass
class Accessory:
    id: int
    accessoryName: str
    categoryName: str
    supplierName: str
    modelNumber: str
    minQuantity: int
    orderNumber: int
    unitCost: int
    purchaseDate: int
    qunatity: int
    notes: int
