from django.contrib import admin
from blog.models import *
# Register your models here.

# class ArticleAdmin(admin.ModelAdmin):
#     fields = ('title','desc','content',)


# 网站信息默认一个不允许新增/不允许删除
class SiteInfoAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     ('基本信息编辑',{'fields':['name','description','github_link']}),
    #     # ('Home',{'fields':['home_heading','home_subheading']}),
    #     # ('About',{'fields':['about_heading','about_subheading']}),
    #     # ('Post',{'fields':['post_heading','post_subheading']}),
    #     # ('Contact',{'fields':['contact_heading','contact_subheading']}),
    # )
    list_display = ['name','description','github_link','zhihu_link','weibo_link']

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class AboutAdmin(admin.ModelAdmin):
    list_display = ['author','intro','self_desc','heading','subheading']
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class PageManagerAdmin(admin.ModelAdmin):
    list_display = ['name','heading','subheading','banner_img']
    # 只读不可修改字段
    readonly_fields = ['name']
    # 初始化之后再启用方法
    # def has_add_permission(self, request):
    #     return False
    def has_delete_permission(self, request, obj=None):
        return False

class CommentAdmin(admin.ModelAdmin):
    list_display = ['username','article','content']

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)

# ArticleManager 无需注册
# admin.site.register(ArticleManager)

admin.site.register(Article)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Links)

#注册网站信息管理
admin.site.register(SiteInfo,SiteInfoAdmin)
# admin.site.register(SiteInfo)

# 注册页面管理
admin.site.register(PageManager,PageManagerAdmin)
admin.site.register(About,AboutAdmin)

#代理模型不知道要不要注册 但因为没表暂时不注册
# admin.site.register(AboutManager)

# admin 后台管理配置
admin.site.site_header = '博客后台管理系统'
admin.site.site_title = '博客后台管理系统'
admin.site.index_title = '博客后台管理系统'

