from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView
from .forms import LogMessageForm
from .models import LogMessage


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""

    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def contact(request):
    return render(request, "blog/contact.html")


def log_message(request):
    """Render and process the log message form.

    The view renders the form on GET and renders the form with errors on
    invalid POST. On valid POST it saves and redirects to `home`.
    """
    form = LogMessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)
        # Save as UTC-aware datetime. Django will store datetimes in UTC when USE_TZ = True.
        # Convert to a local timezone only when presenting timestamps to users.
        message.log_date = timezone.now()
        message.save()
        # Redirect to the home view (named 'home') which lists recent messages
        return redirect("home")

    return render(request, "blog/log_message.html", {"form": form})
