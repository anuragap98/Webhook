from django import forms
from .models import LogMessage


class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)  # NOTE: the trailing comma is required
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your message here",
                    "rows": 6,
                }
            )
        }
