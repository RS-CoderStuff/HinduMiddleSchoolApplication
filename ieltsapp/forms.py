from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.forms import ModelForm
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, smart_str
from ieltsapp.models import *
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(user_type=2)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs

class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(user_type=1)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs

class Course_Content_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(user_type=1) | User.objects.filter(user_type=2)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        # print(qs)
        return qs




class Multi_User_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(is_staff=0)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs



class Sub_course_category_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Sub_Course_Category_Db.objects.all()
        if self.q:
            qs = qs.filter(sub_title__istartswith=self.q)
        return qs


class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.EmailField(max_length=254,label='Email Address',widget=forms.TextInput(attrs={'class': 'inputfield',}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
            # messeage =("There is no user registered with the specified email address!")
            # return redirect('../password_reset',locals())

            # return 'no'
        return email

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("Password Doesn't Match"),
    }
    new_password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'inputfield'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_new_password = forms.CharField(
        label=_("Confirm New Password "),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'inputfield'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm_new_password')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

UserModel = get_user_model()




class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        d = context
        plaintext = get_template('email-template/email.txt')
        htmly = get_template('email-template/forget-password.html')
        subject, from_email, to = 'Password reset on Tec', from_email, to_email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        # subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        # subject = ''.join(subject.splitlines())
        # body = loader.render_to_string(email_template_name, context)
        #
        # email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # if html_email_template_name is not None:
        #     html_email = loader.render_to_string(html_email_template_name, context)
        #     email_message.attach_alternative(html_email, 'text/html')
        #
        # email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )



USER_TYPE_CHOICES = (
      (0,'guest'),
      (1, 'teacher or admin'),
      (2, 'student'),
      (3, 'paid'),

  )




class PasswordChangeForm(SetPasswordForm):

    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Invalid Password"),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,'class': 'inputfield'}),
    )
    field_order = ['old_password', 'new_password1', 'new_password2']
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,required=True,label='Username', widget=forms.TextInput(attrs={'class': 'inputfield'}))
    first_name = forms.CharField(max_length=30,required=True,label='First Name', widget=forms.TextInput(attrs={'class': 'inputfield'}))
    last_name = forms.CharField(max_length=30,required=True,label='Last Name', widget=forms.TextInput(attrs={'class': 'inputfield'}))
    phone = forms.CharField(max_length=30,required=True,label='Mobile Number', widget=forms.NumberInput(attrs={'class': 'inputfield'}))
    city = forms.CharField(max_length=30,required=True,label='City', widget=forms.TextInput(attrs={'class': 'inputfield'}))
    main_course_category_id = forms.ModelChoiceField(required=True,label='Main Course',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    email = forms.EmailField(max_length=254,required=True, label='Email Address',widget=forms.EmailInput(attrs={'class': 'inputfield'}))
    confirm_email = forms.EmailField(max_length=254,required=True,label='Confirm Email Address', widget=forms.EmailInput(attrs={'class': 'inputfield'}))
    password1  = forms.CharField(label='Password',required=True,max_length=254,widget=forms.PasswordInput(attrs={'class': 'inputfield'}))
    password2  =forms.CharField(label='Confirm Password',required=True,max_length=254,widget=forms.PasswordInput(attrs={'class': 'inputfield',}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': False})
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 0
        user.is_active = True
        user.save()
        return user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        # if email == confirm_email:
        if email and User.objects.filter(email__iexact=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email already exists.')
        return email.strip()
    def clean_confirm_email(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        if email.strip() != confirm_email.strip():
            raise forms.ValidationError(u"Email Doesn't Match")
        return confirm_email.strip()











class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=254,required=True, widget=forms.EmailInput(attrs={'class': 'inputfield'}))
    password = forms.CharField(label='Password',required=True,max_length=254,widget=forms.PasswordInput(attrs={'class': 'inputfield'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email,is_active=True).exists():
            raise forms.ValidationError(
                "There is no user registered with the specified email address!")
        return email

# blogs
class Blog_Category_Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class': "inputfield"}))
    description = forms.CharField(required=True,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Blog_Category_Db
        fields = ['title', 'description']
    def clean_title(self):
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            list = Blog_Category_Db.objects.filter(title__iexact=title, id=self.instance.pk)
            if list:
                return title
            else:
                if title and Blog_Category_Db.objects.filter(title__iexact=title).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            if title and Blog_Category_Db.objects.filter(title__iexact=title).exists():
                    raise forms.ValidationError(u'Title already exists.')
        return title









class Blog_Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.ImageField(required=True,max_length=100,)
    author = forms.ModelChoiceField(required=True,queryset=User.objects.filter(is_superuser=1), empty_label="Select Author",widget=forms.Select(attrs={'class': "inputfield"}))
    Blog_Category_id = forms.ModelChoiceField(required=True,queryset=Blog_Category_Db.objects.all(), empty_label="Select Category",widget=forms.Select(attrs={'class': "inputfield"}))
    meta_title = forms.CharField(label='Meta Title',required=True,max_length=1000, widget=forms.TextInput(attrs={'class': "inputfield"}))
    meta_description = forms.CharField(label='Meta Description',required=True,max_length=1000, widget=forms.TextInput(attrs={'class': "inputfield"}))
    meta_keywords = forms.CharField(label='Meta Keywords',required=True,max_length=500, widget=forms.TextInput(attrs={'class': "inputfield"}))
    details = forms.CharField(required=True, max_length=3000, widget=CKEditorUploadingWidget())
    class Meta:
        # managed = False
        model = Blog_Db
        fields =['title','image' ,'author','Blog_Category_id','meta_title','meta_description','meta_keywords','details']
    def clean_title(self):
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            list = Blog_Db.objects.filter(title__iexact=title,id=self.instance.pk)
            if list:
                return title
            else:
                if title and Blog_Db.objects.filter(title__iexact=title).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            if title and Blog_Db.objects.filter(title__iexact=title).exists():
                raise forms.ValidationError(u'Title already exists.')
        return title


# blogs

# FAQs
class Faq_Form(forms.ModelForm):
    title = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    description = forms.CharField(max_length=1000,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    keywords = forms.CharField(max_length=1000,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    question = forms.CharField(max_length=1000,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    answer = forms.CharField(max_length=1000,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Faq_Db
        fields = ['title', 'description', 'keywords','question','answer']


# FAQs

# Testimonials
class Testimonial_Form(forms.ModelForm):
    client_name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    client_photo = forms.ImageField(required=True)
    review = forms.CharField(max_length=1000,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Testimonial_Db
        fields = ['client_name', 'client_photo','review']

    # def clean_title(self):
    #     print(self.instance.pk)
    #     if self.instance.pk != None:
    #         title = self.cleaned_data.get('title')
    #     else:
    #         title = self.cleaned_data.get('title')
    #         if title and Testimonial_Db.objects.filter(title=title).exists():
    #             raise forms.ValidationError(u'Title already exists.')
    #     return title



# Gallery
class Photos_Form(forms.ModelForm):
    gallery_photo = forms.ImageField(required=True)
    alternate_text = forms.CharField(required=False,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Gallery_Db
        fields = ['gallery_photo', 'alternate_text',]




class Main_Course_Category_Form(ModelForm):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.ImageField(max_length=100,label='Icon',)
    description = forms.CharField(required=False,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model= Main_Course_Category_Db
        fields = ['title','image','description']
    def clean_title(self):
        # print(self.instance.pk)
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            list = Main_Course_Category_Db.objects.filter(title__iexact=title, id=self.instance.pk)
            if list:
                return title
            else:
                if title and Main_Course_Category_Db.objects.filter(title__iexact=title).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            if title and Main_Course_Category_Db.objects.filter(title=title).exists():
                raise forms.ValidationError(u'Title already exists.')
        return title








class Super_Course_Category_Form(forms.ModelForm):
    main_course_category_id = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': "inputfield"}))
    description = forms.CharField(required=False,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model= Super_Course_Category_Db
        fields = ['main_course_category_id','title', 'description',]
    def clean_title(self):
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            main_course_category_id = self.cleaned_data.get('main_course_category_id')
            list = Super_Course_Category_Db.objects.filter(title__iexact=title,main_course_category_id=main_course_category_id, id=self.instance.pk)
            if list:
                return title
            else:
                if title and Super_Course_Category_Db.objects.filter(title__iexact=title,main_course_category_id=main_course_category_id).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            main_course_category_id = self.cleaned_data.get('main_course_category_id')
            if title and Super_Course_Category_Db.objects.filter(title__iexact=title,main_course_category_id=main_course_category_id).exists():
                    raise forms.ValidationError(u'In "Main Course Category" Title already exists.')
        return title



class Sub_Course_Category_Form(forms.ModelForm):
    main_course_category_id = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    super_course_category_id = forms.ModelChoiceField(label='Super Course Category',queryset=Super_Course_Category_Db.objects.none(), empty_label="Select Super Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': "inputfield"}))
    description = forms.CharField(required=False,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model= Sub_Course_Category_Db
        fields = ['main_course_category_id','super_course_category_id','title', 'description',]

    def clean_title(self):
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            main_course_category_id = self.cleaned_data.get('main_course_category_id')
            super_course_category_id = self.cleaned_data.get('super_course_category_id')
            list = Sub_Course_Category_Db.objects.filter(title__iexact=title,
                                                           main_course_category_id=main_course_category_id,super_course_category_id=super_course_category_id,
                                                           id=self.instance.pk)
            if list:
                return title
            else:
                if title and Sub_Course_Category_Db.objects.filter(title__iexact=title,
                                                                     main_course_category_id=main_course_category_id,super_course_category_id=super_course_category_id).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            super_course_category_id = self.cleaned_data.get('super_course_category_id')
            main_course_category_id = self.cleaned_data.get('main_course_category_id')
            if title and Sub_Course_Category_Db.objects.filter(title__iexact=title,main_course_category_id=main_course_category_id,super_course_category_id=super_course_category_id).exists():
                    raise forms.ValidationError(u'In "Main OR Super Course Category" Title already exists.')
        return title
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.none()
        if 'main_course_category_id' in self.data:
            try:
                main_course_category_id = int(self.data.get('main_course_category_id'))
                self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.filter(main_course_category_id=main_course_category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance:
            self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.filter(main_course_category_id=self.instance.main_course_category_id)




class Course_Content_Form(forms.ModelForm):
    # main_course_category_id = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    # super_course_category_id = forms.ModelChoiceField(label='Super Course Category',queryset=Super_Course_Category_Db.objects.none(), empty_label="Select Super Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    sub_course_category_id = forms.ModelMultipleChoiceField(label='Course Category',required=True,queryset=Sub_Course_Category_Db.objects.all(),widget=autocomplete.ModelSelect2Multiple(url='Sub_course_category_Autocomplete',attrs={'class': "inputfield"}))
    title = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.ImageField(label='Image',required=False,)
    pdf = forms.FileField(required=False,label='(.docx, .pptx, .pdf,.txt,.jpg,.png)')
    details = forms.CharField(required=False, max_length=3000, widget=forms.Textarea(attrs={'class': "form-control",'cols':''}))
    video2 = forms.FileField(required=False,label='(mp3 OR mp4)')
    type = forms.CharField(max_length=10,required=False)
    students = forms.ModelMultipleChoiceField(required=False,queryset=User.objects.all(),widget=autocomplete.ModelSelect2Multiple(url='Course_Content_Autocomplete',attrs={'class': "inputfield"}))
    class Meta:
        model = Course_Content_Db
        fields = [ 'sub_course_category_id', 'title', 'image','pdf','details' ,'video2','type','students']

    def clean_video2(self):
        video2 = self.cleaned_data.get('video2')
        if video2:
            xxx =smart_str(video2)
            ext = xxx.split('.')
            valid_extensions = ['mp3', 'mp4']
            if not ext[1].lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file extension.')
        return video2
    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if pdf:
            xxx =smart_str(pdf)
            ext = xxx.split('.')
            print(ext)
            valid_extensions = ['docx', 'pptx', 'pdf','txt','jpg','png']
            print(ext[1].lower())
            if not ext[1].lower()  in valid_extensions:
                raise forms.ValidationError('Unsupported file extension.')
        return pdf
    def clean_title(self):
        if self.instance.pk != None:
            title = self.cleaned_data.get('title')
            # main_course_category_id = self.cleaned_data.get('main_course_category_id')
            # super_course_category_id = self.cleaned_data.get('super_course_category_id')
            # sub_course_category_id = self.cleaned_data.get('sub_course_category_id')
            list = Course_Content_Db.objects.filter(title__iexact=title,id=self.instance.pk)
            if list:
                return title
            else:
                if title and Course_Content_Db.objects.filter(title__iexact=title).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return title
        else:
            title = self.cleaned_data.get('title')
            # super_course_category_id = self.cleaned_data.get('super_course_category_id')
            # main_course_category_id = self.cleaned_data.get('main_course_category_id')
            # sub_course_category_id = self.cleaned_data.get('sub_course_category_id')
            if title and Course_Content_Db.objects.filter(title__iexact=title).exists():
                raise forms.ValidationError(u'Title already exists.')
        return title

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.none()
    #     if 'main_course_category_id' in self.data:
    #         try: batch form nikla
    #             main_course_category_id = int(self.data.get('main_course_category_id'))
    #             self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.filter(
    #                 main_course_category_id=main_course_category_id)
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance:
    #         self.fields['super_course_category_id'].queryset = Super_Course_Category_Db.objects.filter(
    #             main_course_category_id=self.instance.main_course_category_id)
    #
    #     if 'super_course_category_id' in self.data:
    #         try:
    #             super_course_category_id = int(self.data.get('super_course_category_id'))
    #             self.fields['sub_course_category_id'].queryset = Sub_Course_Category_Db.objects.filter(
    #                 super_course_category_id=super_course_category_id)
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance:
    #         self.fields['sub_course_category_id'].queryset = Sub_Course_Category_Db.objects.filter(
    #             super_course_category_id=self.instance.super_course_category_id)
    #
    #


class Multi_User_Edit_Form(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=autocomplete.ModelSelect2Multiple(url='Multi_User_Autocomplete',attrs={'class': "inputfield"}))
    # class Meta:
    #     model = Batch_Db
    #     fields = ['students']


class Batch_Form(forms.ModelForm):
    name = forms.CharField(required=True,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    description = forms.CharField(required=True,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield"}))
    start_time = forms.CharField(label='Start Time',required=True,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield input-small timepicker"}))
    end_time = forms.CharField(label='End Time',required=True,max_length=1000,widget=forms.TextInput(attrs={'class': "inputfield input-small timepicker"}))
    category = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    teachers = forms.ModelMultipleChoiceField(required=False,queryset=User.objects.filter(user_type=1),widget=autocomplete.ModelSelect2Multiple(url='teacher-autocomplete',attrs={'class': "inputfield"}))
    type = forms.BooleanField(required=False)

    class Meta:
        model = Batch_Db
        fields = ['name', 'description', 'start_time', 'end_time', 'category', 'students','teachers','type']
    def __init__(self,  *args, **kwargs):
        super(Batch_Form, self).__init__(*args, **kwargs)
        if self.instance.pk != None:
            xxx= Batch_Db.objects.get(id=self.instance.pk)
            abc = xxx.category.id
            list = User_Profile.objects.filter(main_course_category_id=abc)
            batch_kliye.objects.filter(id=1).update(name=abc)
            aa = []
            for list in list:
                aa.append(list.user_id.id)
            self.fields['students'] = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.filter(id__in=aa,user_type=2),
                                                       widget=autocomplete.ModelSelect2Multiple(
                                                          url='get_main_course_user', attrs={'class': "inputfield"}))
        else:
            self.fields['students']  = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.filter(user_type=2),
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                          url='country-autocomplete', attrs={'class': "inputfield"}))
    def clean_name(self):
        if self.instance.pk != None:
            name = self.cleaned_data.get('name')
            list = Batch_Db.objects.filter(name__iexact=name, id=self.instance.pk)
            if list:
                return name
            else:
                if name and Batch_Db.objects.filter(name__iexact=name).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return name
        else:
            name = self.cleaned_data.get('name')
            if name and Batch_Db.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError(u'Title already exists.')
        return name





class Course_Form(forms.ModelForm):
    name = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Course Name",widget=forms.Select(attrs={'class': "inputfield"}))
    price = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.ImageField(max_length=100, required=True)
    details = forms.CharField(required=False, max_length=3000, widget=CKEditorUploadingWidget())
    meta_title = forms.CharField(label='Meta Title',max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    meta_description = forms.CharField(label='Meta Description',max_length=1000, widget=forms.TextInput(attrs={'class': "inputfield"}))
    meta_keywords = forms.CharField(label='Meta Keywords',max_length=1000, widget=forms.TextInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Course_Db
        fields = ['name', 'price', 'image','details', 'meta_title','meta_description','meta_keywords' ]

    def clean_name(self):
        if self.instance.pk != None:
            name = self.cleaned_data.get('name')
            list = Course_Db.objects.filter(name=name, id=self.instance.pk)
            if list:
                return name
            else:
                if name and Course_Db.objects.filter(name=name).exists():
                    raise forms.ValidationError(u'Title already exists.')
                return name
        else:
            name = self.cleaned_data.get('name')
            if name and Course_Db.objects.filter(name=name).exists():
                raise forms.ValidationError(u'Title already exists.')
        return name



class Contact_Us_Form(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=1000)
    find = forms.CharField(max_length=1000)
    message = forms.CharField(max_length=1000)
    class Meta:
        model = Contact_Us
        fields = ['name', 'email', 'find','message']



class Plan_Form(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    main_course_category_id = forms.ModelChoiceField(label='Main Course Category',queryset=Main_Course_Category_Db.objects.all(), empty_label="Select Main Course Category",widget=forms.Select(attrs={'class': "inputfield"}))
    price = forms.IntegerField( widget=forms.NumberInput(attrs={'class': "inputfield"}))
    days = forms.IntegerField( widget=forms.NumberInput(attrs={'class': "inputfield"}))
    class Meta:
        model = Plan_Db
        fields = ['name','main_course_category_id' ,'price', 'days']



class Notification__Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.FileField(required=False)
    details = forms.CharField(required=False,max_length=1000, widget=forms.Textarea(attrs={'class': "inputfield"}))
    batch = forms.ModelMultipleChoiceField(required=True,queryset=Batch_Db.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': "customcheckbox selectedId"}))
    class Meta:
        model = Notification_Db
        fields = ['title', 'image', 'details','batch']




class Notification_Student_Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.FileField(required=False)
    details = forms.CharField(required=False,max_length=1000, widget=forms.Textarea(attrs={'class': "inputfield"}))
    batch = forms.ModelMultipleChoiceField(required=True,queryset=Batch_Db.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': "customcheckbox selectedId"}))
    class Meta:
        model = Student_Notification_Db
        fields = ['title', 'image', 'details','batch']



class Live__Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.FileField(required=False)
    details = forms.CharField(required=False,max_length=1000, widget=forms.Textarea(attrs={'class': "inputfield"}))
    live_date = forms.CharField(required=False,max_length=1000,)
    batch = forms.ModelMultipleChoiceField(required=True,queryset=Batch_Db.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': "customcheckbox selectedId"}))
    class Meta:
        model = Live_Db
        fields = ['title', 'image', 'details','live_date','batch']




class Live_Student_Form(forms.ModelForm):
    title = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': "inputfield"}))
    image = forms.FileField(required=False)
    details = forms.CharField(required=False,max_length=1000, widget=forms.Textarea(attrs={'class': "inputfield"}))
    live_date = forms.CharField(required=False,max_length=1000)
    batch = forms.ModelMultipleChoiceField(required=True,queryset=Batch_Db.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': "customcheckbox selectedId"}))
    class Meta:
        model = Live_Notification_Db
        fields = ['title', 'image', 'details','live_date','batch']



        # fields = '__all__'

class get_main_course_user(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        aa =  batch_kliye.objects.get(id=1)

        print(aa)

        list = User_Profile.objects.filter(main_course_category_id=aa.name)


        aa = []
        for list in list:
            aa.append(list.user_id.id)

        qs=User.objects.filter(id__in=aa,user_type=2)
        print(qs,'------')
        if self.q:
            print(self.q,'---hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh----')
            qs = qs.filter(username__istartswith=self.q)
        return qs





class student_form(forms.Form):
    students = forms.ModelMultipleChoiceField(required=False,queryset=User.objects.filter(user_type=2),widget=autocomplete.ModelSelect2Multiple(url='get_main_course_user',attrs={'class': "inputfield"}))
