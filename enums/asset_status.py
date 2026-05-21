from enum import Enum


class AssetStatus(str, Enum):
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"
    BROKEN = "Broken"
    ARCHIVED = "Archived"
    READY_TO_DEPLOY = "Ready to Deploy"
    PENDING = "Pending"
    LOST_STOLEN = "Lost/Stolen"
    OUT_FOR_DIAGNOSTICS = "Out for Diagnostics"
    OUT_FOR_REPAIR = "Out for Repair"
    DEPLOYED = "Deployed"
