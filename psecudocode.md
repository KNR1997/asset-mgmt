START

DISPLAY "Input asset details: name, tag, serialNumber, description, status, purchaseDate, purchaseCost, select mode"
INPUT name, tag, serialNumber, description, status, purchaseDate, purchaseCost, mode

// Validation
IF name IS NULL OR tag IS NULL OR serialNumber IS NULL THEN
    DISPLAY "Show validation error message: Required fields missing"
    END
END IF

IF purchaseDate IS INVALID OR purchaseCost < 0 THEN
    DISPLAY "Show validation error message: Invalid date or cost"
    END
END IF

IF tag ALREADY EXISTS OR serialNumber ALREADY EXISTS THEN
    DISPLAY "Show validation error message: Duplicate tag or serial number"
    END
END IF

// Create asset
INSERT INTO assets (name, tag, serialNumber, description, status, purchaseDate, purchaseCost, mode)
VALUES (name, tag, serialNumber, description, status, purchaseDate, purchaseCost, mode)

DISPLAY "Success message: Asset created successfully"

END

-------------------------------------------------------------------

START

DISPLAY "Select Asset"
INPUT asset_id

FETCH asset FROM database WHERE asset.id = asset_id

IF asset NOT FOUND THEN
    DISPLAY "Asset not found"
    END
END IF

DISPLAY "Input updated details: name, tag, serialNumber, description, status, purchaseDate, purchaseCost, select mode"
INPUT name, tag, serialNumber, description, status, purchaseDate, purchaseCost, mode

// Validation
IF name IS NULL OR tag IS NULL OR serialNumber IS NULL THEN
    DISPLAY "Show validation error message: Required fields missing"
    END
END IF

IF purchaseDate IS INVALID OR purchaseCost < 0 THEN
    DISPLAY "Show validation error message: Invalid date or cost"
    END
END IF

IF (tag != asset.tag AND tag ALREADY EXISTS IN OTHER ASSET) OR
   (serialNumber != asset.serialNumber AND serialNumber ALREADY EXISTS IN OTHER ASSET) THEN
    DISPLAY "Show validation error message: Duplicate tag or serial number"
    END
END IF

// Update asset
UPDATE assets 
SET name = name, tag = tag, serialNumber = serialNumber, 
    description = description, status = status, 
    purchaseDate = purchaseDate, purchaseCost = purchaseCost, mode = mode
WHERE id = asset_id

DISPLAY "Success message: Asset updated successfully"

END

--------------------------------------------------

START

DISPLAY "Select Asset"
INPUT asset_id

FETCH asset FROM database WHERE asset.id = asset_id

IF asset.status != "ready_to_deploy" THEN
    DISPLAY "Show Asset is not ready to deploy error message"
    END
END IF

DISPLAY "Select employee, Input asset_name, notes, expected_checkin_date"
INPUT employee_id, asset_name, notes, expected_checkin_date

// Validation
IF employee_id NOT EXISTS IN employees THEN
    DISPLAY "Show validation error message: Employee not found"
    END
END IF

IF expected_checkin_date < CURRENT_DATE THEN
    DISPLAY "Show validation error message: Expected check-in date cannot be in past"
    END
END IF

// Checkout asset
UPDATE assets 
SET status = "deployed", 
    checked_out_to = employee_id,
    checkout_date = CURRENT_DATE,
    expected_checkin_date = expected_checkin_date,
    checkout_notes = notes
WHERE id = asset_id

INSERT INTO checkout_records (asset_id, employee_id, checkout_date, expected_checkin_date, notes)
VALUES (asset_id, employee_id, CURRENT_DATE, expected_checkin_date, notes)

DISPLAY "Create checkout record: Success"

END

--------------------------------------------------------

START

DISPLAY "Select Asset"
INPUT asset_id

FETCH asset FROM database WHERE asset.id = asset_id

IF asset.status != "deployed" THEN
    DISPLAY "Show Asset is not checked out yet"
    END
END IF

DISPLAY "Select Asset current condition, Input checkin date, notes"
INPUT condition, checkin_date, notes

// Validation
IF condition IS NULL OR condition IS EMPTY THEN
    DISPLAY "Show validation error message: Condition is required"
    END
