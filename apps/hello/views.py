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


def about(request):
    return render(request, "hello/about.html")


def contact(request):
    return render(request, "hello/contact.html")


def hello_there(request, name):
    return render(
        request, "hello/hello_there.html", {"name": name, "date": timezone.now()}
    )


def log_message(request):
    """Render and process the log message form.

    The view renders the form on GET and renders the form with errors on
    invalid POST. On valid POST it saves and redirects to `home`.
    """
    form = LogMessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)
        message.log_date = timezone.now()
        message.save()
        return redirect("home")

    return render(request, "hello/log_message.html", {"form": form})
