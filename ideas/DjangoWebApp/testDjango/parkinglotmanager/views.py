from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'parkinglotmanager/index.html')

def edit(request):
    return render(request, 'parkinglotmanager/edit.html')