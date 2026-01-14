from rest_framework import serializers
from .models import Theater, Screen, Movie, Show
from django.urls import reverse

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScreenSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and hasattr(request.user, 'role') and request.user.role == 'theater_owner':
            self.fields['theater'].queryset = Theater.objects.filter(owner=request.user)

class TheaterSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, read_only=True)
    
    class Meta:
        model = Theater
        fields = ('id', 'owner', 'name', 'location', 'screens')
        read_only_fields = ('owner',)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'owner', 'title', 'description', 'duration_minutes', 'release_date')
        read_only_fields = ('owner',)

class ShowSerializer(serializers.ModelSerializer):
    movie_name = serializers.ReadOnlyField(source='movie.title')
    theater_name = serializers.ReadOnlyField(source='screen.theater.name')
    screen_name = serializers.ReadOnlyField(source='screen.name')
    book_url = serializers.SerializerMethodField()
    manage_show_url = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ('id', 'movie', 'movie_name', 'screen', 'screen_name', 'theater_name', 'date', 'time', 'price', 'book_url', 'manage_show_url')

    def get_book_url(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'customer':
            return request.build_absolute_uri(reverse('booking-list')) + f"?show={obj.id}"
        return None

    def get_manage_show_url(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'theater_owner':
            return request.build_absolute_uri(reverse('show-detail', kwargs={'pk': obj.pk}))
        return None

    def validate(self, data):
        screen = data.get('screen')
        date = data.get('date')
        time = data.get('time')

        # Check for existing shows on the SAME screen at the SAME time
        overlapping_shows = Show.objects.filter(
            screen=screen,
            date=date,
            time=time
        )

        # If we are UPDATING an existing show, exclude it from the check
        if self.instance:
            overlapping_shows = overlapping_shows.exclude(pk=self.instance.pk)

        if overlapping_shows.exists():
            raise serializers.ValidationError(
                f"Conflict: {screen.name} is already booked for another movie on {date} at {time}."
            )

        return data

    def __init__(self, *args, **kwargs):
        super(ShowSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and hasattr(request.user, 'role') and request.user.role == 'theater_owner':
            if 'screen' in self.fields:
                self.fields['screen'].queryset = Screen.objects.filter(theater__owner=request.user)
            if 'movie' in self.fields:
                self.fields['movie'].queryset = Movie.objects.filter(owner=request.user)
