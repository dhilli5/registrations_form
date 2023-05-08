from django.shortcuts import render
from django.core.mail import send_mail

from app.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

from app.forms import *
def home_page(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home_page.html',d)
    return render(request,'home_page.html')


def registration(request):  # sourcery skip: extract-method
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    
    if request.method=="POST" and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        
        
        if UFD.is_valid() and PFD.is_valid():
            NSUO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()
            
            
            NSPO=PFD.save(commit=False)
            NSPO.username=NSUO 
            NSPO.save()  
            send_mail('wish',
                      'good morning',
                      'sana11111999@gmail.com',
                      [NSUO.email],
                      fail_silently=True)

            
            return HttpResponse("registration successfully")
        
        else:
            return HttpResponse("data not valid")  
    return render(request,'registration.html',d) 


def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home_page'))
        else:
            return HttpResponse('Invalid username or password') 

    return render(request,'login_user.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    uo=User.objects.get(username=username)
    po=Profile.objects.get(username=uo)
    
    d={'uo':uo,"po":po}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=="POST":
        password=request.POST['password']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(password)
        uo.save()
        return HttpResponse("change password successfully")
        
    
    return render(request,'change_password.html')

def forget_password(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        
        uo=User.objects.get(username=username)
        uo.set_password(password)
        uo.save()
        
        return HttpResponse("password changed done")
    return render(request,'forget_password.html')
