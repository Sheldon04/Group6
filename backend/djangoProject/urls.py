"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from djangoProject import view, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/start', view.start_detector), #视频监控地址
    # path('api/video', view.send_video), #视频监控地址
    path('api/user/login', view.login), #登陆
    path('api/admin/getall', view.get_all_users), #获取所有用户信息
    path('api/admin/getuserbyname', view.get_user_by_username), #获取指定用户信息
    path('api/changepass', view.change_password), #修改密码
    path('api/adduser', view.user_reg), #用户增
    path('api/sendemail', view.send_my_email), #发送邮件
    path('api/admin/deluser', view.user_delete), #用户删
    path('api/admin/edituser', view.user_update), #用户改
    path('api/attacklistuser/all', view.get_invation_records), #所有入侵记录
    path('api/attacklistuser', view.get_specific_invation_records), #指定时间入侵记录
    path('api/attacklistuser/detail', view.get_invasion_detail),  # 获取入侵记录详情
    path('api/invationrecord/getmonth', view.get_month_records), #指定月份入侵记录
    path('api/invationrecord/chart1', view.get_num_records_day), #入侵统计图chart1接口
    path('api/invationrecord/getvideo', view.get_video), #视频回放
    path('api/attacklistuser/invasiontime', view.get_specific_invation_time), #制定日期入侵记录时间
    path('api/admin/whitelist/add', view.whitelist_add), #注册白名单
    path('api/admin/whitelist/all', view.whitelist_all), #获取白名单
    path('api/admin/whitelist/edit', view.whitelist_edit), #编辑白名单
    path('api/admin/whitelist/del', view.whitelist_delete), #删除白名单
    path('api/deblur/submit', view.task_add), #创建工单
    path('api/deblur/gettasks', view.task_get_all), #获取工单
    path('api/deblur/download', view.task_download_processed), #获取工单
    path('api/deblur/show', view.task_get_photos), #获取工单
    path('api/admin/segmentation', view.add_segmentation), #新增监控区域划分

    path('api/event/postfall', view.record_fall), #上报摔倒事件
    path('api/event/postemo', view.record_emo), #上报情绪事件
    path('api/event/postinteraction', view.record_interaction), #上报义工交互事件
    path('api/event/postunkown', view.record_unkown), #上报陌生人事件
    path('api/event/postattack', view.record_attack), #上报闯入事件

    path('api/event/fall/all', view.get_fall_records), #所有摔倒事件
    path('api/event/fall/detail', view.get_fall_detail), #摔倒事件
    path('api/event/fall', view.get_specific_fall_records), #指定摔倒事件
    path('api/event/emo/all', view.get_emo_records), #所有情绪事件
    path('api/event/emo/detail', view.get_emo_detail), #所有摔倒事件
    path('api/event/emo', view.get_specific_emo_records), #指定情绪事件
    path('api/event/interaction/all', view.get_interaction_records), #所有互动事件
    path('api/event/interaction/detail', view.get_interaction_detail), #所有互动事件
    path('api/event/interaction', view.get_specific_interaction_records), #指定互动事件
    path('api/event/unkown/all', view.get_unkown_records), #所有陌生人事件
    path('api/event/unkown/detail', view.get_unkown_detail), #陌生人事件
    path('api/event/unkown', view.get_specific_unkown_records), #指定陌生人事件
    path('api/event/attack/all', view.get_attack_records), #所有闯入事件
    path('api/event/attack/detail', view.get_attack_detail), #闯入事件
    path('api/event/attack', view.get_specific_attack_records), #指定闯入事件
    path('api/event/mask/all', view.get_mask_records), #所有口罩事件
    path('api/event/mask/detail', view.get_mask_detail), #口罩事件
    path('api/event/mask', view.get_specific_mask_records), #指定口罩事件


    path('api/admin/addo', view.o_reg), #增
    path('api/admin/delo', view.o_delete), #删
    path('api/admin/edito', view.o_update), #改
    path('api/admin/getallo', view.get_all_o), #获取所有用户信息
    # path('api/admin/getobyname', view.get_o_by_name), #获取指定用户信息

    path('api/admin/addv', view.v_reg), #增
    path('api/admin/delv', view.v_delete), #删
    path('api/admin/editv', view.v_update), #改
    path('api/admin/getallv', view.get_all_v), #获取所有用户信息

    path('api/admin/adds', view.s_reg), #增
    path('api/admin/dels', view.s_delete), #删
    path('api/admin/edits', view.s_update), #改
    path('api/admin/getalls', view.get_all_s), #获取所有用户信息

    path('api/admin/uploadface', view.upload_face), #上传人脸照片
    path('api/admin/getface', view.get_face), #获取人脸照片
    path('api/admin/updateface', view.update_face), #更新人脸照片

    path('api/admin/delcamera', view.camera_delete), #删
    path('api/admin/editcamera', view.camera_update), #改
    path('api/admin/getallcamera', view.get_all_camera), #获取所有用户信息

    path('api/admin/getpersontype', view.get_person_type), #获取所有用户信息

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
