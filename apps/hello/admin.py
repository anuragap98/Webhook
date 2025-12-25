from django.contrib import admin
from .models import LogMessage


@admin.register(LogMessage)
class LogMessageAdmin(admin.ModelAdmin):
    list_display = ("message", "log_date")
    ordering = ("-log_date",)
