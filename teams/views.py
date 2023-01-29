from django.shortcuts import render

# Create your views here.
def teams(request):
    context = {}
    return render(request, "soon.html", context)