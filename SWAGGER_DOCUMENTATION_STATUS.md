# 📚 Swagger Documentation Status

## Current Status: ❌ NO SWAGGER DOCUMENTATION

**Files checked:**
- accounts/views.py: 0 decorators
- orders/views.py: 0 decorators
- marketplace/views.py: 0 decorators
- notifications/views.py: 0 decorators
- locations/views.py: 0 decorators
- admin_dashboard/views.py: 0 decorators

## What's Needed

Every API endpoint needs:
1. `@swagger_auto_schema()` decorator
2. Request body schema (for POST/PUT/PATCH)
3. Query parameters documentation
4. Response schema
5. Example responses

## Priority Endpoints to Document

### 🔴 CRITICAL (Auth & Core):
1. **accounts/views.py**
   - POST `/api/auth/register/` - User registration
   - POST `/api/auth/login/` - User login
   - POST `/api/auth/logout/` - User logout
   - GET `/api/users/profile/` - Get user profile
   - PUT `/api/users/profile/` - Update profile

2. **orders/views.py**
   - POST `/api/orders/` - Create order
   - GET `/api/orders/` - List orders
   - GET `/api/orders/{id}/` - Get order details
   - PATCH `/api/orders/{id}/` - Update order
   - POST `/api/orders/{id}/accept/` - Accept order

### 🟡 IMPORTANT (Payments & Marketplace):
3. **orders/views.py (payments)**
   - POST `/api/payments/ncba/qr/initiate/` - Initiate QR payment
   - POST `/api/payments/ncba/qr/callback/` - Payment callback
   - GET `/api/payments/{id}/status/` - Check payment status

4. **marketplace/views.py**
   - GET `/api/marketplace/items/` - List items
   - POST `/api/marketplace/items/` - Create item
   - GET `/api/marketplace/items/{id}/` - Item details

### 🟢 NICE TO HAVE:
5. **notifications/views.py**
6. **locations/views.py**
7. **admin_dashboard/views.py**

## Recommendation

**Option 1 - Full Documentation (Recommended for Production)**
Add swagger decorators to ALL endpoints (~100+ endpoints)
Time: 3-4 hours

**Option 2 - Critical Only (Quick Fix)**
Document only the 20 most used endpoints
Time: 1 hour

**Option 3 - Auto-generate (Fast but Less Detailed)**
Use DRF's built-in schema generation
Time: 30 minutes

## Current Swagger URL

Once documented, Swagger UI will be available at:
- Render: https://fagierrandsbackup.onrender.com/swagger/
- cPanel: https://fagierrandsbackup.fagierrands.com/swagger/

## Next Steps

Choose an option and I'll implement it. For now, the API works but lacks
interactive documentation in Swagger UI.

**What would you like to do?**
1. Document ALL endpoints (3-4 hours)
2. Document 20 critical endpoints (1 hour)
3. Use auto-generation (30 min)
