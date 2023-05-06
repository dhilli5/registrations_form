from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from app.forms import *
from django.core.mail import send_mail


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
            return HttpResponse("registration successfully")
        
        else:
            return HttpResponse("data not valid")  
    return render(request,'registration.html',d)       
    