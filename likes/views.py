from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist	#引用不存在错误
from .models import LikeCount, LikeRecord  


def ErrorResponse(code, message):	#返回异常信息
    data = {}					
    data['status'] = 'ERROR'	#基本状态
    data['code'] = code		#标记
    data['message'] = message	
    return JsonResponse(data)

def SuccessResponse(liked_num):	#返回正常信息
    data = {}		#设置字典，单独分离，结构清晰
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user	#验证用户是否登录
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type') #元素类型
    object_id = int(request.GET.get('object_id')) #对象id

    try:	
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:	#捕捉错误
        return ErrorResponse(401, 'object not exist')	#对象不存在

    # 处理数据
    if request.GET.get('is_like') == 'true': #判断标记状态是否为点赞状态
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)#返回点赞对象和创建状态
        if created: 
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1	#保存数量+1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')	#402错误
    else:	#request.GET.get('is_like') == 'False'
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:	#如果数据有问题
                return ErrorResponse(404, 'data error')	#数据为0
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not liked')
