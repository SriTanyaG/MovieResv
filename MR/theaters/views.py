from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Theater, Screen, Movie, Show
from .serializers import TheaterSerializer, ScreenSerializer, MovieSerializer, ShowSerializer

class IsTheaterOwnerStrict(permissions.BasePermission):
    """
    Strict permission: Only theater owners can access (even for viewing).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'theater_owner'

class CanViewShowsOnly(permissions.BasePermission):
    """
    Allows everyone to view (GET), but only theater owners can modify.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'theater_owner'

class TheaterViewSet(viewsets.ModelViewSet):
    serializer_class = TheaterSerializer
    permission_classes = [IsTheaterOwnerStrict]

    def get_queryset(self):
        return Theater.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ScreenViewSet(viewsets.ModelViewSet):
    serializer_class = ScreenSerializer
    permission_classes = [IsTheaterOwnerStrict]

    def get_queryset(self):
        return Screen.objects.filter(theater__owner=self.request.user)

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsTheaterOwnerStrict]

    def get_queryset(self):
        return Movie.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ShowViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSerializer
    permission_classes = [CanViewShowsOnly]
    filterset_fields = ['movie', 'screen__theater', 'date', 'time']

    def get_queryset(self):
        return Show.objects.all()
