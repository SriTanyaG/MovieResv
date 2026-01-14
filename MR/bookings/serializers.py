from rest_framework import serializers
from .models import Booking
from theaters.models import Show
from django.urls import reverse

class BookingSerializer(serializers.ModelSerializer):
    show_details = serializers.ReadOnlyField(source='show.__str__')
    movie_name = serializers.ReadOnlyField(source='show.movie.title')
    theater_name = serializers.ReadOnlyField(source='show.screen.theater.name')
    cancel_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ('id', 'show', 'movie_name', 'theater_name', 'show_details', 'seats_booked', 'total_price', 'booked_at', 'cancel_url')
        read_only_fields = ('total_price', 'booked_at')

    def __init__(self, *args, **kwargs):
        super(BookingSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        # If a specific show is requested in the URL, filter the dropdown to ONLY that show
        if request and request.method == 'GET' and 'show' in request.query_params:
            show_id = request.query_params.get('show')
            if 'show' in self.fields:
                self.fields['show'].queryset = Show.objects.filter(pk=show_id)

    def get_cancel_url(self, obj):
        request = self.context.get('request')
        if request:
            # Generates the direct URL to the booking detail (where the DELETE button is)
            return request.build_absolute_uri(reverse('booking-detail', kwargs={'pk': obj.pk}))
        return None

    def validate(self, data):
        show = data['show']
        seats = data['seats_booked']
        
        # Check current user role - only customers can book
        user = self.context['request'].user
        if user.role != 'customer':
            raise serializers.ValidationError("Only customers can book tickets.")

        # Standard seat availability check
        booked_seats = sum(b.seats_booked for b in show.bookings.all())
        available_seats = show.screen.total_seats - booked_seats
        
        if seats > available_seats:
            raise serializers.ValidationError(f"Only {available_seats} seats available. Total capacity: {show.screen.total_seats}")
        
        return data
