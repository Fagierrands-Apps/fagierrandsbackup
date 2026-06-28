"""
Server-side price calculation and validation
Prevents client-side price manipulation
"""
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Pricing constants (server-side source of truth)
PRICING_RULES = {
    'delivery': {
        'base_price': Decimal('200.00'),
        'free_distance_km': Decimal('7.5'),
        'price_per_km': Decimal('23.00'),
    },
    'cargo': {
        'base_price': Decimal('500.00'),
        'free_distance_km': Decimal('7.5'),
        'price_per_km': Decimal('28.00'),
    },
    'shopping': {
        'base_price': Decimal('200.00'),
        'free_distance_km': Decimal('7.5'),
        'price_per_km': Decimal('23.00'),
    },
    'banking': {
        'base_price': Decimal('0.00'),  # No distance charges
        'free_distance_km': Decimal('0.00'),
        'price_per_km': Decimal('0.00'),
    },
}


def calculate_distance_price(order_type_name, distance_km):
    """
    Calculate price based on order type and distance
    
    Args:
        order_type_name: 'delivery', 'cargo', 'shopping', 'banking'
        distance_km: Distance in kilometers (Decimal or float)
    
    Returns:
        Decimal: Calculated price
    """
    order_type_name = order_type_name.lower()
    
    if order_type_name not in PRICING_RULES:
        logger.warning(f"Unknown order type: {order_type_name}, using delivery pricing")
        order_type_name = 'delivery'
    
    rules = PRICING_RULES[order_type_name]
    distance = Decimal(str(distance_km))
    
    # Base price for first X km
    base_price = rules['base_price']
    free_distance = rules['free_distance_km']
    price_per_km = rules['price_per_km']
    
    # Calculate additional distance charges
    if distance <= free_distance:
        total_price = base_price
    else:
        additional_distance = distance - free_distance
        total_price = base_price + (additional_distance * price_per_km)
    
    logger.info(f"Calculated price: {order_type_name} {distance}km = KSh {total_price}")
    
    return total_price


def calculate_shopping_total(items, distance_km):
    """
    Calculate shopping order total (items + delivery)
    
    Args:
        items: List of shopping items with 'price' and 'quantity'
        distance_km: Distance in kilometers
    
    Returns:
        dict: {'items_total', 'delivery_fee', 'total'}
    """
    items_total = Decimal('0.00')
    
    for item in items:
        item_price = Decimal(str(item.get('price', 0)))
        quantity = int(item.get('quantity', 1))
        items_total += item_price * quantity
    
    delivery_fee = calculate_distance_price('shopping', distance_km)
    total = items_total + delivery_fee
    
    return {
        'items_total': items_total,
        'delivery_fee': delivery_fee,
        'total': total
    }


def validate_order_price(order_data, tolerance_percent=2):
    """
    Validate client-provided price against server calculation
    
    Args:
        order_data: Dict with 'order_type', 'distance', 'price', optional 'shopping_items'
        tolerance_percent: Allow X% variance for rounding differences
    
    Returns:
        dict: {'valid': bool, 'calculated_price': Decimal, 'error': str}
    
    Raises:
        ValueError: If price manipulation detected
    """
    order_type = order_data.get('order_type', '')
    distance = Decimal(str(order_data.get('distance', 0)))
    client_price = Decimal(str(order_data.get('price', 0)))
    
    # Calculate server-side price
    if order_type.lower() == 'shopping':
        shopping_items = order_data.get('shopping_items', [])
        calc = calculate_shopping_total(shopping_items, distance)
        calculated_price = calc['total']
    else:
        calculated_price = calculate_distance_price(order_type, distance)
    
    # Check if client price matches server price (with tolerance)
    tolerance = calculated_price * (Decimal(str(tolerance_percent)) / 100)
    price_diff = abs(calculated_price - client_price)
    
    if price_diff > tolerance:
        error_msg = (
            f"Price manipulation detected! "
            f"Client sent: KSh {client_price}, "
            f"Server calculated: KSh {calculated_price} "
            f"(difference: KSh {price_diff})"
        )
        logger.error(error_msg)
        return {
            'valid': False,
            'calculated_price': calculated_price,
            'error': error_msg
        }
    
    return {
        'valid': True,
        'calculated_price': calculated_price,
        'error': None
    }


def get_pricing_info(order_type_name):
    """
    Get pricing information for an order type
    
    Returns:
        dict: Pricing rules for the order type
    """
    order_type_name = order_type_name.lower()
    
    if order_type_name not in PRICING_RULES:
        order_type_name = 'delivery'
    
    rules = PRICING_RULES[order_type_name]
    
    return {
        'order_type': order_type_name,
        'base_price': float(rules['base_price']),
        'free_distance_km': float(rules['free_distance_km']),
        'price_per_km': float(rules['price_per_km']),
        'example': f"KSh {rules['base_price']} for first {rules['free_distance_km']}km, "
                   f"then KSh {rules['price_per_km']}/km"
    }
