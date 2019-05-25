from django.contrib import admin
from .models import ReadNum, ReadDetail

#注册ReadNum类到admin的方法
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	#此处的content_object为实例类Blog
	list_display = ('read_num', 'content_object')

#注册ReadDetail类到admin的方法
@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	#此处的content_object为实例类Blog
	list_display = ('date','read_num', 'content_object')