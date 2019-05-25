#引用
from django.contrib import admin
#引用同层目录的下models里的BlogType, Blog
from .models import BlogType, Blog

admin.site.site_title = 'MyDjango后台管理1'
admin.site.site_header = '文章管理'

#后台（通过类的方式实现继承）
#使用装饰器将BlogTypeAdmin和模型BlogType绑定注册到后台
@admin.register(BlogType)
#自定义BlogTypeAdmin，使其继承ModelAdmin
#ModelAdmin主要设置模型信息如何展现在后台系统中
class BlogTypeAdmin(admin.ModelAdmin):
	#设置admin后台数据的表头设置
	#id是哪儿出来的
	list_display = ('id','type_name')
	search_fields = ['id','type_name']
	list_filter = ['type_name'] 



#使用装饰器将BlogAdmin和模型Blog绑定注册到后台
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('id','title' , 'blog_type','author','get_read_num','created_time','last_updated_time')
	search_fields = ['id','title' , 'blog_type__type_name']
	list_filter = ['title' , 'blog_type__type_name']

