# models_updated.py — stub file, original models were removed
# These are placeholder classes to prevent import errors
# TODO: Remove references to these across serializers.py, views.py, admin.py

from django.db import models


class _StubModel(models.Model):
    class Meta:
        abstract = True


class OrderTracking(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class TrackingWaypoint(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class TrackingEvent(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class TrackingLocationHistory(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class ClientFeedback(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class RiderFeedback(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class CargoPhoto(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class CargoValue(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class ReportIssue(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class Referral(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True


class OrderVideo(_StubModel):
    class Meta:
        app_label = 'orders'
        abstract = True
