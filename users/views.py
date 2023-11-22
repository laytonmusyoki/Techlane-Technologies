from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from myapp.models import Customer
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group


# Create your views here.
def register(request):
    form=RegistrationForm
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User=form.save()
            group=Group.objects.get(name='customer')
            User.groups.add(group)
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            Customer.objects.create(
                user=User,
                name=User.username,
                email=User.email,
            )
            return redirect('signin')
    context={
        "forms":form
    }
    return render(request,'register.html',context)



def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'Welcome back {username}')
            if request.user.groups.filter(name='customer').exists():
                return redirect('index')
            else:
                return redirect('all_products')
    return render(request,'login.html')



def signout(request):
    logout(request)
    messages.warning(request,'You have been logged out')
    return redirect('index')