from django.contrib import admin

# Register your models here.
from .models import Trivia, UserScores

admin.site.register(Trivia)
admin.site.register(UserScores)