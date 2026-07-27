# Order Export Feature

## Overview
This feature allows exporting order information to Excel format (.xlsx) for easy data management and reporting.

## Installation

Add `openpyxl` to your requirements:
```bash
pip install openpyxl
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### API Endpoint

**Export Single Order**
```
GET /api/orders/<order_id>/export/
```

**Authentication Required:** Yes

**Permissions:** 
- Order client
- Assigned assistant
- Assigned handler
- Admin users

**Response:** Excel file download (.xlsx)

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://your-domain.com/api/orders/123/export/ \
  -o order_123.xlsx
```

### Django Admin

1. Navigate to Django Admin → Orders
2. Select one or more orders using checkboxes
3. Choose "Export selected orders to Excel" from the Actions dropdown
4. Click "Go"
5. Excel file will be downloaded automatically

## Excel File Contents

### Single Order Export
Contains detailed information about the order:
- Order ID, Title, Description
- Order Type and Status
- Client information (name, phone)
- Assistant and Handler details
- Pickup and Delivery addresses
- Contact information (recipient, alternative contact)
- Pricing details (price, items total, estimated value)
- Distance and duration
- Timestamps (created, assigned, started, completed, cancelled)

### Bulk Export (Admin)
Contains summary information for multiple orders:
- ID, Title
- Client, Assistant
- Order Type, Status
- Price
- Pickup/Delivery addresses
- Contact number
- Created and Completed timestamps

## Security

- Authentication required for all export operations
- Users can only export orders they have access to:
  - Clients can export their own orders
  - Assistants can export assigned orders
  - Handlers can export orders they manage
  - Admins can export any order

## Technical Details

**Files:**
- `orders/export_views.py` - API view for single order export
- `orders/admin.py` - Admin action for bulk export
- `orders/urls.py` - URL routing

**Dependencies:**
- openpyxl - Excel file generation
- Django REST Framework - API views
- Django Admin - Bulk export action

## Error Handling

- Returns 404 if order not found
- Returns 403 if user lacks permission
- Returns 500 for unexpected errors
- All errors are logged for debugging
