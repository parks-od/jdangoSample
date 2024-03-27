from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.models import Asset


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    qs = Asset.objects.all()

    return render(
        request,
        "app/index.html",
        {
            "asset_list": qs,
        },
    )
