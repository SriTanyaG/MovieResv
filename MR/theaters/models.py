from django.db import models
from django.conf import settings
from django.utils import timezone

class Theater(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='theaters')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='screens')
    name = models.CharField(max_length=100) # e.g., Screen 1, IMAX
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.theater.name} - {self.name}"

class Movie(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies', null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} at {self.screen.name} ({self.date} {self.time})"
