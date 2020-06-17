"""ieltsclasses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.urls import path
from django.conf.urls import url, include
from ieltsapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from ieltsapp.forms import EmailValidationOnForgotPassword, SetPasswordForm
from ieltsclasses.settings import DEBUG
from django.views.static import serve


urlpatterns = [

    url(r'^country-autocomplete/$', views.CountryAutocomplete.as_view(), name='country-autocomplete', ),
    url(r'^Course_Content_Autocomplete/$', views.Course_Content_Autocomplete.as_view(), name='Course_Content_Autocomplete', ),
    url(r'^Multi_User_Autocomplete/', views.Multi_User_Autocomplete.as_view(), name='Multi_User_Autocomplete', ),
    url(r'^Sub_course_category_Autocomplete/', views.Sub_course_category_Autocomplete.as_view(), name='Sub_course_category_Autocomplete', ),


    url('admin/', admin.site.urls),
    url('ckeditor', include('ckeditor_uploader.urls')),
    url('api/(?P<version>(v4|v5))/', include('apiapp.urls')),
    url('rest-auth/', include('rest_auth.urls')),

    url(r'^aaa', views.aaa, name='aaa'),
    url(r'^$', views.index, name='index'),
    url(r'^blogs', views.blog, name='blogs'),
    url(r'^blog/(?P<slug>[-\w\d]+)', views.blog_details, name='blog_details'),

    url(r'^payment-successful', views.payment_successful, name='payment_successful'),
    url(r'^cancel-payment', views.cancel_payment, name='cancel_payment'),
    url(r'^student-login', views.student_login, name='student_login'),
    url(r'^student-signup', views.Student_Sign_Up.as_view(), name='student_signup'),
    url(r'^buy-course/(?P<pk>\d+)', views.buy_course, name='buy_course'),
    url(r'^paymentstatus/(?P<pair>[0-9A-Za-z_\-]+)',views.paymentstatus),
    # url(r'^tec-courses', views.tec_courses, name='tec_courses'),
    url(r'^load_sub_course_category_front', views.load_sub_course_category_front, name='load_sub_course_category_front'),


    # url(r'^tec-pdf', views.tec_pdf, name='tec_pdf'),
    # url(r'^crash-courses', views.crash_courses, name='crash_courses'),
    # url(r'^course-details/(?P<pk>\d+)/(?P<sub_id>\d+)', views.course_details, name='course_details'),

    url(r'^sign-in', views.sign_in, name='sign_in'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^sign-up', views.Sign_Up.as_view(), name='sign_up'),
    url(r'^Contact_us_save', views.Contact_us_save.as_view(), name='Contact_us_save'),
    url(r'^logout', auth_views.LogoutView, {'next_page': '/'}, name='logout'),


    #######################################
   url(r'^change-password', views.change_password, name='change_password'),
   url(r'^password_reset/$', auth_views.PasswordChangeView.as_view(),{'template_name': 'forget-password.html','html_email_template_name': 'email-template/forget-password.html','password_reset_form': EmailValidationOnForgotPassword}, name='password_reset'),
   url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
   url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(), {'template_name': 'password_reset_confirm.html','set_password_form':SetPasswordForm}, name='password_reset_confirm'),
   url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), {'template_name': 'password-reset-complete.html'}, name='password_reset_complete'),


    # url(r'^enroll-now', views.enroll_now, name='enroll_now'),
   # front URLs end

    url(r'^verify-email', views.verify_email, name='verify_email'),
    url(r'^invalid', views.invalid, name='invalid'),

    # admin URLs start
    url(r'^dashboard', views.Dashboard.as_view(), name='dashboard'),

    # users
    url(r'^profile', views.profile, name='profile'),
    url(r'^users', views.List_All_User.as_view(), name='users'),
    url(r'^delete_user/(?P<pk>\d+)', views.Delete_User.as_view(), name='delete_user'),


    url(r'^view-awards', views.view_awards, name='view-awards'),
    url(r'^all-awards', views.all_awards, name='all-awards'),
    url(r'^multi-user-edit', views.multi_user_edit, name='multi-user-edit'),
    url(r'^paid-users', views.List_Paid_User.as_view(), name='paid_users'),
    url(r'^edit-user/(?P<pk>\d+)', views.User_Edit.as_view(), name='user_edit'),
    url(r'^students', views.List_Students_User.as_view(), name='students'),
    url(r'^guest', views.List_Guest_User.as_view(), name='guest'),
    url(r'^teachers', views.List_Teacher_User.as_view(), name='teachers'),

    url(r'^contact-list', views.List_All_Contact.as_view(), name='contact_list'),
    url(r'^delete_contact/(?P<pk>\d+)', views.Delete_Contact.as_view(), name='delete_contact'),



    # batches
    url(r'^add-batch', views.Add_Batch.as_view(), name='add_batch'),
    url(r'^view-batches', views.List_Batch.as_view(), name='view_batches'),
    url(r'^edit-batch/(?P<pk>\d+)', views.Edit_Batch.as_view(), name='edit_batch'), # batches
    url(r'^delete_batch/(?P<pk>\d+)', views.Delete_Batch.as_view(), name='delete_batch'), # batches

    # Main_Course_Category
    url(r'^add-course-category', views.Add_Main_Course_Category.as_view(), name='add_course_category'),
    url(r'^edit-course-category/(?P<pk>\d+)', views.Edit_Main_Course_Category.as_view(), name='edit_course_category'),
    url(r'^course-category-list', views.List_Main_Course_Category.as_view(), name='list_course_category'),
    url(r'^delete_course_category/(?P<pk>\d+)', views.Delete_Main_Course_Category.as_view(),name='delete_course_category'),

    # Super_Course_Category
    url(r'^course-super-category-add', views.Add_Super_Course_Category.as_view(), name='add_course_super_category'),
    url(r'^course-super-category-list', views.List_Super_Course_Category.as_view(), name='course_super_category_list'),
    url(r'^delete_super_course_category/(?P<pk>\d+)', views.Delete_Super_Course_Category.as_view(),name='delete_super_course_category'),
    url(r'^edit-super-category/(?P<pk>\d+)', views.Edit_Super_Course_Category.as_view(), name='edit_course_super_category'),

    # Sub_Course_Category
    url(r'^course-sub-category-add', views.Add_Sub_Course_Category.as_view(), name='add_course_sub_category'),
    url(r'^course-sub-category-list', views.List_Sub_Course_Category.as_view(), name='course_sub_category_list'),
    url(r'^delete_sub_course_category/(?P<pk>\d+)', views.Delete_Sub_Course_Category.as_view(), name='delete_sub_course_category'),
    url(r'^edit-sub-category/(?P<pk>\d+)', views.Edit_Sub_Course_Category.as_view(), name='edit_course_sub_category'),


    ##########################
    url('load_main_course_category/', views.load_main_course_category, name='load_main_course_category'),  # <-- this one here
    url('load_sub_course_category/', views.load_sub_course_category, name='load_sub_course_category'),  # <-- this one here

    url(r'^add-course', views.Add_Course.as_view(), name='add_course'),
    url(r'^course-list', views.List_Course.as_view(), name='course_list'),
    url(r'^edit-course/(?P<pk>\d+)', views.Edit_Course.as_view(), name='edit_course'),
    url(r'^delete_course/(?P<pk>\d+)', views.Delete_Course.as_view(), name='delete_course'),

    url(r'^course-content-list', views.List_Course_Content.as_view(), name='course_content_list'),
    url(r'^addcourse-content', views.Add_Course_Content.as_view(), name='add_course_content'),
    url(r'^editcourse-content/(?P<pk>\d+)', views.Edit_Course_Content.as_view(), name='edit_course_content'),
    url(r'^deletecourse-content/(?P<pk>\d+)', views.Delete_Course_Content.as_view(), name='deletecourse_content'),



    url(r'^course-fee-list', views.fee_list, name='fee_list'), # courses

    # Blog_Category
    url(r'^add-blog-category', views.Add_Blog_Category.as_view(), name='add_blog_category'),
    url(r'^edit-blog-category/(?P<pk>\d+)', views.Edit_Blog_Category.as_view(),name='edit_blog_category'),
    url(r'^blog-category-list', views.List_Blog_Category.as_view(), name='list_blog_category'),
    url(r'^delete_blog_category/(?P<pk>\d+)', views.Delete_Blog_Category.as_view(), name='delete_blog_category'),

    # Blog
    url(r'^blog-list', views.List_Blog.as_view(), name='blog_list'),
    url(r'^add-blog', views.Add_Blog.as_view(), name='add_blog'),
    url(r'^edit-blog/(?P<pk>\d+)', views.Edit_Blog.as_view(), name='edit_blog'),
    url(r'^delete-blog/(?P<pk>\d+)', views.Delete_Blog.as_view(), name='delete_blog'), # blog

    # FAQ
    url(r'^add-faqs', views.Add_Faq.as_view(), name='add_faqs'),
    url(r'^view-faqs', views.List_Faq.as_view(), name='view_faqs'),
    url(r'^edit-faqs/(?P<pk>\d+)', views.Edit_Faq.as_view(), name='edit_faqs'),
    url(r'^delete-faqs/(?P<pk>\d+)', views.Delete_Faq.as_view(), name='delete_faqs'), # FAQs

    # Testimonials
    url(r'^add-testimonial', views.Add_Testimonial.as_view(), name='add_testimonial'),
    url(r'^view-testimonials', views.List_Testimonial.as_view(), name='view_testimonials'),
    url(r'^edit-testimonial/(?P<pk>\d+)', views.Edit_Testimonial.as_view(), name='edit_testimonial'),
    url(r'^delete-testimonial/(?P<pk>\d+)', views.Delete_Testimonial.as_view(),name='delete_testimonial'),

    # gallery
    url(r'^add-photos', views.Add_Photos.as_view(), name='add_photos'),
    url(r'^view-gallery', views.List_Photos.as_view(), name='view_gallery'),
    url(r'^edit-gallery', views.Edit_Photos.as_view(), name='edit_gallery'),
    url(r'^delete-gallery/(?P<pk>\d+)', views.Delete_Photos.as_view(), name='delete_gallery'),


    # Trash
    url(r'^view-course-content-trash', views.List_Course_Content_Trash.as_view(), name='view_course_content_trash'), # Trash
    url(r'^restore_course_content/(?P<pk>\d+)', views.Restore_Course_Content.as_view(), name='restore_course_content'),  # blog
    url(r'^delete_course_content_permanent/(?P<pk>\d+)', views.Delete_Course_Content_Permanent.as_view(), name='delete_course_content_permanent'),  # blog


    url(r'^view-blog-trash', views.List_Blog_Trash.as_view(), name='view_blog_trash'), # Trash
    url(r'^restore_blog/(?P<pk>\d+)', views.Restore_Blog.as_view(), name='restore_blog'),  # blog
    url(r'^delete_blog_permanent/(?P<pk>\d+)', views.Delete_Blog_Permanent.as_view(), name='delete_blog_permanent'),  # blog




    # notifications
    url(r'^add-notification', views.Add_notification.as_view(), name='add_notification'),
    url(r'^view-notifications', views.Notification_List.as_view(), name='view_notification'),
    url(r'^edit-notification', views.edit_notification, name='edit_notification'),
    url(r'^delete_notification/(?P<pk>\d+)', views.Delete_Notification.as_view(), name='delete_notification'),
    # blog
    url(r'^add-live', views.Add_Live.as_view(), name='add_live'),
    url(r'^view-live', views.Live_List.as_view(), name='view_live'),
    url(r'^delete_live/(?P<pk>\d+)', views.Delete_Live.as_view(), name='delete_live'),
    # blog



    #plans

    url(r'^plan-list', views.Plan_List.as_view(), name='plan_list'),
    url(r'^add-plan', views.Add_Plan.as_view(), name='add_plan'),
    url(r'^edit-plan/(?P<pk>\d+)', views.Edit_Plans.as_view(), name='edit_plan'),
    url(r'^delete_plan/(?P<pk>\d+)', views.Delete_Plan.as_view(), name='delete_plan'),
    # blog

    # admin URLs end
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

if DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [ url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_ROOT }),
                     # url(r'^uploads/course_photo/(?P<file>.*)$', views.serve_protected_document,
                     #     name='serve_protected_document'),

                     url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]

handler404 = views.handler
handler500 = views.handler50


