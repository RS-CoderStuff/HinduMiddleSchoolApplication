from django.conf.urls import include, url
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.authtoken import views
from apiapp import views as api_views



urlpatterns = [

    url(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

    url(r'^api-token-auth/', views.obtain_auth_token),
    ################
    url('LoginView', api_views.LoginView.as_view(), name="LoginView"),
    url('Singup', api_views.Singup.as_view(), name="Singup"),
    url('PasswordChangeView', api_views.PasswordChangeView.as_view(), name="PasswordChangeView"),
    url('PasswordResetView', api_views.PasswordResetView.as_view(), name="PasswordResetView"),
    url('User_Serializers_list', api_views.User_Serializers_list.as_view(), name="User_Serializers_list"),
    url('User_Device_list', api_views.User_Device_list.as_view(), name="User_Device_list"),
    url('Main_Course_Category_Singal_list/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Main_Course_Category_Singal_list.as_view(), name="Main_Course_Category_Singal_list"),
    url('Main_Course_Category_list', api_views.Main_Course_Category_list.as_view(), name="Main_Course_Category_list"),
    url('Super_Course_Category_Serializers_list/(?P<main_course_category_id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Super_Course_Category_Serializers_list.as_view(), name="Super_Course_Category_Serializers_list"),
    url('Sub_Course_Category_Serializers_list/(?P<super_course_category_id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Sub_Course_Category_Serializers_list.as_view(), name="Sub_Course_Category_Serializers_list"),
    url('Course_Content_Serializers_list/(?P<sub_course_category_id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Course_Content_Serializers_list.as_view(), name="Course_Content_Serializers_list"),
    url('Course_Content_Serializers_Private/', api_views.Course_Content_Serializers_Private.as_view(), name="Course_Content_Serializers_Private"),
    url('Course_Content_Serializers_Single/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Course_Content_Serializers_Single.as_view(), name="Course_Content_Serializers_Single"),
    url('Course_Content_Serializers_Save/', api_views.Course_Content_Serializers_Save.as_view(), name="Course_Content_Serializers_Save"),
    ######################


    # admin panel api link here
    url('User_list', api_views.User_list.as_view(), name="User_list"),
    url('Guest_list', api_views.Guest_list.as_view(), name="Guest_list"),
    url('Teacher_list', api_views.Teacher_list.as_view(), name="Teacher_list"),
    url('Student_list', api_views.Student_list.as_view(), name="Student_list"),
    url('Paid_list', api_views.Paid_User_list.as_view(), name="Paid_list"),
    url('User_Edit_Api', api_views.User_Edit_Api.as_view(), name="User_Edit_Api"),
    url('Update_user_list/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Single_User_list.as_view(), name="Update_user_list"),
    url('111',api_views.version111.as_view(), name='111'),


    url('Plan_Serializers_list', api_views.Plan_Serializers_list.as_view(), name="Plan_Serializers_list"),
    url('Plan_Serializers_User', api_views.Plan_Serializers_User.as_view(), name="Plan_Serializers_User"),
    url('Batch_Serializers_list', api_views.Batch_Serializers_list.as_view(), name="Batch_Serializers_list"),
    url('Uplode_noti/', api_views.Uplode_Noti.as_view(), name="Uplode_noti"),
    url('Notification_Serializers_list', api_views.Notification_Serializers_list.as_view(), name="Notification_Serializers_list"),
    url('Student_Notification_list', api_views.Student_Notification_Serializers_list.as_view(), name="Student_Notification_list"),
    url('Student_single/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Student_single.as_view(), name="Student_single"),
    url('Live_Serializers_list', api_views.Live_Notification_Serializers_list.as_view(), name="Live_Serializers_list"),
    url('Live_single/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Live_single.as_view(), name="Live_single"),
    url('Notification_Serializers_single/(?P<id>[0-9A-Za-z_\-!@#$%^&*()]+)', api_views.Notification_Serializers_single.as_view(), name="Notification_Serializers_single"),

]
