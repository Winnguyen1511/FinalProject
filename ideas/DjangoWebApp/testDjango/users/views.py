from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserRegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been registered! You are now able to login.')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')