#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django表单定义
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱地址（可选）'
        })
    )
    
    first_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入姓名'
        })
    )
    
    last_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入姓氏'
        })
    )
    
    agree_terms = forms.BooleanField(
        required=True,
        label='我已阅读并同意用户协议和隐私政策',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名（3-20个字符）'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入密码（至少8个字符）'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '请再次输入密码'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已存在，请选择其他用户名")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被使用，请使用其他邮箱")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            try:
                UserProfile.objects.get_or_create(user=user)
            except Exception as e:
                print(f"创建用户资料时出错: {e}")
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """自定义登录表单"""
    remember_me = forms.BooleanField(
        required=False,
        label='记住我',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入用户名或邮箱',
            'autofocus': True
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入密码'
        })


class UserProfileForm(forms.ModelForm):
    """用户资料编辑表单"""
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'signature')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '简单介绍一下自己...'
            }),
            'signature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '个性签名'
            }),
        }


class UserEditForm(forms.ModelForm):
    """用户信息编辑表单"""
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '姓名'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '姓氏'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '邮箱地址（可选）'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['email'].initial = self.instance.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("该邮箱已被使用，请使用其他邮箱")
        return email