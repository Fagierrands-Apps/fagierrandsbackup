#!/usr/bin/env python
"""
Test price validation to ensure manipulation is blocked
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fagierrandsbackup.settings')
django.setup()

from orders.pricing import calculate_distance_price, validate_order_price
from decimal import Decimal

print("=== PRICE VALIDATION TESTS ===\n")

# Test 1: Normal delivery pricing
print("Test 1: Normal Delivery (10km)")
price = calculate_distance_price('delivery', 10)
print(f"  Calculated: KSh {price}")
print(f"  Expected: KSh 200 + (10-7.5) × 23 = KSh 257.50")
print(f"  ✅ PASS" if price == Decimal('257.50') else f"  ❌ FAIL")
print()

# Test 2: Cargo pricing
print("Test 2: Cargo Delivery (15km)")
price = calculate_distance_price('cargo', 15)
print(f"  Calculated: KSh {price}")
print(f"  Expected: KSh 500 + (15-7.5) × 28 = KSh 710.00")
print(f"  ✅ PASS" if price == Decimal('710.00') else f"  ❌ FAIL")
print()

# Test 3: Short distance (within free range)
print("Test 3: Short Delivery (5km - within free range)")
price = calculate_distance_price('delivery', 5)
print(f"  Calculated: KSh {price}")
print(f"  Expected: KSh 200 (base price only)")
print(f"  ✅ PASS" if price == Decimal('200.00') else f"  ❌ FAIL")
print()

# Test 4: Price manipulation detection
print("Test 4: Price Manipulation Detection")
fake_order = {
    'order_type': 'delivery',
    'distance': 20,
    'price': 50  # Client trying to pay KSh 50 for 20km delivery!
}
validation = validate_order_price(fake_order)
print(f"  Client sent: KSh 50")
print(f"  Server calculated: KSh {validation['calculated_price']}")
print(f"  Valid: {validation['valid']}")
print(f"  ✅ BLOCKED" if not validation['valid'] else "  ❌ FAIL - SHOULD BLOCK")
print()

# Test 5: Valid price (should pass)
print("Test 5: Valid Price (should accept)")
valid_order = {
    'order_type': 'delivery',
    'distance': 20,
    'price': 487.50  # Correct: 200 + (20-7.5)×23
}
validation = validate_order_price(valid_order)
print(f"  Client sent: KSh 487.50")
print(f"  Server calculated: KSh {validation['calculated_price']}")
print(f"  Valid: {validation['valid']}")
print(f"  ✅ PASS" if validation['valid'] else "  ❌ FAIL - SHOULD ACCEPT")
print()

# Test 6: Extreme manipulation
print("Test 6: Extreme Manipulation (KSh 1 for 50km cargo)")
extreme_fake = {
    'order_type': 'cargo',
    'distance': 50,
    'price': 1
}
validation = validate_order_price(extreme_fake)
print(f"  Client sent: KSh 1")
print(f"  Server calculated: KSh {validation['calculated_price']}")
print(f"  Potential loss: KSh {validation['calculated_price'] - Decimal('1')}")
print(f"  ✅ BLOCKED" if not validation['valid'] else "  ❌ FAIL - HUGE RISK")
print()

print("=== ALL TESTS COMPLETE ===")
