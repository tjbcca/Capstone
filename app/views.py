from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def checks(request):
    return render(request, 'checks.html')