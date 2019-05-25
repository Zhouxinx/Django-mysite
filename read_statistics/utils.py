import datetime #？
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum #自带总计？
from .models import ReadNum, ReadDetail #同层目录插入两个类

#方法
#获得阅读数
def read_statistics_once_read(request, obj):
	#获得类的对象赋给ct
	ct = ContentType.objects.get_for_model(obj)
	#把对象的组件值和模型值赋给key
	key = "%s_%s_read" % (ct.model , obj.pk)

	if not request.COOKIES.get(key):
		#总阅读数+1
		#get_or_create查找具有给定对象的便捷方法kwargs（如果您的模型具有所有字段的默认值，则可能为空），必要时创建一个
		readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk)
		readnum.read_num += 1
		readnum.save()

		#当天阅读数+1
		date = timezone.now().date()
		readDetail,created = ReadDetail.objects.get_or_create(content_type = ct , object_id = obj.pk, date = date)
		readDetail.read_num += 1
		readDetail.save()
	return key

def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	dates = []
	read_nums = []
	for i in range(7,0,-1):
		date = today - datetime.timedelta(days = i)
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type = content_type, date =date)
		result = read_details.aggregate(read_num_sum = Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)
	return dates,read_nums

def get_today_hot_data(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type = content_type, date = today).order_by('-read_num')
	#返回前7个数据
	return read_details[:7]

def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days = 1)
	read_details = ReadDetail.objects.filter(content_type = content_type, date = yesterday).order_by('-read_num')
	return read_details[:7]
