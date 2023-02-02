# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from blog.models import User
import re

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class RegForm(forms.Form):
    '''
    注册表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "以后不能修改咯~", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email","type":"email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    # url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),
                              # max_length=100, required=False)
    # PasswordInput 不会明文显示
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class CommentForm(forms.Form):
    '''
    评论表单
    '''
    # author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
    #                                                        "required": "required","size": "25", "tabindex": "1"}),
    #                           max_length=50,error_messages={"required":"username不能为空",})
    # email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
    #                                                        "required":"required","size":"25", "tabindex":"2"}),
    #                              max_length=50, error_messages={"required":"email不能为空",})
    # url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
    #                                                    "size":"25", "tabindex":"3"}),
    #                           max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "1"}),
                                                    error_messages={"required":"评论不能为空",})
    # article = forms.CharField(widget=forms.HiddenInput())

class UserForm(forms.Form):
    '''
    个人详情表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                               max_length=50,error_messages={"required": "Username不能为空",})
    # email 必有
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email","id":"email","type":"email","required": "required",
                                                           "size":"25", "tabindex":"2"}),max_length=50,error_messages={"required": "Email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "url","id":"url","type":"url","size":"25", "tabindex":"3"}),max_length=100)
    qq = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "QQ","tabindex":"4" }),max_length=20)
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
    #                            max_length=20,error_messages={"required": "password不能为空",})
    # avatar = forms.
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
    #                            max_length=20,error_messages={"required": "password不能为空",})

class ContactForm(forms.Form):
    '''
    联系我表单
    '''
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "怎么称呼你", "required": "required","tabindex": "1"}),
                          max_length=50,error_messages={"required": "Name不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "我会给这个邮箱回复哦~","id":"email","type":"email","required": "required",
                                                           "size":"25", "tabindex":"2"}),max_length=50,error_messages={"required": "Email不能为空",})
    # QQ可以没有
    # qq = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "QQ","tabindex":"4" }),max_length=20)
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "有什么问题都可以联系我","id":"message","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5","tabindex": "3"}),error_messages={"required":"Message不能为空",})