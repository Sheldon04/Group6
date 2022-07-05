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
    path('api/start', view.start_detector), #视频监控地址
    path('api/video', view.send_video), #视频监控地址
    path('api/user/login', view.login), #登陆
    path('api/admin/getall', view.get_all_users), #获取所有用户信息
    path('api/admin/getuserbyname', view.get_user_by_username), #获取指定用户信息
    path('api/changepass', view.change_password), #修改密码
    path('api/adduser', view.user_reg), #用户增
    path('api/sendemail', view.send_my_email), #发送邮件
    path('api/admin/deluser', view.user_delete), #用户删
    path('api/admin/edituser', view.user_update), #用户改
    path('api/admin/uploadface', view.upload_face), #上传人脸照片
    path('api/admin/getface', view.get_face), #获取人脸照片
    path('api/admin/updateface', view.update_face), #更新人脸照片
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
