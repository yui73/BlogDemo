import markdown
# 登录 评论
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
# 密码加密
from django.contrib.auth.hashers import make_password
import json

from django.shortcuts import render
import logging
from django.conf import settings
from blog.models import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

import django.utils.timezone as timezone

# 目录美化
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# 导入表格model
from blog.forms import *

# 导入邮箱服务
from django.core import mail

# 导入缓存配置
from django.core.cache import cache, caches

logger = logging.getLogger('blog.views')

def global_setting(request):
    #取非空对象
    all_siteInfo = SiteInfo.objects.get(name__isnull=False)
    # 获取当前年份
    year = timezone.now().year
    # 数据截取的方法 QuerySet 惰性查询
    # all_siteInfo = SiteInfo.objects.all()[:1]
    if request.user.is_authenticated:
        print("已登录")
        # 获取用户信息-全局使用
    else:
        print("未登录")

    return {
        'siteInfo_list': all_siteInfo,
        'year':year,
    }

    #取settings的默认写死数据
    # return {
    #     # 'SITE_NAME': settings.SITE_NAME,
    #     # 'SITE_DESC':settings.SITE_DESC,
    #     # 'WELCOME_DESC':settings.WELCOME_DESC,
    # }

# Create your views here.
# def index(request):
#     all_article=Article.objects.all()
#     all_category=Category.objects.all()
#     all_tag=Tag.objects.all()
#     try:
#         # 一些方法
#         pass
#     except Exception as e:
#         # 有异常会进行捕获
#         logger.error(e)
#     return render(request,'index.html',{
#         'article_list':all_article,
#         'category_list':all_category,
#         'tag_list':all_tag
#     })

#-- 首页 --#
def index_view(request):
    try:
        # 一些方法-取前五数据放home
        all_article=Article.objects.all()[:5]
        index_info=PageManager.objects.get(pk=1)

    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    # 用locals()函数一起封装传递也可以
    return render(request, 'index.html',{
        'article_list':all_article,
        'index_info':index_info,
    })

#-- 归档页 --#
def archives_view(request):
    try:
        # 一些方法
        # 取年份
        # all_archives_year = Article.objects.distinct_year_list()
        all_article=Article.objects.all()
        archives_info=PageManager.objects.get(pk=2)
        archives_count = Article.objects.all().count()
        # article_list={}
        #
        # for year in all_archives_year:
        #     article_list['year','articles'] = [year,Article.objects.filter(date_publish__icontains=year)]
        #     print(article_list)
        # all_archives_date = Article.objects.distinct_date_list()
        # print(all_archives_date)
        # pass
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'archives.html',{
        # 'archive_year_list':all_archives_year,
        'article_list':all_article,
        'archives_info':archives_info,
        'archives_count':archives_count,
        # 'archive_date_list':all_archives_date,
    })

#-- 文章详情页 --#
def article_view(request):
    try:
        #一些方法-根据id查询文章
        id = request.GET.get('id',None)
        try:
            # 查询文章对象
            article = Article.objects.get(pk=id)
            # 上下篇获取不可从id排序，逻辑上应该按照date排序
            # 获取上一篇一篇
            article_front = Article.objects.filter(date_publish__lt=article.date_publish).order_by('date_publish').last()
            # 获取下一篇
            article_next = Article.objects.filter(date_publish__gt=article.date_publish).order_by('date_publish').first()
            # 对文章内容使用markdown插件渲染
            # article.content = markdown.markdown(article.content,extensions=[
            #     'markdown.extensions.extra',
            #     'markdown.extensions.codehilite',
            #     'markdown.extensions.toc',# 目录拓展
            # ])
            # 实例化一个markdown对象
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                # 'markdown.extensions.toc',# 目录拓展
                # 目录搜索链接美化
                TocExtension(slugify=slugify),
            ])
            # 在边栏生成目录
            article.content = md.convert(article.content)
            # article对象原本是没有toc这个属性的 通过md的toc动态添加
            article.toc = md.toc
            # print(article.content)
            # print(article.toc)
            # 返回文章信息
            # article_after_render = {'article':article,'article_front':article_front,'article_next':article_next,}
            # 查询文章对应的评论 PQ查询也可实现 但会增加读取数据库的资源
            comments = Comment.objects.filter(article=article).order_by('id')
            comment_list=[]
            comment_count = comments.count()
            comment_form = CommentForm()

            for comment in comments:
                # 取出头像
                user = User.objects.get(id=comment.user_id)
                avatar = user.avatar

                newcomment = comment
                newcomment.avatar=avatar

                for item in comment_list:
                    if not hasattr(item,'children_comment'):
                        setattr(item,'children_comment',[])
                    if comment.pid == item:
                        # item.children_comment.append(comment)
                        item.children_comment.append(newcomment)
                        break
                if comment.pid is None:
                    # comment_list.append(comment)
                    comment_list.append(newcomment)

            print(comment_list)
            # 返回评论数据
            # comment_after_render = {'comment':comment_list,'comment_count':comment_count,}
            # 渲染评论表格



            # for comment in comments:
            #     comment.avatar = User.objects.filter(username=comment.username).avatar
            #     print(comment.avatar)

        except Article.DoesNotExist:
            return render(request,'failure.html',{'reason':'没有找到对应文章'})
        pass
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request, 'article.html', {'article':article,'article_front':article_front,'article_next':article_next,'comment_list':comment_list,'comment_count':comment_count,'comment_form':comment_form, })

#-- 关于页 --#
def about_view(request):
    try:
        pass
        about = About.objects.get(author__isnull=False)
        about.self_desc = markdown.markdown(about.self_desc,extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        # 一些方法
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request, 'about.html',{
        'about':about,
    })

