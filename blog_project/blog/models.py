# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField


# Create your models here.
# 用户模型 继承AbstractUser类，django自带
# 扩展方式可以使用关联
class User(AbstractUser):
    # 图片类型字段
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


# 标签设计
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    # 备注方便在admin中管理
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    # unicode方法，返回自身属性，admin后台使用，默认字符串类型的，非字符串类型需要包一个str进行类型更改
    # unicode 方法有bug使用str方法代替
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    # unicode方法，返回自身属性，admin后台使用，默认字符串类型的，非字符串类型需要包一个str进行类型更改
    def __str__(self):
        return self.name


# 自定义一个文章Model的管理器 - 日期
# 1 新加一个数据处理的方法
# 2 改变原有的queryset - 未使用
class ArticleManager(models.Manager):
    # 获取年份
    def distinct_year_list(self):
        # 保存结果-初始化空
        distinct_year_list = []
        # 取数据
        date_list = self.values('date_publish')
        for date in date_list:
            # 数据格式按需求标准化
            # date = date['date_publish'].strftime('%Y/%m文章存档')
            year = date['date_publish'].strftime('%Y')
            # 判断日期不在列表里就加入
            if year not in distinct_year_list:
                distinct_year_list.append(year)
        return distinct_year_list

    # 获取具体无年分日期
    # def distinct_date_list(self):
    #     distinct_date_list = []
    #     date_list = self.values('data_publish')
    #     for date in date_list:
    #         dateDetail = date['data_publish'].strftime('%m/%d')
    #         if dateDetail not in distinct_date_list:
    #             distinct_date_list.append(dateDetail)
    #     return distinct_date_list


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    # content = models.TextField(verbose_name='文章内容')
    content = MDTextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    # 关联管理器
    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish'] #按照文章发布日期排序

    def __str__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    #--- 用于实现匿名评论-被阉割了 ---#
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    #---------------------#
    # 与用户表关联 ----实名评论 #
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.DO_NOTHING)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.content)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='头像')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# 网站基本信息-雏形-标题定制-解耦（不会
class SiteInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='网站名称')
    description = models.CharField(max_length=50, blank=True, null=True, verbose_name='网站描述')
    github_link = models.URLField(blank=True, null=True, verbose_name='Github链接')
    zhihu_link = models.URLField(blank=True, null=True, verbose_name='知乎链接')
    weibo_link = models.URLField(blank=True, null=True, verbose_name='微博链接')

    # # 个性化定制信息-首页
    # home_heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='首页-大标题')
    # home_subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='首页-副标题')
    # # 个性化定制信息-关于
    # about_heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='关于页-大标题')
    # about_subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='关于页-副标题')
    # # 个性化定制信息-发布
    # post_heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='发布页-大标题')
    # post_subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='发布页-副标题')
    # # 个性化定制信息-联系
    # contact_heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系页-大标题')
    # contact_subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系页-副标题')

    class Meta:
        verbose_name = '网站基本信息管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '网站基本信息管理'

# 各种网页解耦-代理模型不可行-尝试多表继承-代码重构
class PageManager(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='页面名称')
    heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='大标题')
    subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='副标题')
    banner_img=models.ImageField(upload_to='banner/%Y/%m', default='banner/default.png', max_length=200, blank=True,
                                 null=True, verbose_name='页面头图')
    class Meta:
        verbose_name = '页面管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# AboutManager-PageManager
class About(models.Model):
    author = models.CharField(max_length=50, verbose_name='名字')
    intro = models.CharField(max_length=100, blank=True, null=True, verbose_name='格言')
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='头像')
    self_desc = MDTextField(verbose_name='自我介绍')
    heading = models.CharField(max_length=100, blank=True, null=True, verbose_name='大标题')
    subheading = models.CharField(max_length=100, blank=True, null=True, verbose_name='副标题')
    banner_img=models.ImageField(upload_to='banner/%Y/%m', default='banner/default.png', max_length=200, blank=True,
                                 null=True, verbose_name='页面头图')

    class Meta:
        verbose_name = 'about页面管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'about页面管理'