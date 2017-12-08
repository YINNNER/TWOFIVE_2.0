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
from PIL import Image,ImageFile
from TWOFIVE.settings import MEDIA_ROOT,MEDIA_URL
ImageFile.LOAD_TRUNCATED_IMAGES = True
# Create your views here.
# 注冊
def register(request):
    redirect_to=request.POST.get('next',request.GET.get('next',''))
    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.portrait_url=os.path.join(MEDIA_URL,'default.png')
            form.save()
            form=RegisterForm()
    else:
        form = RegisterForm()
    return form

# 主頁
@login_required
def homepage(request):
    return render(request,'homepage.html')

# 登錄
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

# 寫文章頁面
@login_required
def writing(request):
    return render(request,'writing.html')

# 发布文章
@login_required
def publish(request):
    if request.is_ajax():
        text=request.GET.get('data')
    is_success={'is_success':'success'}
    return JsonResponse(is_success)

# 推薦頁面
@login_required
def browsing(request):
    return render(request,'browsing.html')

# 相冊頁面
@login_required
def album(request):
    return render(request,'album.html')

# 設置頁面
def settings(request):
    return render(request,'settings.html')

# 注銷登陸
def logout_view(request):
    logout(request)
    return render_to_response('registration/login.html')

# 獲得用戶上傳的頭像照片，並進行裁剪
def upload_file(request,filename):
    if request.method =='POST':
        myFile=request.FILES.get(filename,None) # 获取用户上传圖片，若没有则为None
        if not myFile:
            return False
        # 將用戶上傳的圖片存到服務器
        pic_url=os.path.join(MEDIA_ROOT,request.user.username+'_por_pic.png')
        destination=open(pic_url,'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)

        #用戶圖片裁剪成正方形
        img=Image.open(pic_url)
        width=img.size[0]
        height=img.size[1]
        minsize=width if width<height else height
        region=(width/2-minsize/2,height/2-minsize/2,width/2+minsize/2,height/2+minsize/2)
        cut_img=img.crop(region)
        cut_img.save(os.path.join(MEDIA_ROOT,request.user.username+'_portrait.png'),'png')
        cut_url=os.path.join(MEDIA_URL,request.user.username+'_portrait.png')
        request.user.portrait_url=cut_url
        destination.close()
        return cut_url

# 用戶設置
def user_setting(request):
    if request.method=='POST':
        portrait = request.FILES.get('portrait')
        portrait_url='not_portrait'
        if portrait != None:
            portrait_url=upload_file(request,'portrait') # 獲得用戶頭像的url
        # 若portrait_url為空，説明設置失敗
        if not portrait_url:
            is_success={'is_success':'portrait_failure'}
            return JsonResponse(is_success)

        # 修改昵称
        is_nickname=False
        if request.POST.get('nickname')!=request.user.nickname and request.POST.get('title')!='':
            request.user.nickname=request.POST.get('nickname')
            is_nickname=True

        #修改个人简介
        is_title=False
        if request.POST.get('title') != request.user.title and request.POST.get('title')!='':
            request.user.title=request.POST.get('title')
            is_title=True

        # 判斷是否修改成功，成功則is_success賦值為success，若用戶沒有修改，則is_success賦值為not_change,返回給前端
        if is_nickname or is_title:
            request.user.save()
            is_success={'is_success':'success'}
        else:
            is_success={'is_success':'not_change'}

        if not portrait_url:
            result={
                'is_success':is_success['is_success'],
                'portrait_url':'not_change'
            }
            return JsonResponse(is_success)
        else:
            result={
                'is_success':is_success['is_success'],
                'portrait_url':portrait_url,
            }
            return JsonResponse(result)


