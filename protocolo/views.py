from django.shortcuts import render

# Create your views here.


def protocolo(request):
    return render(request, 'protocolo.html')
