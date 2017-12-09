# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *
from django import forms

from django.contrib.auth.forms import UsernameField


class RegisterForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'InputPassword2', 'placeholder': "请输入您的密码"}))
    password2=forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'InputPasswordRepeat', 'placeholder': "请再次输入您的密码"}))
    class Meta(UserCreationForm.Meta):
        model=User
        fields = ('username','email','nickname')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','id':'InputUserName2','placeholder':"请输入您的用户名"}),
            'email':forms.TextInput(attrs={'class':'form-control','id':'InputEmail1','placeholder':"请输入您的邮箱"}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','id':'InputPassword2','placeholder':"请输入您的密码"}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','id':'InputPasswordRepeat','placeholder':"请再次输入您的密码"}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'id': 'InputUserName1',
            'placeholder': '请输入您的用户名',
             'name': 'login_username'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'InputPassword1',
            'placeholder':'请输入您的密码',
            'name':'login_password'}
    ))

class CommentForm(forms.Form):

    name = forms.CharField(label='称呼', max_length=16, error_messages={
            'required': '请填写您的称呼',
            'max_length': '称呼太长咯'
    })

    content = forms.CharField(label='评论内容', error_messages={
            'required': '请填写您的评论内容！',
            'max_length': '评论内容太长咯'
    })

# class ArticleForm(forms.Form):
#     title=forms.CharField(
#          label='标题', max_length=244,error_messages={
#             'required': '请填写标题',
#             'max_length': '标题太长咯'
#     })
#     content=forms.CharField(
#         widget=forms.Textarea
#     )
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','content')