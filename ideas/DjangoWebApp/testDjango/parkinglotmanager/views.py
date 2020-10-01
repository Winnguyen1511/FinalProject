from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
@permission_required("parkinglotmanager.view_history")
@permission_required("parkinglotmanager.view_parkinglotlist")
@permission_required("parkinglotmanager.view_parking")
def index(request):
    return render(request, 'parkinglotmanager/index.html')

@login_required
def edit(request):
    return render(request, 'parkinglotmanager/edit.html')