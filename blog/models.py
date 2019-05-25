from django.db import models    #牢记数据库和文件的关系
from django.contrib.auth.models import User    #引用的用户模型
from django.contrib.contenttypes.fields import GenericRelation #反向泛型关系
from django.urls import reverse#重定向函数
from ckeditor_uploader.fields import RichTextUploadingField #富文本标签
from read_statistics.models import ReadNumExpandMethod, ReadDetail    #？？？待定

#模型定义了后台的字段，记住几个知识点：
#ORM框架
#创建了一个可在编程语言中使用的“虚拟对象数据库”
#定义的博客类型
#在META类来定义本类中在后台admin中中文显示的文字，来方便后台进行的开发
class BlogType(models.Model):
    #类型名称为字符串，最大字长为15
    type_name = models.CharField(max_length=15,verbose_name = '文章类型')
    #先要有实例，才能有初始化
    #self指的是实例BlogType本身
    #设置返回值
    #这样做的目的是为了别人在引用此外键的时候指向为type_name而不是别的字段
    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = '文章类型'
            
    

class Blog(models.Model, ReadNumExpandMethod):
    #如果没有primary_key=True为模型中的任何字段指定，Django将自动添加一个AutoField来保存主键
    #primary_key=True暗示null=False和 unique=True
    #unique=True该字段在整个表格中必须是唯一的，这在数据库级别和模型验证中强制执行
    #标题为字符串类型，最大长度为50
    title = models.CharField('标题',max_length=50)
    #引用外键
    #？？？博客类型是引用外键，关联删除
    #关于ForeignKey，on_delete=models.CASCADE，级联删除，Django模拟SQL约束ON DELETE CASCADE的行为，并删除包含ForeignKey的对象。
    #删除blog_type，同时也会把BlogType给删除掉了
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE,verbose_name = '文章类型')
    #文章内容是富文本标签
    content = RichTextUploadingField()  #文本内容，富文本标签

    #？？？作者引用外键，关联删除
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = '作者')
    #？？？阅读细节反向解析
    #反向泛型关系，每个Blog实例都有一个read_details属性，可以用来检索它们的关联ReadDetail
    #如果在Blog中定义了GenericRelation，删除了一个实例，在ReadDetail中所有的相关实例也会被删除
    read_details = GenericRelation(ReadDetail)
    #创建时间是为日期（DateTimeField）类型，auto_now_add=True自动添加时间，若为end_datetime = models.DateTimeField(null=True, blank=True)
    #则null=True表示该字段的数值可以为空，blank=True，设置在admin站点管理中添加数据的时候可允许空值
    #请注意，这与null=blank。null纯粹与数据库相关，而blank与验证相关。如果字段有blank=True，则表单验证将允许输入空值。如果字段有blank=False，则需要该字段。
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    #上次更新时间是为日期（DateTimeField）类型，auto_now_add=True自动添加时间
    last_updated_time = models.DateTimeField('最后更新时间',auto_now=True)
    #DateTimeField.auto_now每次保存对象时自动将字段设置为现在。对“最后修改”的时间戳有用。
    #DateTimeField.auto_now_add首次创建对象时自动将字段设置为现在
    #DateTimeField是日期和时间
    #DateFiel是日期
    #在auto_now和auto_now_add选项将始终使用的日期默认时区在创建或更新的时刻。    

    #得到url
    def get_url(self):
        #reverse（viewname，urlconf = None，args = None，kwargs = None，current_app = None）
        #viewname可以是URL模式名称或可调用视图对象
        #此url接受参数args、kwargs都可以
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})#反向解析blog_detail的url 

    #返回用户的email
    def get_email(self):
        return self.author.email

    #返回的字段是<Blog: str(self.title)>"
    #即是文章标题
    def __str__(self):
        return "<标题: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章'
        verbose_name_plural = '文章'




