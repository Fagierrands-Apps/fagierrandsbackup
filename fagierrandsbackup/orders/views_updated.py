# views_updated.py — stub file, original was removed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class _StubView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def post(self, request, *args, **kwargs):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)


OrderTrackingView = _StubView
TrackingWaypointListCreateView = _StubView
TrackingWaypointDetailView = _StubView
TrackingEventListCreateView = _StubView
TrackingEventDetailView = _StubView
TrackingLocationHistoryListView = _StubView
InitializeTrackingView = _StubView
