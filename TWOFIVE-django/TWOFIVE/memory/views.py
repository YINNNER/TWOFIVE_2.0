# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,render_to_response
from . forms import RegisterForm,LoginForm
from django.contrib.auth import  authenticate,login,logout
from django.http import HttpResponse
from models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    redirect_to=request.POST.get('next',request.GET.get('next',''))
    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form=RegisterForm()
    else:
        form = RegisterForm()
    return form

@login_required
def homepage(request):
    return render(request,'homepage.html')


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/memory/homepage')
    login_form = LoginForm()
    if request.method == 'POST':
        submit=request.POST.get('submit')

        if submit=='login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    # return homepage(request)
                    return redirect('/memory/homepage')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        elif submit=='regist':
            regist_form=register(request)
            is_registed=False
            if regist_form != None:
                is_registed=True
            return render(request,'registration/login.html',context={'login_form':login_form,'form':regist_form,'is_registed':is_registed})
    else:
        regist_form=register(request)
        return render(request,'registration/login.html',context={'login_form':login_form,'form':regist_form})

@login_required
def writing(request):
    return render(request,'writing.html')

@login_required
def publish(request):
    return redirect('/memory/homepage')

@login_required
def browsing(request):
    return render(request,'browsing.html')

@login_required
def album(request):
    return render(request,'album.html')

def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html')