END IF
IF checkin_date IS INVALID OR checkin_date > CURRENT_DATE THEN
    DISPLAY "Show validation error message: Check-in date invalid or in future"
    END
END IF
IF checkin_date < asset.checkout_date THEN
    DISPLAY "Show validation error message: Check-in date cannot be before checkout date"
    END
END IF

// Checkin asset
UPDATE assets 
SET status = "available", 
    last_checkin_date = checkin_date,
    current_condition = condition,
    checkin_notes = notes,
    checked_out_to = NULL,
    expected_checkin_date = NULL
WHERE id = asset_id

UPDATE checkout_records 
SET checkin_date = checkin_date, 
    checkin_condition = condition,
    checkin_notes = notes
WHERE asset_id = asset_id AND checkin_date IS NULL
DISPLAY "Update Asset status: Available"
END

---------------

START

DISPLAY "Select Broken Asset"
INPUT asset_id

FETCH asset FROM database WHERE asset.id = asset_id

IF asset.status != "broken" THEN
    DISPLAY "Asset is not marked as broken"
    END
END IF

DISPLAY "Input repair_date, repair_cost, notes, performed_by, warranty_covered"
INPUT repair_date, repair_cost, notes, performed_by, warranty_covered

// Validation
IF repair_date IS INVALID OR repair_date > CURRENT_DATE THEN
    DISPLAY "Show validation error message: Invalid repair date"
    END
END IF

IF repair_cost < 0 THEN
    DISPLAY "Show validation error message: Repair cost cannot be negative"
    END
END IF

IF performed_by IS NULL THEN
    DISPLAY "Show validation error message: Performed by is required"
    END
END IF

// Create repair record
INSERT INTO maintenance_records (asset_id, repair_date, repair_cost, notes, performed_by, warranty_covered)
VALUES (asset_id, repair_date, repair_cost, notes, performed_by, warranty_covered)

// Update asset status
UPDATE assets 
SET status = "ready_to_deploy",
    last_maintenance_date = repair_date
WHERE id = asset_id

DISPLAY "Update Asset status: Ready to Deploy"

END

--------------------------

START

DISPLAY "Select consumable"
INPUT consumable_id

FETCH consumable FROM database WHERE consumable.id = consumable_id

DISPLAY "Input requested quantity"
INPUT requested_qty

IF consumable.quantity < requested_qty THEN
    DISPLAY "Show not enough message: Only X units available"
    END
END IF

DISPLAY "Input employee_id, consumable_quantity, notes"
INPUT employee_id, consumable_quantity, notes

// Validation
IF employee_id NOT EXISTS IN employees THEN
    DISPLAY "Show validation error message: Employee not found"
    END
END IF

IF consumable_quantity <= 0 THEN
    DISPLAY "Show validation error message: Quantity must be positive"
    END
END IF

IF consumable_quantity > consumable.quantity THEN
    DISPLAY "Show validation error message: Not enough stock"
    END
END IF

// Update consumable quantity
UPDATE consumables 
SET quantity = quantity - consumable_quantity
WHERE id = consumable_id

// Create release record
INSERT INTO consumable_releases (consumable_id, employee_id, quantity, release_date, notes)
VALUES (consumable_id, employee_id, consumable_quantity, CURRENT_DATE, notes)

DISPLAY "Create consumable release record: Success"

END

----------------------

START

DISPLAY "Input date range for maintenance records"
INPUT start_date, end_date

// Validation
IF start_date IS NULL OR end_date IS NULL THEN
    DISPLAY "Show validation error message: Both dates required"
    END
END IF

IF start_date > end_date THEN
    DISPLAY "Show validation error message: Start date cannot be after end date"
    END
END IF

IF end_date > CURRENT_DATE THEN
    DISPLAY "Show validation error message: End date cannot be in future"
    END
END IF

// Filter records
SELECT * FROM maintenance_records 
WHERE maintenance_date BETWEEN start_date AND end_date

DISPLAY "Filtered maintenance records"

DISPLAY "Click download? (Yes/No)"
INPUT download_choice

IF download_choice = "Yes" THEN
    EXPORT filtered_records TO CSV format
    TRIGGER file download
    DISPLAY "Process CSV report: Download started"
ELSE
    DISPLAY "Report generation cancelled"
END IF

END