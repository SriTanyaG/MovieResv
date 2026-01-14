from django.contrib import admin
from .models import Theater, Screen, Movie, Show

admin.site.register(Theater)
admin.site.register(Screen)
admin.site.register(Movie)
admin.site.register(Show)