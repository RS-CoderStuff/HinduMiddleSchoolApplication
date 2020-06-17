from django.contrib.sites.shortcuts import get_current_site
from django.http.multipartparser import MultiPartParser
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from fcm_django.models import FCMDevice
from rest_auth.registration.app_settings import register_permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import (TokenSerializer, JWTSerializer, create_token, LoginSerializer)
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)



from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, AllowAny,IsAuthenticated
import json
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.views import APIView
from social_django.utils import psa
from apiapp.tokens import account_activation_token

from apiapp.serializers import *
from ieltsapp.models import *
from ieltsclasses.settings import WEB_SITE_URL

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)

import datetime



class PasswordResetView(GenericAPIView):

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )

class Singup(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(Singup, self).dispatch(*args, **kwargs)
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}
        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_response_data(user), status=status.HTTP_200_OK,headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)
        current_site = get_current_site(self.request)
        d = ({'email': user.email, 'username': user.username, 'WEB_SITE_URL': WEB_SITE_URL})
        plaintext = get_template('email-template/email.txt')
        htmly = get_template('email-template/welcome.html')
        subject, from_email, to = "Welcome To Tajinder's English Classes", settings.DEFAULT_FROM_EMAIL, user.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return user

from django.contrib.sessions.models import Session

from ieltsapp.models import LoggedInUser

class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)
    def process_login(self):
        django_login(self.request, self.user)
    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
            print(response_serializer)
        else:
            response_serializer = TokenSerializer
            print(response_serializer)
        return response_serializer
    def login(self):
        self.user = self.serializer.validated_data['user']
        django_login(self.request, self.user)

        print(self.user,"self.user")
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()
    def get_response(self, ):
        serializer_class = self.get_response_serializer()
        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,context={'request': self.request})
        # response = Response({'status': True, 'message': 'sucessfully','data':serializer.data}, status=status.HTTP_200_OK)
        if self.request.user.is_staff == 1:
            # response = Response(serializer.data, status=status.HTTP_200_OK)
            response = Response({'user_data': serializer.data, 'user_type': 1,'is_superuser':self.request.user.is_superuser}, status=status.HTTP_200_OK)

        elif self.request.user.is_staff == 0:
           print("************UserID***********");
           user_id = self.request.user.id;
           print(user_id);
           list_data = User_Profile.objects.get(user_id=user_id)
           import datetime
           date_today = datetime.date.today()
           if list_data.exp_date >= date_today:
               response = Response({'user_data': serializer.data,'user_type':0,'is_superuser':self.request.user.is_superuser}, status=status.HTTP_200_OK)
           else:
               response = Response({'user': 'user accont expire'}, status=200)
        else:
            response = Response({'user':'user does not exit'}, status=200)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)

        return response
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True,"message": "New password has been saved."},status=status.HTTP_200_OK)


