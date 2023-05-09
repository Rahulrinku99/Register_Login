from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=="POST" and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            NSUO.set_password(ufd.cleaned_data['password'])
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()

            send_mail('Registration',
                      'successfully Registration is Done',
                      '7829794470rahul@gamil.com',
                      [NSUO.email],
                      fail_silently=False)
            return HttpResponse('Registration is Successfully')
        else:
            return HttpResponse('Not Valid')

    return render(request,'registration.html',d) 

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render (request,'home.html',d)
    return render(request,'home.html')


def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')
    return render(request,'signup.html')    


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=="POST":
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()

        send_mail('Registration',
                      'successfully Registration is Done',
                      '7829794470rahul@gamil.com',
                      [UO.email],
                      fail_silently=False)
        
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=="POST":
        un=request.POST['un']
        pw=request.POST['pw']
        UO=User.objects.filter(username=un)
        if UO :
            LUO=UO[0]
            LUO.set_password(pw)
            LUO.save()
            return HttpResponse('password reset successfully')
        else:
            return HttpResponse('user is not present in DB')
        
        
    return render(request,'forgot_password.html')