from django.shortcuts import render

# Create your views here.
def events(request):
    context = {}
    return render(request, "soon.html", context)