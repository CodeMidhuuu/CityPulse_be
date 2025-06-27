from django.contrib import admin
from django.utils.html import format_html
from .models import CivicIssue, UserProfile

@admin.register(CivicIssue)
class CivicIssueAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'status', 'reported_at', 'user_phone_number', 'location_link')

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'user_phone_number')
        }),
        ('Issue Details', {
            'fields': ('category', 'custom_category', 'subject', 'description')
        }),
        ('Location Data', {
            'fields': ('location', 'latitude', 'longitude', 'google_maps_link')
        }),
        ('Media', {
            'fields': ('media',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

    readonly_fields = ('google_maps_link', 'reported_at', 'user_phone_number')

    def user_phone_number(self, obj):
        try:
            return obj.user.userprofile.phone_number
        except UserProfile.DoesNotExist:
            return "Not available"

    user_phone_number.short_description = "Phone Number"

    def google_maps_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">📍 Open in Google Maps</a>', url)
        return "Coordinates not available"
    
    google_maps_link.short_description = "Map Link"

    def location_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">View Location</a>', url)
        return "-"

    location_link.short_description = "Location"