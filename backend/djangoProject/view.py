# -*- coding: utf-8 -*-
# Create your views here.
import datetime
import json
import os
import random
import time

import arrow
from django.contrib import auth
from django.core import serializers
from django.core.mail import send_mail
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse

from django.contrib.auth.models import User
from django.urls import path

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from datamodel import models
from datamodel.models import invationRecord, WhiteList, mypicture, mytask, segmentation, FallEvent, EmoEvent, \
    InteractionEvent, UnkownEvent, AttackEvent, Older, FaceLib, Volunteer, Stuff, Camera, MaskEvent
from djangoProject import settings

from django.views.decorators.http import require_http_methods




# _model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

admins = list(mypicture.objects.values("photo", "phone"))

print(admins)

known_face_encodings = []
admin_levels_names = []

# for admin in admins:
#     img = face_recognition.load_image_file('./media/' + admin['photo'])
#     item = {}
#     temp = WhiteList.objects.filter(phone_number=admin['phone']).values('name', 'level')[0]
#     item['name'] = temp['name']
#     item['level'] = temp['level']
#     admin_levels_names.append(item)
#     face_encoding = face_recognition.face_encodings(img)[0]
#     known_face_encodings.append(face_encoding)
#
# print('known face encode done')
# print(admin_levels_names)

#日期转码
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

#登陆
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def login(request):
    """登录"""
    result = True
    errorInfo = u''
    detail = {}
    data = request.data
    username = data.get('username')
    password = data.get('password')
    is_superuser = data.get('is_superuser')

    # 调用django进行用户认证
    # 验证成功 user返回<class 'django.contrib.auth.models.User'>
    # 验证失败 user返回None
    user = auth.authenticate(username=username, password=password)
    print("user", user)
    if user == None:
        result = False
        errorInfo = u'用户名或密码错误'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})

    if user.is_superuser == False and is_superuser == '1':
        result = False
        errorInfo = u'权限不足'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})
    # 用户名和密码验证成功
    # 获取用户的token 如果没有token ，表示时用户首次登录，则进行创建，并且返回token
    try:
        tokenObj = Token.objects.get(user_id=user.id)
    except Exception as e:
        # token 不存在 说明是首次登录
        tokenObj = Token.objects.create(user=user)
    # 获取token字符串
    token = tokenObj.key
    user.last_login = datetime.datetime.now()
    return Response({"result": result, "detail": {'token': token}, "errorInfo": errorInfo})

