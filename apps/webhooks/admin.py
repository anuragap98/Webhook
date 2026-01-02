from django.contrib import admin
from .models import WebhookEndpoint, WebhookEvent


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "url", "is_active", "created_at", "last_used_at")
    list_filter = ("is_active", "user")
    search_fields = ("name", "url", "user__username")
    readonly_fields = ("created_at", "last_used_at")
    fieldsets = (
        (
            None,
            {"fields": ("user", "name", "url", "secret", "is_active", "description")},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "last_used_at"),
            },
        ),
    )


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "status", "created_at")
    list_filter = ("event_type", "status")
    readonly_fields = ("payload", "created_at")
