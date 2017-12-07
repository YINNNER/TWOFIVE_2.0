# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,render_to_response
from . forms import RegisterForm,LoginForm
from django.contrib.auth import  authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
import json
from TWOFIVE.settings import MEDIA_ROOT
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
    request.session.set_expiry(0)
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

# 发布
@login_required
def publish(request):
    if request.method == 'POST':
        text=request.POST.get('text')
    return redirect('/memory/homepage')

@login_required
def browsing(request):
    return render(request,'browsing.html')

@login_required
def album(request):
    return render(request,'album.html')

def settings(request):
    return render(request,'settings.html')

def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html')

# 传个人简介和用户名给homepage
def ajax_name(request):
    username={'name':'ha'}
    # return JsonResponse(username)
    return HttpResponse(json.dumps(username),content_type='application/json')

def upload_file(request,filename):
    if request.method =='POST':
        myFile=request.FILES.get(filename,None) #获取用户上传文件，若没有则为None
        if not myFile:
            return False
        print MEDIA_ROOT
        destination=open(os.path.join(MEDIA_ROOT,request.user.username+'_portrait.png'),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
            destination.close()
            return True


def user_setting(request):
    if request.method=='POST':
        if request.POST.get('nickname')!=request.user.nickname:
            request.user.nickname=request.POST.get('nickname')
        if request.POST.get('title') != request.user.title:
            request.user.title=request.POST.get('title')
        portrait=request.POST.get('portrait')
        request.user.save()
        if portrait != '':
            isuploaded=upload_file(request,'portrait')
            if isuploaded == True:
                is_success={'is_success':'success'}
                return HttpResponse(json.dumps(is_success), content_type='application/json')
            else:
                is_success = {'is_success': 'failure'}
                return HttpResponse(json.dumps(is_success), content_type='application/json')
        is_success={'is_success':'success'}
        return HttpResponse(json.dumps(is_success), content_type='application/json')


