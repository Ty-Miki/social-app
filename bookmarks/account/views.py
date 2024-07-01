from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request,
                  "account/dashboard.html",
                  {"section": "dashboard"})