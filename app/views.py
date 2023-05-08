from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail

from django.http import HttpResponsePermanentRedirect
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
            return HttpResponsePermanentRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')
    return render(request,'signup.html')    


@login_required
def signout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse('home'))