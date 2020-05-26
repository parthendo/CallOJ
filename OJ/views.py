from django.shortcuts import render

def aboutview1 (request):
    return render(request, 'about1.html')

def aboutview2 (request):
    return render(request, 'about2.html')

def aboutview3 (request):
    return render(request, 'about3.html')