from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TheaterViewSet, ScreenViewSet, MovieViewSet, ShowViewSet

router = DefaultRouter()
router.register(r'theaters', TheaterViewSet, basename='theater')
router.register(r'screens', ScreenViewSet, basename='screen')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'shows', ShowViewSet, basename='show')

urlpatterns = [
    path('', include(router.urls)),
]
