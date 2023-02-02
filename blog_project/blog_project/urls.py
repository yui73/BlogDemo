"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import url
from django.conf.urls.static import static
from blog.views import index_view
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    #从路由
    path('',include('blog.urls')),
    #后台管理路由
    path('admin/', admin.site.urls),
    #markdown插件
    path(r'mdeditor/',include('mdeditor.urls')),



    # url(r'^$',index_view,name='index_view'),
    # url(r'^', include('blog.urls')),
    # 关闭debug 需要重新设置静态路由
    # re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATICFILES_DIRS,}),
    # url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)