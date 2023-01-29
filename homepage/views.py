from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "title": "District Blossoms Water Polo Club",
    }
    return render(request, "homepage.html", context)

