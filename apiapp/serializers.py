import datetime

from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from ieltsapp.forms import SetPasswordForm, PasswordResetForm

from ieltsclasses import settings

from ieltsapp.models import *





class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)












class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=allauth_settings.USERNAME_REQUIRED)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    main_course_category_id = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True, write_only=True)
    city = serializers.CharField(required=True, write_only=True)
    country = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.is_staff = False
        user.is_active = True
        user.save()

        aaaa = User_Profile()
        aaaa.mobile=request.data['mobile']
        aaaa.city=request.data['city']
        aaaa.country=request.data['country']
        aaaa.user_id=user
        aaaa.main_course_category_id = Main_Course_Category_Db.objects.get(id=request.data['main_course_category_id'])
        aaaa.exp_date = datetime.date.today() + datetime.timedelta(days=1)
        aaaa.save()

        return user





class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm_new_password = serializers.CharField(max_length=128)
    set_password_form_class = SetPasswordForm
    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = '__all__'






class Main_Course_Category_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Main_Course_Category_Db
        fields = '__all__'


class Super_Course_Category_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Super_Course_Category_Db
        fields = '__all__'



class Sub_Course_Category_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Sub_Course_Category_Db
        fields = '__all__'



class Course_Content_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Course_Content_Db
        fields = '__all__'

class Course_Content_Serializers_save_db(serializers.ModelSerializer):
    # main_course_category_id = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Main_Course_Category_Db.objects.all(),required=False)
    # super_course_category_id = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Super_Course_Category_Db.objects.all(),required=False)
    # sub_course_category_id = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Sub_Course_Category_Db.objects.all(),required=False)
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=10000,required=False)
    class Meta:
        model = Course_Content_Db
        fields = ['title','image','details']


# admin panle start here



class User_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = User
        fields = ["id","is_superuser","username","email","is_staff","is_active","user_type"]




class Plan_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Plan_Db
        fields = '__all__'


class Batch_Serializers_db(serializers.ModelSerializer):
    # services_id = serializers.CharField(max_length=1000,required=False)
    # title = serializers.CharField(max_length=1000,required=False)
    class Meta:
        model = Batch_Db
        fields = '__all__'



class Notification_Serializers_db(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=1000,required=False)
    # batch = serializers.StringRelatedField(many=True)
    class Meta:
        model = Notification_Db
        fields = '__all__'


class Notification_Serializers_save_db(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=1000,required=False)
    # batch = serializers.CharField(max_length=100,required=False)
    class Meta:
        model = Notification_Db
        fields ='__all__'
    # def __init__(self):
    #     batch_id= self.validated_data.get('batch_id', '')
    #     print(batch_id)





class Notification_Student_Serializers_db(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=1000,required=False)
    # batch = serializers.StringRelatedField(many=True)
    class Meta:
        model = Student_Notification_Db
        fields = '__all__'

class Live_Student_Serializers_db(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=1000,required=False)
    # batch = serializers.StringRelatedField(many=True)
    class Meta:
        model = Live_Notification_Db
        fields = '__all__'


class Notification_Student_Serializers_save_db(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100,required=False)
    image = serializers.FileField(required=False)
    details = serializers.CharField(max_length=1000,required=False)
    # batch = serializers.StringRelatedField(many=True)
    class Meta:
        model = Student_Notification_Db
        fields = ['title','image','details']



# class Course_Content_Serializers_db(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=100,required=False)
#     image = serializers.FileField(required=False)
#     details = serializers.CharField(max_length=1000,required=False)
#     class Meta:
#         model = Course_Content_Db
#         fields = '__all__'
#

