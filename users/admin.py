from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avg_result', 'testing_count', 'rating')
    list_filter = ('user', 'avg_result', 'testing_count')
