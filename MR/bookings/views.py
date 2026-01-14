from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer

class DenyAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Hide the POST form on the main list page (where ?show= is missing)
        if self.action == 'create' and 'show' not in self.request.query_params:
            return [DenyAll()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'theater_owner':
            return Booking.objects.filter(show__screen__theater__owner=user)
        return Booking.objects.filter(user=user)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        # Pre-fill the 'show' field in the HTML form if show ID is in URL
        if self.request.method == 'GET' and 'show' in self.request.query_params:
            show_id = self.request.query_params.get('show')
            # Check if it is a single serializer (has 'fields') and not a ListSerializer
            if hasattr(serializer, 'fields') and 'show' in serializer.fields:
                serializer.fields['show'].initial = show_id
        return serializer

    def perform_create(self, serializer):
        show = serializer.validated_data['show']
        seats = serializer.validated_data['seats_booked']
        total_price = show.price * seats
        serializer.save(user=self.request.user, total_price=total_price)
