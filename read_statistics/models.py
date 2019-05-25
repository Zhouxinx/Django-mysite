from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType #ContentType表示和存储有关项目中安装的模型的信息的实例， 以及安装ContentType新模型时自动创建的新实例
from django.utils import timezone #时区转换

#阅读数类
#这里的models.Model为类Blog
class ReadNum(models.Model):
    #阅读数整数，默认为0
    read_num = models.IntegerField(default=0,verbose_name = '阅读数')
    #内容类型为外键，引用外键为ContentType，级联删除
    #这里使用的content_type代替了实际的model（如Post，Picture）
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #传入对象的id
    #object_id则代表了实际model中的一个实例的主键
    #object_id必须是一个正整数
    object_id = models.PositiveIntegerField()
    #传入实例化的对象，其包含了两个属性content_type和object_id
    #ContentType提供了一种GenericForeignKey的类型，通过这种类型可以实现对其余所有model的外键关系
    #content_type和object_id的字段命名都是作为字符串参数传进content_object的
    #content_object指的是类的一个实例，而content_type指的是类，object_id则为实际类的实例中的一个主键
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读次数'
        verbose_name_plural = '阅读次数'

class ReadNumExpandMethod():
    #阅读次数的扩展方法
      def get_read_num(self):
        #查询try语句中的字段是否有错误，如果无误，则跳过except继续执行，返回readnum.read_num，否则在except里查找对应的错误exceptions.ObjectDoesNotExist，如果为此异常，则返回0值
        try:
            #get_for_model（model，for_concrete_model = True），获取模型类或模型的实例
            #self指的是 类实例对象本身 (注意：不是类本身)
            #self.pk值赋予类的实例中的一个主键值
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type = ct, object_id = self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
#这里的models.Model为类Blog
class ReadDetail(models.Model):
    #date = models.DateTimeField(auto_now_add=True)
    date = models.DateField('日期',default=timezone.now)
    #阅读数为整形
    read_num = models.IntegerField('阅读数',default=0)
    #ContentType三剑客
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读明细'
        verbose_name_plural = '阅读明细'