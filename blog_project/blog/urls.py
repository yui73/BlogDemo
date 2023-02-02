from django.conf.urls import url
from django.urls import path
from blog.views import *

urlpatterns = [
    # 网站路由
    path('',index_view,name='index'),
    path('index/',index_view, name='index'),
    path('archives/',archives_view, name='archives'),
    path('about/',about_view,name='about'),
    path('post/',post_view,name='post'),
    path('links/',links_view,name='links'),
    path('contact/',contact_view,name='contact'),
    # path('failure/', ,name='failure'),
    #--文章详情路径正则--#
    path('article/',article_view,name='article'),
    path('tags/',tags_view,name='tags'),
    path('tag/',tag_view,name='tag'),
    # 登录/注册/注销
    path('login/',do_login,name='login'),
    path('reg/',do_reg,name='register'),
    path('logout/',do_logout,name='logout'),
    # 个人信息管理
    path('mycenter/',my_center,name='my_center'),
    # 个人信息管理提交
    path('mycenter/post/',my_center_post,name='my_center_post'),
    # 提交评论
    path('article/post/',comment_post,name="comment_post"),
    # 联系提交
    path('contact/post',contact_post,name="contact_post"),
    # 提交成功页面
    path('success/',success_view,name="success")
]
