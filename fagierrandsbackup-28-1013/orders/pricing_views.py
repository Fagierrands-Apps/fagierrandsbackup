"""
Pricing API endpoints
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .pricing import calculate_distance_price, calculate_shopping_total, get_pricing_info
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class PricingCalculatorView(APIView):
    """
    Calculate order price based on type and distance
    Endpoint: POST /api/orders/pricing/calculate/
    """
    permission_classes = [permissions.AllowAny]  # Frontend needs this before login
    
    def post(self, request):
        """
        Calculate price for an order
        
        Body:
        {
            "order_type": "delivery" | "cargo" | "shopping",
            "distance": 15.5,
            "shopping_items": [{"price": 100, "quantity": 2}]  // optional for shopping
        }
        """
        order_type = request.data.get('order_type', '').lower()
        distance = request.data.get('distance', 0)
        
        if not order_type or not distance:
            return Response({
                'error': 'order_type and distance are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            distance = Decimal(str(distance))
            
            if order_type == 'shopping':
                shopping_items = request.data.get('shopping_items', [])
                result = calculate_shopping_total(shopping_items, distance)
                return Response({
                    'order_type': order_type,
                    'distance_km': float(distance),
                    'items_total': float(result['items_total']),
                    'delivery_fee': float(result['delivery_fee']),
                    'total_price': float(result['total']),
                    'currency': 'KSh'
                })
            else:
                price = calculate_distance_price(order_type, distance)
                return Response({
                    'order_type': order_type,
                    'distance_km': float(distance),
                    'total_price': float(price),
                    'currency': 'KSh'
                })
                
        except Exception as e:
            logger.error(f"Price calculation error: {e}")
            return Response({
                'error': f'Calculation error: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class PricingInfoView(APIView):
    """
    Get pricing information for all order types
    Endpoint: GET /api/orders/pricing/info/
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """
        Get pricing rules for all order types
        """
        return Response({
            'pricing_rules': {
                'delivery': get_pricing_info('delivery'),
                'cargo': get_pricing_info('cargo'),
                'shopping': get_pricing_info('shopping'),
                'banking': get_pricing_info('banking'),
            },
            'note': 'All prices in KSh (Kenyan Shillings)'
        })
