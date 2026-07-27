"""
Query optimization utilities for better database performance
"""
from functools import wraps
from django.core.cache import cache
from django.db.models import Prefetch
import hashlib
import json


def cache_queryset(timeout=300, key_prefix='qs'):
    """
    Decorator to cache queryset results
    Usage: @cache_queryset(timeout=600)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and args
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args).encode()).hexdigest()}"
            
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator


def optimize_order_queryset(queryset):
    """
    Optimize Order queryset with all necessary relations
    """
    return queryset.select_related(
        'client',
        'assistant',
        'order_type'
    ).prefetch_related(
        'shopping_items',
        'orderimage_set',
        'orderattachment_set'
    ).only(
        'id', 'title', 'status', 'price', 'created_at', 'updated_at',
        'pickup_address', 'delivery_address',
        'client__id', 'client__first_name', 'client__last_name',
        'assistant__id', 'assistant__first_name', 'assistant__last_name',
        'order_type__name'
    )


def bulk_update_optimized(model, objs, fields, batch_size=500):
    """
    Optimized bulk update with batching
    """
    from django.db import transaction
    
    with transaction.atomic():
        model.objects.bulk_update(objs, fields, batch_size=batch_size)


def get_cached_count(queryset, cache_key, timeout=300):
    """
    Get cached count for expensive count queries
    """
    count = cache.get(cache_key)
    if count is None:
        count = queryset.count()
        cache.set(cache_key, count, timeout)
    return count