class User_Device_list(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset = FCMDevice.objects.filter(user_id=request.user.id)
        dict ={}
        for queryset in queryset:
            dict.update(registration_id=queryset.registration_id)
        user = {'status': True, 'data':dict, 'message': 'device list'}
        return Response(user, status=status.HTTP_200_OK)




class User_Serializers_list(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset = User_Profile.objects.filter(user_id=request.user.id)

        # queryset = User_Profile.objects.filter(user_id=1)
        dict ={}
        for list in queryset:
            dict.update(user_id=smart_str(list.user_id.id))
            dict.update(username=smart_str(list.user_id.username))
            dict.update(email=smart_str(list.user_id.email))
            dict.update(type=smart_str(list.user_id.is_staff))
            dict.update(type=smart_str(list.user_id.is_staff))
            dict.update(main_course_category_id=list.main_course_category_id.id)
            dict.update(exp_date=list.exp_date)
        # serializer = Super_Course_Category_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':dict, 'message': 'user list'}
        return Response(user, status=status.HTTP_200_OK)

class Main_Course_Category_Singal_list(APIView):
    permission_classes = (AllowAny,)
    def get(self ,request, *args, **kwargs):
        id = kwargs['id']
        queryset = Main_Course_Category_Db.objects.filter(id=id)
        serializer = Main_Course_Category_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Main_Course_Category_Singal_list'}
        return Response(user, status=status.HTTP_200_OK)



class Main_Course_Category_list(APIView):
    permission_classes = (AllowAny,)
    def get(self ,request, *args, **kwargs):
            queryset = Main_Course_Category_Db.objects.all()
            serializer = Main_Course_Category_Serializers_db(queryset,many=True)
            user = {'status': True, 'data':serializer.data , 'message': 'Main_Course_Category'}
            return Response(user, status=status.HTTP_200_OK)




class Super_Course_Category_Serializers_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        main_course_category_id = kwargs['main_course_category_id']
        queryset = Super_Course_Category_Db.objects.filter(main_course_category_id=main_course_category_id)
        serializer = Super_Course_Category_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Super_Course_Category'}
        return Response(user, status=status.HTTP_200_OK)

class Sub_Course_Category_Serializers_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        super_course_category_id = kwargs['super_course_category_id']
        queryset = Sub_Course_Category_Db.objects.filter(super_course_category_id=super_course_category_id)
        serializer = Sub_Course_Category_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Sub_Course_Category'}
        return Response(user, status=status.HTTP_200_OK)

class Course_Content_Serializers_list(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        sub_course_category_id = kwargs['sub_course_category_id']
        queryset = Course_Content_Db.objects.filter(sub_course_category_id=sub_course_category_id,trash=1,type=0) | Course_Content_Db.objects.filter(students=request.user.id,sub_course_category_id=sub_course_category_id,trash=1,type=1)
        serializer = Course_Content_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Course_Content_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)



class Course_Content_Serializers_Private(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset = Course_Content_Db.objects.filter(trash=1,students=request.user.id,type=1)
        serializer = Course_Content_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Course_Content_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)



class Course_Content_Serializers_Single(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        queryset = Course_Content_Db.objects.filter(id=id,trash=1)
        serializer = Course_Content_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Course_Content_Serializers_Single'}
        return Response(user, status=status.HTTP_200_OK)



class Course_Content_Serializers_Save(APIView):
    permission_classes = (AllowAny,)
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        sub_course_category_id = request.data['sub_course_category_id']
        sub_course_category_id = Sub_Course_Category_Db.objects.get(id=sub_course_category_id)
        sub_course_category_id =[sub_course_category_id]

        # print(request.data)
        serializer = Course_Content_Serializers_save_db(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save(sub_course_category_id=sub_course_category_id)
            user = {'status': True, 'user': serializer.data, 'message': 'Course_Content_Serializers Save'}
            return Response(user, status=status.HTTP_200_OK)
        return Response({'status': False, 'message': 'errors'}, status=status.HTTP_400_BAD_REQUEST)


class Uplode_Noti(APIView):
    permission_classes = (AllowAny,)
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        serializer = Notification_Serializers_save_db(data=request.data)
        if serializer.is_valid():
            serializer.save()
            batch_id = request.data['batch_id']
            batch_id = int(batch_id)
            bbb =  Batch_Db.objects.get(id=batch_id)
            xxx =Notification_Db.objects.get(id=serializer.data['id'])
            xxx.batch.add(bbb)
            xxx.save()
            list =  Batch_Db.objects.filter(id=batch_id)
            for x in list:
                for b in x.students.all():
                    print(b.id)
                    serializer_1 = Notification_Student_Serializers_save_db(data=request.data)
                    if serializer_1.is_valid():
                        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                        serializer_1.save(notification_id=serializer.data['id'],student_id=b.id)
                    devices = FCMDevice.objects.filter(user_id=b.id)
                    aa ={'data':serializer.data,'notification_code':1}
                    devices.send_message(title="TECOnline",body="New Message",data={"test":aa})
            user = {'status': True, 'user': serializer.data, 'message': 'Course_Content_Serializers Save'}
            return Response(user, status=status.HTTP_200_OK)
        return Response({'status': True, 'message': 'error', 'data': serializer.errors}, status=400)





# admin panel api start here



class User_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                # dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
        user = {'status': True, 'data':list , 'message': 'User_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)




class Guest_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(user_type=0,is_staff=0)
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id.id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
        user = {'status': True, 'data':list , 'message': 'Guest_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)




class Teacher_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(user_type=1)
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id.id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
        user = {'status': True, 'data':list , 'message': 'Teacher_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)




class Student_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(user_type=2)
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id.id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
        user = {'status': True, 'data':list , 'message': 'Student_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)




class Paid_User_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(user_type=3)
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id.id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
         # serializer = User_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':list , 'message': 'Paid_User_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)



class Single_User_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        id_data = kwargs['id']
        queryset = User.objects.filter(id=id_data)
        list = []
        for i in queryset:
            dict ={}
            dict.update(user_id=i.id)
            dict.update(is_superuser=i.is_superuser)
            dict.update(username=i.username)
            dict.update(email=i.email)
            dict.update(is_staff=i.is_staff)
            dict.update(is_active=i.is_active)
            dict.update(user_type=i.user_type)
            queryset_2 = User_Profile.objects.filter(user_id=i.id)
            if queryset_2:
                for x in queryset_2:
                    dict.update(mobile=x.mobile)
                    # dict.update(main_course_category_id=x.main_course_category_id.id)
                    dict.update(exp_date=x.exp_date)
            else:
                dict.update(mobile='')
                dict.update(main_course_category_id='')
                dict.update(exp_date='')
            list.append(dict)
         # serializer = User_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':list , 'message': 'Paid_User_Serializers_list'}
        return Response(user, status=status.HTTP_200_OK)




class User_Edit_Api(APIView):
    permission_classes = (AllowAny,)
    model = User_Profile
    def post(self,request,*args, **kwargs):
        user_id = request.POST['user_id']
        exp_date = request.POST['exp_date']
        user_type = request.POST['user_type']
        exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
        if int(user_type) == 1:
            User.objects.filter(pk=user_id).update(user_type=user_type,is_staff=1)
        else:
            User.objects.filter(pk=user_id).update(user_type=user_type,is_staff=0)
        self.model.objects.filter(user_id=user_id).update(exp_date=exp_date)
        return Response({'status': True, 'message': 'sucessfully'}, status=status.HTTP_200_OK)



class Plan_Serializers_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = Plan_Db.objects.all()
        serializer = Plan_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'plan list'}
        return Response(user, status=status.HTTP_200_OK)


class Plan_Serializers_User(APIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        data = User_Profile.objects.get(user_id=request.user.id)
        print(data.main_course_category_id.id)
        queryset = Plan_Db.objects.filter(main_course_category_id=data.main_course_category_id.id)
        serializer = Plan_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'plan list'}
        return Response(user, status=status.HTTP_200_OK)


class Batch_Serializers_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = Batch_Db.objects.all()
        serializer = Batch_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Batch list'}
        return Response(user, status=status.HTTP_200_OK)






#

#
# #
# class Uplode_noti(APIView):
#     permission_classes = (AllowAny,)
#     parser_class = (FileUploadParser,)
#     def post(self, request, *args, **kwargs):
#         serializer = Notification_Serializers_save_db(data=request.data)
#         # print(serializer.data)
#
#         print('-------------------------------------------')
#         if serializer.is_valid():
#             print('hhhhhhhhhhhhh')
#             serializer.save()
#             print(serializer.data)
#             # xxx =Notification_Db.objects.get(id=serializer.data['id'])
#             # xxx.batch.add(bbb)
#             # xxx.save()
#             # list =  Batch_Db.objects.filter(id=batch_id)
#             # for x in list:
#             #     for b in x.students.all():
#             #         serializer_1 =  Notification_Student_Serializers_db(data=request.data)
#             #         if serializer_1.is_valid():
#             #             serializer_1.save(notification_id=serializer.data['id'],student_id=b.id)
#             #         devices = FCMDevice.objects.filter(user_id=b.id)
#             #         aa ={'data':serializer.data,'notification_code':1}
#             #         devices.send_message(title="TECOnline",body="New Message",data={"test":aa})
#             # return Response({'status': True, 'message': 'sucessfully', 'data':{'batch_id':batch_id,'title':serializer.data['title'],'details':serializer.data['details'],'image':smart_str(serializer.data['image'])}}, status=200)
#         return Response({'status': True, 'message': 'error', 'data': serializer.errors}, status=400)
#



class Notification_Serializers_list(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        queryset = Notification_Db.objects.all()
        serializer = Notification_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Notification list'}
        return Response(user, status=status.HTTP_200_OK)



class Notification_Serializers_single(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        id_data = kwargs['id']
        queryset = Notification_Db.objects.filter(id=id_data)
        serializer = Notification_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Notification list'}
        return Response(user, status=status.HTTP_200_OK)



class Student_Notification_Serializers_list(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset=Student_Notification_Db.objects.filter(student_id=request.user.id)
        serializer = Notification_Student_Serializers_db(queryset, many=True)
        user = {'status': True, 'data': serializer.data, 'message': 'Student Notification list'}
        return Response(user, status=status.HTTP_200_OK)



class Student_single(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        id_data = kwargs['id']
        queryset = Student_Notification_Db.objects.filter(id=id_data)
        # queryset = Student_Notification_.Db.objects.all()
        serializer = Notification_Student_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'Notification list'}
        return Response(user, status=status.HTTP_200_OK)





class Live_Notification_Serializers_list(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        queryset=Live_Notification_Db.objects.filter(student_id=request.user.id)
        serializer = Live_Student_Serializers_db(queryset, many=True)
        user = {'status': True, 'data': serializer.data, 'message': 'Student live list'}
        return Response(user, status=status.HTTP_200_OK)



class Live_single(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        id_data = kwargs['id']
        queryset = Live_Notification_Db.objects.filter(id=id_data)
        # queryset = Student_Notification_.Db.objects.all()
        serializer = Live_Student_Serializers_db(queryset,many=True)
        user = {'status': True, 'data':serializer.data , 'message': 'live list'}
        return Response(user, status=status.HTTP_200_OK)




class version111(APIView):
    permission_classes(AllowAny)
    def get(self,request, *args,**kwargs):
        print('11111111111111111111')
        data = {"version":26}
        return Response(data,status=status.HTTP_200_OK)