#-- 友情链接页 --#
def links_view(request):
    try:
        links_info=PageManager.objects.get(pk=3)
        links=Links.objects.all()

    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    # 用locals()函数一起封装传递也可以
    return render(request, 'links.html',{
        'links_info':links_info,
        'links':links,
    })

#-- 多标签页--#
def tags_view(request):
    try:
        # 一些方法
        all_tag = Tag.objects.all()
        pass
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'tags.html',{
        'all_tag':all_tag,
    })

#-- 单标签页 --#
def tag_view(request):
    try:
        # 一些方法-获取tag id
        id = request.GET.get('id',None)
        # 多对多关系
        tag = Tag.objects.get(id=id)
        all_article=Article.objects.filter(tag=tag)
        # all_article=Article.objects.filter(pk=1).fields()
        archives_count = all_article.count()
        print(all_article)
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'tag.html',{
        'all_article':all_article,
        'tag':tag,
        'archives_count':archives_count,
    })

#-- 联系页 --#
def contact_view(request):
    try:
        # 一些方法
        # 获取样式
        contact_info=PageManager.objects.get(pk=4)
        contact_form = ContactForm()
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'contact.html',{
        'contact_info':contact_info,
        'contact_form':contact_form,
    })

def contact_post(request):
    try:
        contact_form = ContactForm(request.POST)
        print("触发邮件处理")
        if contact_form.is_valid():
            # 现有数据拆分
            new_name = contact_form.cleaned_data['name']
            new_email = contact_form.cleaned_data['email']
            new_message = contact_form.cleaned_data['message']
            # 表单提交自动生成邮件并发送
            subject = new_name+" 给你的博客留言了！"
            message = "邮箱地址："+new_email+"\n"+new_message
            mail.send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['1507371282@qq.com',],
            )
        else:
            return render(request, 'failure.html', {'reason': contact_form.errors})
    except Exception as e:
        logger.error(e)
    # 删除缓存页面
    cache.clear()
    # cache.delete('contact_form')
    # 重新写跳转-success页面
    return redirect(request.POST.get('source_url'))
        # render(request,'success.html')


#-- 提交评论 --#
def comment_post(request):
    try:
        print("评论提交函数")
        # 文章id
        id = request.GET.get('id',None)
        # 父级评论id
        pid = request.POST.get('pid',None)
        comment_form = CommentForm(request.POST)
        user=request.user
        print(user.username)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=id,
                                             pid_id=pid,
                                             # 判断用户是否登录
                                             user=user,
                                             username=user.username,
                                             email=user.email,
                                             url=user.url,)
            comment.save()
            print("成功上传")
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


#-- 注销 --#
def do_logout(request):
    try:
        # Django自带logout方法 对session进行清除
        logout(request)
    except Exception as e:
        logger.error(e)
        # 有bug应该重定向到首页
    return redirect(request.META['HTTP_REFERER'])

#-- 注册 --#
def do_reg(request):
    try:
        if request.method == 'POST':
            print("触发注册提交表单后端处理")
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           # url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                # 将报错信息渲染到失败页
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', {'reg_form':reg_form,})

#-- 登录 --#
def do_login(request):
    try:
        # 如果是post请求
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                # Django 自己的验证方法 - 可以自定义重写
                user = authenticate(username=username, password=password)
                if user is not None:
                    # 使用默认的登录方法 - 可以自定义重写
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', {'login_form':login_form,})

#-- 个人中心 --#
def my_center(request):
    try:
        # 查询数据
        user_id=request.user.id
        user_obj = User.objects.get(id=user_id)
        print(user_obj)
        # if request.method == 'POST':
        #     user_form = UserForm(request.POST)
        #     if user_form.is_valid():
        #         # 现有数据拆分
        #         new_username = user_form.cleaned_data['username']
        #         new_url = user_form.cleaned_data['url']
        #         new_qq = user_form.cleaned_data['qq']
        #         User.objects.filter(id=user_id).update({'username':new_username,'url':new_url,'qq':new_qq})
        #         # update 方法 修改数据
        #         #
        #     else:
        #         return render(request, 'failure.html', {'reason': user_form.errors})
        # else:
        # 填充数据
        user_form = UserForm(initial={'email':user_obj.email,'url':user_obj.url,'qq':user_obj.qq,})

    except Exception as e:
        logger.error(e)
    return render(request,'mycenter.html',{'user_form':user_form,})

#-- 个人中心信息上传 --#
def my_center_post(request):
    try:
        # 查询数据
        user_id=request.user.id
        user_obj = User.objects.get(id=user_id)
        print(user_obj)
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # 现有数据拆分
            # new_username = user_form.cleaned_data['username']
            new_email = user_form.cleaned_data['email']
            new_url = user_form.cleaned_data['url']
            new_qq = user_form.cleaned_data['qq']
            print({'email':new_email,'url':new_url,'qq':new_qq})
            # ,url':new_url,'qq':new_qq}
            # if new_url == 'null':
            #     User.objects.filter(id=user_id).update( email=new_email,url=None,qq=new_qq)
            User.objects.filter(id=user_id).update(email=new_email,url=new_url,qq=new_qq)
        else:
            return render(request, 'failure.html', {'reason': user_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# def get_article_list(request):
#     try:
#         # 一些方法
#         pass
#     except Exception as e:
#         # 有异常会进行捕获
#         logger.error(e)
#     return render(request, {
#
#     })

def success_view(request):
    try:
        # 一些方法
        pass
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'success.html',)




def post_view(request):
    try:
        # 一些方法
        pass
    except Exception as e:
        # 有异常会进行捕获
        logger.error(e)
    return render(request,'post.html',)