#获取所有用户信息
@api_view(['GET'])
def get_all_users(request):
    userList = User.objects.values("id", "username", "email", "is_superuser", "last_login", "first_name", "last_name")
    response_data = json.dumps(list(userList.values("id", "username", "email", "is_superuser", "last_login", "first_name", "last_name")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

#删除用户
@api_view(['POST'])
def user_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    User.objects.filter(id=id).delete()

    if(User.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def user_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if(User.objects.filter(id=id).update(username=username, email=email, first_name=first_name, last_name=last_name)):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

# def gen(d):
#     while True:
#         for frame in d.run2():
#             time.sleep(.001)
#             cv2.imwrite('./1.jpg', frame)
#             flag, buffer = cv2.imencode('.jpg', frame)
#             # if is_invade == True:
#             #     t = Invasion_Record_Saver(_date, _time, num)
#             #     t.start()
#             #     print('invade')
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')
#
# #处理过后视频推流
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# @authentication_classes(())
# def send_video(request):
#     d = Detector_RTMP(3, model=_model, known_face_encodings=known_face_encodings, admin_levels_names=admin_levels_names)
#     return StreamingHttpResponse(gen(d), content_type="multipart/x-mixed-replace; boundary=frame")
#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# @authentication_classes(())
# def start_detector(request):
#     print('start detector')
#     d = Detector(3, model=_model, known_face_encodings=known_face_encodings, admin_levels_names=admin_levels_names)
#     d.run2()
#     return HttpResponse('ok')
#
def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    camera = cv2.VideoCapture(file_name)
    if camera.isOpened():
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            flag, buffer = cv2.imencode('.jpg', frame)
            if not flag:
                continue
            # print('send video')
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')

#视频回放调取视频
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes(())
def get_video(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    time = time.split(':')
    filepath = date + '-' + time[0] + '-' + time[1] + '-' + time[2]
    filepath = './monitor/video/' + filepath + '.avi'
    return StreamingHttpResponse(file_iterator(filepath), content_type="multipart/x-mixed-replace; boundary=frame")


#人脸接受保存
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def upload_face(request):
    img = request.FILES.get('img')
    idcard = request.POST.get('idcard')
    #phone = '222'
    print(img)
    print(idcard)
    face_model = models.FaceLib(
        img=img,  # 拿到图片路径
        idcard=idcard # 拿到图片对应手机号
    )
    face_model.save()  # 保存图片
    print(face_model.img.name)
    return HttpResponse('media/' + face_model.img.name)

@api_view(['POST'])
#@permission_classes((AllowAny,))
def get_face(request):
    idcard = request.POST.get('idcard')
    #phone = '222'
    print(idcard)
    qset = FaceLib.objects.filter(idcard=idcard)
    print(qset.count())
    mypic = qset.first()
    return HttpResponse('media/' + mypic.img.name)

@api_view(['POST'])
#@permission_classes((AllowAny,))
def update_face(request):
    del_path = ''
    img = request.FILES.get('img')
    idcard = request.POST.get('idcard')
    #phone = '222'
    print(idcard)
    try:
        old = FaceLib.objects.filter(img=img).first()
        del_path = './media/' + old.img.name
        os.remove(del_path)
    except:
        print('delete failed')
    print(del_path)
    FaceLib.objects.filter(idcard=idcard).delete()
    face_model = models.FaceLib(
        img=img,  # 拿到图片路径
        idcard=idcard # 拿到图片对应手机号
    )
    face_model.save()  # 保存图片
    return HttpResponse('media/' + face_model.img.name)

@api_view(['POST'])
#获取某一天某段时间内的入侵记录
def get_specific_invation_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    invation_list1 = invationRecord.objects.filter(date__range=(date_choose, date_choose))
    invation_list = invation_list1.filter(time__range=(time_from,time_to)).values("date", "time", "level", "camera_id", 'area', 'invation_num')

    response_data =json.dumps(
        list(invation_list.values("date", "time", "level", "camera_id", 'area', 'invation_num')), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部入侵记录
def get_invation_records(request):

    recordList = invationRecord.objects.values("date", "time", "level", "camera_id",'area','invation_num')
    response_data = json.dumps(list(recordList.values("date", "time", "level", "camera_id",'area','invation_num')), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)


def isLeapYear(year):
    '''
    通过判断闰年，获取年份year的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(year, int), "请输入整数年，如 2018"

    if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum

@api_view(['GET'])
@permission_classes((AllowAny,))
#获取每天入侵数量
def get_num_records_day(request):
    start_year = 2021
    current_year = datetime.datetime.now().year
    mydict = {}
    for i in range(start_year, current_year+1):
        start_date = '%d-1-1' % i
        for j in range(0, isLeapYear(i)-300):
            date = arrow.get(start_date).shift(days=j).format("YYYY-MM-DD")
            day_choose = datetime.datetime.strptime(date,'%Y-%m-%d')
            invation_list = invationRecord.objects.filter(date=date)
            mydict[date] = invation_list.count()

    return JsonResponse({'dict':mydict})


@api_view(['POST'])
#获取一个月的入侵记录
#request: Year-month
#return [{'day1':count1},{'day2':count2},...]
#url:'api/invationrecord/getmonth'
def get_month_records(request):
    month_choose_str = request.POST.get('month')
    month_choose = datetime.datetime.strptime(month_choose_str,'%Y-%m')
    invation_m_list1 = invationRecord.objects.filter(date__year=month_choose.year)
    invation_m_list =invation_m_list1.filter(date__month=month_choose.month)
    invation_list=[]
    dict = {}
    for i in range(1,31):
        invation_d_list =invation_m_list.filter(date__day=i)
        if invation_d_list.count() !=0:
            # dict={i:invation_d_list.count()}
            dict[i] = invation_d_list.count()
            invation_list.append(dict)

    response_data =json.dumps(list(invation_list),cls=DateEncoder,indent= 4)
    return Response(dict)

#白名单
#增
@api_view(['POST'])
def whitelist_add(request):
    result = True
    detail = {}
    error_info=''

    name = request.POST.get('name')
    level = request.POST.get('level')
    phone_number = request.POST.get('phone_number')
    time_span_str = request.POST.get('time_span')
    time_str_list = time_span_str.split(',')
    time_start_str = time_str_list[0]
    time_end_str = time_str_list[1]

    whitelist = WhiteList.objects
    if whitelist.filter(name__exact=name).count()!=0:
        print('name')
        result = False
        error_info='名称重复'
    elif name =='' or level =='' or phone_number =='' or time_start_str =='' or time_end_str =='':
        print('empty')
        result =False
        error_info = '所填项不能为空'
    elif not phone_number.isdigit():
        print('phone')
        result = False
        error_info = '手机号码格式错误'
    else:
        print('sucsuc')
        time_start = datetime.datetime.strptime(time_start_str, '%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end_str, '%H:%M:%S')
        whitelist.create(name=name,level=level,phone_number=phone_number,time_start=time_start,time_end=time_end)


    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

@api_view(['POST'])
#获取某一天某段时间内的入侵记录
def get_specific_invation_time(request):
    date_choose_str= request.POST.get('date')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")

    invation_list1 = invationRecord.objects.filter(date__range=(date_choose, date_choose))
    invation_list = list(invation_list1.values("time"))
    print(invation_list)

    # response_data =json.dumps(
    #     list(invation_list.values("date", "time", "level", "camera_id", 'area', 'invation_num')), cls=DateEncoder)
    return Response(invation_list)

@api_view(['GET'])
#返回所有白名单信息
def whitelist_all(request):
    recordList = WhiteList.objects.values('name','level','phone_number','time_start','time_end')
    response_data = json.dumps(list(recordList.values('name','level','phone_number','time_start','time_end')),
                               cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

#白名单
#编辑
@api_view(['POST'])
def whitelist_edit(request):
    result = True
    detail = {}
    error_info=''

    name = request.POST.get('name')
    level = request.POST.get('level')
    phone_number = request.POST.get('phone_number')
    time_span_str = request.POST.get('time_span')
    time_str_list = time_span_str.split(',')
    time_start_str = time_str_list[0]
    time_end_str = time_str_list[1]

    whitelist = WhiteList.objects
    if name =='' or level =='' or phone_number =='' or time_start_str =='' or time_end_str =='':
        print('empty')
        result =False
        error_info = '所填项不能为空'
    else:
        print('sucsuc')
        time_start = datetime.datetime.strptime(time_start_str, '%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end_str, '%H:%M:%S')
        whitelist.filter(phone_number=phone_number).update(name=name,level=level,phone_number=phone_number,time_start=time_start,time_end=time_end)


    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#白名单
#删除
@api_view(['POST'])
def whitelist_delete(request):
    detail = {}
    error_info=''
    whitelist = WhiteList.objects
    phone_number = request.POST.get('phone_number')
    try:
        old = mypicture.objects.filter(phone=phone_number).first()
        del_path = './media/' + old.photo.name
        os.remove(del_path)
        old.delete()
    except:
        print('delete failed')
    if(whitelist.filter(phone_number=phone_number).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

@api_view(['POST'])
def get_user_by_username(request):
    username = request.POST.get('username')
    user_info = User.objects.filter(username=username)
    ret = []
    trans = {
        'username': '用户名', 'email': '邮箱', 'is_superuser': '是否为管理员', 'last_login': '最近一次登录', 'first_name': '名',
        'last_name': '姓', 'date_joined': '注册日期', 'auth_token': 'Token'
    }
    # print(list(user_info.values("username", "email", "is_superuser", "last_login", "first_name", "last_name", "date_joined", "auth_token")))
    for key, value in list(user_info.values("username", "email", "is_superuser", "last_login", "first_name", "last_name", "date_joined", "auth_token"))[0].items():
        if value == True:
            value = 'Ture'
        elif value == False:
            value = 'False'
        print('key ',trans[key], 'value ', value)
        ret.append({'key': trans[key], 'value': value})
    response_data = json.dumps(
        ret,
        cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def change_password(request):
    detail = {}
    error_info=''
    result = True
    username = request.POST.get('username')
    newpass = request.POST.get('password')
    user = User.objects.get(username=username)
    print('user ', user)
    if user == None:
        error_info = '用户不存在'
        result = False
    user.set_password(newpass)
    user.save()
    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#增加用户
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def user_reg(request):
    result = True
    detail = {}
    error_info = ''
    username = request.POST.get("username")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        # user.phone_number = phone_number
        ret = user.save()
        result = True
        print(ret)
    except:
        result = False
        error_info = '用户已存在'

    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

#增加用户
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def send_my_email(request):
    detail = {}
    error_info=''
    result = True
    code = request.POST.get('code')
    email = request.POST.get('email')
    title = "美团骑手offer"
    msg = "恭喜你成为美团骑手, 你的验证码是：" + code
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        email
    ]
    # 发送邮件
    try:
        send_mail(title, msg, email_from, reciever)
    except Exception as e:
        result = False
        error_info = '验证码发送失败'
        print(e)
    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

@api_view(['POST'])
def get_invasion_detail(request):
    date = request.POST.get("date")
    time = request.POST.get("time")
    time = time.split(':')
    datetime = date + '-' + time[0] + '-' + time[1] + '-' + time[2]
    dirname = './media/screen_shots/' + datetime
    print('dirname ', dirname)
    # dirname = './monitor/video/2021-07-27-10-23-08'
    file_num = sum([os.path.isfile(dirname + '/' + listx) for listx in os.listdir(dirname)])
    filename_list = []
    for i in range(0, file_num):
        filename_list.append('http://127.0.0.1:8000/media/screen_shots/' + datetime + '/' + str(i) + '.jpg')
    print(filename_list)
    return Response(filename_list)

@api_view(['POST'])
def add_segmentation(request):
    detail = {}
    error_info=''
    result = True
    top = request.POST.get("top")
    left = request.POST.get("left")
    width = request.POST.get("width")
    height = request.POST.get("height")
    try:
        segmentation.objects.create(top=top, left=left, width=width, height=height, level=1)
        print('添加成功')
    except Exception as e:
        print(e)
        result = False
        error_info = '添加失败'
        print('添加失败')
    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

@api_view(['POST'])
def task_add(request):
    detail = {}
    error_info=''
    result = True
    try:
        img = request.FILES.get('img')
        token = request.POST.get('token')
        #phone = '222'
        uid = Token.objects.filter(key=token).first().user_id
        print(uid)
        print(img)
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        task_model = models.mytask(
            date=date,
            time=time,
            status=0,
            uid=uid,  # 拿到图片对应用户id
            origin=img # 拿到图片
        )
        task_model.save()  # 保存图片
        print(task_model.origin.name)
        #启动处理线程
        #
        #此处调用线程
        #
    except:
        result = False
    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

@api_view(['GET'])
def task_get_all(request):
    taskList = mytask.objects.values('id','date','time','status')
    response_data = json.dumps(list(taskList.values('id','date','time','status')),
                               cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def task_download_processed(request):
    detail = {}
    error_info=''
    result = True
    id = request.POST.get('id')
    try:
        processed = mytask.objects.filter(id=id).first()
        print(processed.processed)
        detail['url'] = processed.processed.name
    except Exception as e:
        print(e)
        result = False
        error_info = '下载失败'
        detail['exception'] = repr(e)
    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

@api_view(['POST'])
def task_get_photos(request):
    detail = {}
    error_info=''
    result = True
    id = request.POST.get('id')
    try:
        task = mytask.objects.filter(id=id).first()
        urls = ['http://127.0.0.1:8000/media/' + task.processed.name, 'http://127.0.0.1:8000/media/' + task.origin.name]
        detail['urls'] = urls
    except Exception as e:
        print(e)
        result = False
        error_info = '查找失败'
        detail['exception'] = repr(e)
    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})



# 上报摔倒事件
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def record_fall(request):
    img = request.FILES.get('img')
    cid = request.POST.get('cid') # camera id
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    detail = request.POST.get('detail')

    result = 1
    fall_model = models.FallEvent(
        cid=cid,
        date=date,
        time=time,
        detail=detail,
        img=img
    )
    try:
        fall_model.save()
    except Exception as e:
        print(e)
        result = 0

    return JsonResponse({'result': result})

# 上报闯入事件
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def record_attack(request):
    img = request.FILES.get('img')
    cid = request.POST.get('cid') # camera id
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    detail = request.POST.get('detail')
    personType = request.POST.get('personType')
    area = request.POST.get('area')
    personId = request.POST.get('personId')

    result = 1
    attack_model = models.AttackEvent(
        cid=cid,
        date=date,
        time=time,
        detail=detail,
        img=img,
        personId=personId,
        personType=personType,
        area=area
    )
    try:
        attack_model.save()
    except Exception as e:
        print(e)
        result = 0

    return JsonResponse({'result': result})



# 上报陌生人事件
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def record_unkown(request):
    img = request.FILES.get('img')
    cid = request.POST.get('cid') # camera id
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    detail = request.POST.get('detail')
    num = request.POST.get('num')

    result = 1
    unkown_model = models.UnkownEvent(
        cid=cid,
        date=date,
        time=time,
        detail=detail,
        img=img,
        num=num
    )
    try:
        unkown_model.save()
    except Exception as e:
        print(e)
        result = 0

    return JsonResponse({'result': result})


# 上报情绪事件
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def record_emo(request):
    img = request.FILES.get('img')
    cid = request.POST.get('cid') # camera id
    oid = request.POST.get('oid')
    emo = request.POST.get('emo')
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    detail = request.POST.get('detail')

    result = 1
    emo_model = models.EmoEvent(
        oid=oid,
        cid=cid,
        date=date,
        time=time,
        detail=detail,
        emo=emo,
        img=img
    )
    try:
        emo_model.save()
    except Exception as e:
        print(e)
        result = 0

    return JsonResponse({'result': result})


# 上报交互事件
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def record_interaction(request):
    img = request.FILES.get('img')
    cid = request.POST.get('cid') # camera id
    oid = request.POST.get('oid')
    vid = request.POST.get('vid')
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    detail = request.POST.get('detail')

    result = 1
    interaction_model = models.InteractionEvent(
        oid=oid,
        vid=vid,
        cid=cid,
        date=date,
        time=time,
        detail=detail,
        img=img
    )
    try:
        interaction_model.save()
    except Exception as e:
        print(e)
        result = 0

    return JsonResponse({'result': result})



@api_view(['POST'])
#获取某一天某段时间内的摔倒记录
def get_specific_fall_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = FallEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部摔倒记录
def get_fall_records(request):

    recordList = FallEvent.objects.values("date", "time", "cid", "detail", "id")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "detail", "id")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_fall_detail(request):

    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = FallEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)


@api_view(['POST'])
#获取某一天某段时间内的情绪记录
def get_specific_emo_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = EmoEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail","oid","emo", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail","oid","emo", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部情绪记录
def get_emo_records(request):

    recordList = EmoEvent.objects.values("date", "time", "cid", "detail","oid","emo", "id")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "detail","oid","emo", "id")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_emo_detail(request):
    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = EmoEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)


@api_view(['POST'])
#获取某一天某段时间内的情绪记录
def get_specific_interaction_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = InteractionEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail","oid","vid", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail","oid","vid", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部情绪记录
def get_interaction_records(request):

    recordList = InteractionEvent.objects.values("date", "time", "cid", "detail","oid","vid", "id")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "detail","oid","vid", "id")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_interaction_detail(request):
    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = InteractionEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)


@api_view(['POST'])
#获取某一天某段时间内的摔倒记录
def get_specific_unkown_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = UnkownEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail","num", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail","num", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部陌生人记录
def get_unkown_records(request):

    recordList = UnkownEvent.objects.values("date", "time", "cid", "detail","num", "id")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "detail","num", "id")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_unkown_detail(request):
    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = UnkownEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)


@api_view(['POST'])
#获取某一天某段时间内的闯入记录
def get_specific_attack_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = AttackEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail","personId","personType","area", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail","personId","personType","area", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部闯入记录
def get_attack_records(request):

    recordList = AttackEvent.objects.values("date", "time", "cid", "detail","area","personId","personType","area", "id")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "detail","personId","personType","area", "id")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_attack_detail(request):
    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = AttackEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)



@api_view(['POST'])
#获取某一天某段时间内的口罩记录
def get_specific_mask_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    list1 = MaskEvent.objects.filter(date__range=(date_choose, date_choose))
    list_ = list1.filter(time__range=(time_from,time_to)).values("date", "time", "cid", "detail","personId","personType","area", "id")

    response_data =json.dumps(
        list(list_.values("date", "time", "cid", "detail","personId","personType","area", "id")), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部口罩记录
def get_mask_records(request):

    recordList = MaskEvent.objects.values("date", "time", "cid", "hasmask", "id", "detail")
    response_data = json.dumps(list(recordList.values("date", "time", "cid", "hasmask", "id", "detail")), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['POST'])
def get_mask_detail(request):
    id = request.POST.get('id')
    #phone = '222'
    print(id)
    qset = MaskEvent.objects.filter(id=id)
    print(qset.count())
    mypic = qset.first()
    filename_list = []
    filename_list.append('http://47.106.148.74:8080/media/' + mypic.img.name)
    return Response(filename_list)

#增加用户
@api_view(['POST'])
def o_reg(request):
    result = True
    detail = {}
    error_info = ''
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    r1name = request.POST.get("r1name")
    r1phone = request.POST.get("r1phone")
    r2name = request.POST.get("r2name")
    r2phone = request.POST.get("r2phone")
    health = request.POST.get("health")
    room = request.POST.get("room")
    try:
        older = models.Older(
            name = name,
            phone = phone,
            age = age,
            idcard = idcard,
            gender = gender,
            regdate = regdate,
            r1name = r1name,
            r1phone = r1phone,
            r2name = r2name,
            r2phone = r2phone,
            health = health,
            room = room
        )
        older.save()
        result = True
    except Exception as e:
        result = False
        print(e)
        error_info = '用户已存在'

    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

#删除用户
@api_view(['POST'])
def o_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    Older.objects.filter(id=id).delete()

    if(Older.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def o_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    r1name = request.POST.get("r1name")
    r1phone = request.POST.get("r1phone")
    r2name = request.POST.get("r2name")
    r2phone = request.POST.get("r2phone")
    health = request.POST.get("health")
    room = request.POST.get("room")

    if(Older.objects.filter(id=id).update(name = name,
                                         phone = phone,
                                         age = age,
                                         idcard = idcard,
                                         gender = gender,
                                         regdate = regdate,
                                         r1name = r1name,
                                         r1phone = r1phone,
                                         r2name = r2name,
                                         r2phone = r2phone,
                                         health = health,
                                         room = room)):
        print("success")
        result = True
    else:
        print('edit failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#获取所有用户信息
@api_view(['GET'])
def get_all_o(request):
    oList = Older.objects.values("id", "name", "phone", "age", "idcard", "regdate", "r1name", "r1phone", "r2name", "r2phone", "gender", "health", "room")
    response_data = json.dumps(list(oList.values("id", "name", "phone", "age", "idcard", "regdate", "r1name", "r1phone", "r2name", "r2phone", "gender", "health", "room")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

#增加用户
@api_view(['POST'])
def o_reg(request):
    result = True
    detail = {}
    error_info = ''
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    r1name = request.POST.get("r1name")
    r1phone = request.POST.get("r1phone")
    r2name = request.POST.get("r2name")
    r2phone = request.POST.get("r2phone")
    health = request.POST.get("health")
    room = request.POST.get("room")
    try:
        older = models.Older(
            name = name,
            phone = phone,
            age = age,
            idcard = idcard,
            gender = gender,
            regdate = regdate,
            r1name = r1name,
            r1phone = r1phone,
            r2name = r2name,
            r2phone = r2phone,
            health = health,
            room = room
        )
        older.save()
        result = True
    except Exception as e:
        result = False
        print(e)
        error_info = '用户已存在'

    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

#删除用户
@api_view(['POST'])
def o_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    Older.objects.filter(id=id).delete()

    if(Older.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def o_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    r1name = request.POST.get("r1name")
    r1phone = request.POST.get("r1phone")
    r2name = request.POST.get("r2name")
    r2phone = request.POST.get("r2phone")
    health = request.POST.get("health")
    room = request.POST.get("room")

    if(Older.objects.filter(id=id).update(name = name,
                                          phone = phone,
                                          age = age,
                                          idcard = idcard,
                                          gender = gender,
                                          regdate = regdate,
                                          r1name = r1name,
                                          r1phone = r1phone,
                                          r2name = r2name,
                                          r2phone = r2phone,
                                          health = health,
                                          room = room)):
        print("success")
        result = True
    else:
        print('edit failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#获取所有用户信息
@api_view(['GET'])
def get_all_o(request):
    oList = Older.objects.values("id", "name", "phone", "age", "idcard", "regdate", "r1name", "r1phone", "r2name", "r2phone", "gender", "health", "room")
    response_data = json.dumps(list(oList.values("id", "name", "phone", "age", "idcard", "regdate", "r1name", "r1phone", "r2name", "r2phone", "gender", "health", "room")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)


#增加用户
@api_view(['POST'])
def s_reg(request):
    result = True
    detail = {}
    error_info = ''
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    try:
        stuff = models.Stuff(
            name = name,
            phone = phone,
            age = age,
            idcard = idcard,
            gender = gender,
            regdate = regdate
        )
        stuff.save()
        result = True
    except Exception as e:
        result = False
        print(e)
        error_info = '用户已存在'

    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

#删除用户
@api_view(['POST'])
def s_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    Stuff.objects.filter(id=id).delete()

    if(Stuff.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def s_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")

    if(Stuff.objects.filter(id=id).update(name = name,
                                          phone = phone,
                                          age = age,
                                          idcard = idcard,
                                          gender = gender,
                                          regdate = regdate)):
        print("success")
        result = True
    else:
        print('edit failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#获取所有用户信息
@api_view(['GET'])
def get_all_s(request):
    sList = Stuff.objects.values("id", "name", "phone", "age", "idcard", "regdate", "gender")
    response_data = json.dumps(list(sList.values("id", "name", "phone", "age", "idcard", "regdate", "gender")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)


#增加用户
@api_view(['POST'])
def v_reg(request):
    result = True
    detail = {}
    error_info = ''
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")
    try:
        vonlunteer = models.Volunteer(
            name = name,
            phone = phone,
            age = age,
            idcard = idcard,
            gender = gender,
            regdate = regdate
        )
        vonlunteer.save()
        result = True
    except Exception as e:
        result = False
        print(e)
        error_info = '用户已存在'

    return JsonResponse({'result': result, 'detail': detail, 'errorInfo': error_info})

#删除用户
@api_view(['POST'])
def v_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    Volunteer.objects.filter(id=id).delete()

    if(Volunteer.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def v_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    age = request.POST.get("age")
    idcard = request.POST.get("idcard")
    gender = request.POST.get("gender")
    regdate = request.POST.get("regdate")

    if(Volunteer.objects.filter(id=id).update(name = name,
                                              phone = phone,
                                              age = age,
                                              idcard = idcard,
                                              gender = gender,
                                              regdate = regdate)):
        print("success")
        result = True
    else:
        print('edit failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#获取所有用户信息
@api_view(['GET'])
def get_all_v(request):
    vList = Volunteer.objects.values("id", "name", "phone", "age", "idcard", "regdate", "gender")
    response_data = json.dumps(list(vList.values("id", "name", "phone", "age", "idcard", "regdate", "gender")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)


#删除用户
@api_view(['POST'])
def camera_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    Camera.objects.filter(id=id).delete()

    if(Stuff.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def camera_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    cid = request.POST.get("cid")
    area = request.POST.get("area")
    state = request.POST.get("state")
    brand = request.POST.get("brand")

    if(Camera.objects.filter(id=id).update(cid = cid,
                                          area = area,
                                          state = state,
                                          brand = brand,)):
        print("success")
        result = True
    else:
        print('edit failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#获取所有用户信息
@api_view(['GET'])
def get_all_camera(request):
    sList = Camera.objects.values("id", "cid", "area", "state", "brand")
    response_data = json.dumps(list(sList.values("id", "cid", "area", "state", "brand")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)


@api_view(['POST'])
#获取人物信息
def get_person_type(request):
    personType = ''
    error_info=''
    idcard = request.POST.get("idcard")

    len1 = len(Older.objects.filter(idcard=idcard).get(idcard = idcard))
    len2 = len(Stuff.objects.filter(idcard=idcard).get(idcard = idcard))
    len3 = len(Volunteer.objects.filter(idcard=idcard).get(idcard = idcard))
    if(len1 != 0):
        print("Older Type")
        result = True
        personType = '老人'
    elif(len2 != 0):
        print("Stuff Type")
        result = True
        personType = '工作人员'
    elif(len3 != 0):
        print("Volunteer Type")
        result = True
        personType = '义工'
    else:
        result = False

    return JsonResponse({'result':result,'personType':personType,'errorInfo':error_info})