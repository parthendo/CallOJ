from django.shortcuts import render

def aboutview (request):
    return render(request, 'about.html')