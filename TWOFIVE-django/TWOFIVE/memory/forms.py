# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
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
