# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect,render_to_response
from .forms import *
from django.contrib.auth import  authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
import json
from PIL import Image,ImageFile
from TWOFIVE.settings import MEDIA_ROOT,MEDIA_URL
ImageFile.LOAD_TRUNCATED_IMAGES = True

from .models import *
from django.views.generic import ListView
import markdown2 #这里需要install markdown2 package

# Create your views here.

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
    if request.is_ajax():
        text=request.GET.get('data')
    is_success={'is_success':'success'}
    return JsonResponse(is_success)

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
        pic_url=os.path.join(MEDIA_ROOT,request.user.username+'_por_pic.png')
        destination=open(pic_url,'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
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


def user_setting(request):
    if request.method=='POST':
        portrait = request.FILES.get('portrait')
        portrait_url='not_portrait'
        if portrait != None:
            portrait_url=upload_file(request,'portrait')
            request.user.portrait_url=portrait_url
            request.user.save()
        if not portrait_url:
            is_success={'is_success':'portrait_failure'}
            return JsonResponse(is_success)
        # 修改昵称
        is_nickname=False
        if request.POST.get('title')!='':
            request.user.nickname=request.POST.get('nickname')
            is_nickname=True

        #修改个人简介
        is_title=False
        if request.POST.get('title')!='':
            request.user.title=request.POST.get('title')
            is_title=True

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
                'is_success':'success',
                'portrait_url':portrait_url,
            }
            return JsonResponse(result)





def get_articles(request):
    myArticles = Article.objects.all().order_by('-pub_date')
    return render_to_response('homepage.html',{'myArticles':myArticles})

#
# def get_details(request,blog_id):
#     try:
#         article = Article.objects.get(id=blog_id)
#     except Article.DoesNotExist:
#         raise Http404
#     if request.method == 'GET':
#         form = CommentForm()
#     else:
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             cleaned_data['article'] = article
#             Comment.objects.create(**cleaned_data)
#     ctx = {
#         'article':article,
#         'comments':article.comment_set.all().order_by('-created'),
#         'form':form
#     }
#    return render(request,'article-details.html',ctx)



# def addArticle(request):
#     if request.method == 'POST':
#         article_form = ArticleForm(request.POST)
#     if article_form.is_valid():
#         cd = article_form.cleaned_data
#         article=Article()
#         article.title=cd['title']
#         article.content=cd['content']
#         article.save()
#         return HttpResponseRedirect('/memory/homepage')
#
#     else:
#         article_form = ArticleForm()
#         return render_to_response('writing.html', {'form': article_form})
def addArticle(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
    if article_form.is_valid():
        title=article_form.cleaned_data['title']
        content = article_form.cleaned_data['content']
        author=request.user
        Article.objects.create(title=title, author=author, content=content)
        #article_form.save()
        return redirect('/memory/homepage')

    else:
        article_form = ArticleForm()
        return render(request, 'writing.html', {'article_form': article_form})


class HomeView(ListView):
    template_name ="homepage.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.content = markdown2.markdown(article.content, )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Mood.objects.all().order_by('color')
        return super(HomeView, self).get_context_data(**kwargs)
