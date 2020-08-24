import razorpay
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PyODConverter import DocumentConverter
from pdf2image import convert_from_path
from fcm_django.models import FCMDevice
from django.db.models import Q
import datetime

from apiapp.tokens import account_activation_token
from ieltsapp.forms import *
from ieltsapp.models import *
from ieltsclasses import settings
from ieltsclasses.settings import BASE_DIR, WEB_SITE_URL
import phonenumbers
from phonenumbers.phonenumberutil import (

    region_code_for_number,
)

client = razorpay.Client(auth=("rzp_live_2hQX2O1sphWJK4", "ybUOaopHhynTWymSvvjwFxD9"))

from fpdf import FPDF




import pycountry


def aaa(request):
    return render(request, 'account-verify1.html', locals())

def payment_successful(request):
    return render(request, 'payment-successful.html', locals())

def cancel_payment(request):
    return render(request, 'cancel-payment.html', locals())



def student_login(request):
    redirect_to = request.GET.get('next','')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():

            email = request.POST['email']
            password = request.POST['password']
            try:
                username = User.objects.get(email=email.lower()).username
                user = authenticate(request, username=username, password=password)
            except:
                user = None
                messages.error(request, "Your Email Address or Password was not recognized")
            if user is not None:
                auth.login(request, user)
                if request.user.is_superuser == 1:
                    return redirect(reverse('dashboard'))
                else:
                    return redirect(redirect_to)
            else:
                messages.error(request, "Your Email Address or Password was not recognized")
        else:
            return render(request, 'sign-in.html', locals())

    else:
        form = UserLoginForm()
    return render(request, 'student-login.html', locals())





class Student_Sign_Up(SuccessMessageMixin,CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'student-signup.html'
    def post(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        print(redirect_to)
        print('------------------------------')

        form =self.form_class(request.POST)
        countryCode = request.POST['countryCode']
        print(countryCode)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form_1 = form.save()
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            get_ct = '+'+countryCode+phone
            pn = phonenumbers.parse(get_ct)
            country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
            main_course_category_id = form.cleaned_data.get('main_course_category_id')
            user_profile = User_Profile()
            user_profile.user_id = form_1
            user_profile.main_course_category_id = main_course_category_id
            user_profile.mobile = get_ct
            user_profile.city = city
            user_profile.country = country.name
            user_profile.exp_date = datetime.date.today() + datetime.timedelta(days=1)
            user_profile.save()
            to_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            current_site = get_current_site(request)
            use_https = False
            d = ({'email': to_email,'username':username, 'WEB_SITE_URL': WEB_SITE_URL})
            plaintext = get_template('email-template/email.txt')
            htmly = get_template('email-template/welcome.html')
            subject, from_email, to = "Welcome To Tajinder's English Classes", settings.DEFAULT_FROM_EMAIL, to_email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            #msg.send()
            if redirect_to != '':
                return redirect(redirect_to)
            else:
                return redirect(reverse('index'))


        return render(request, self.template_name, locals())
    def get(self, request, *args, **kwargs):
        form  = self.form_class
        return render(request,self.template_name,locals())




def view_awards(request):
    return render(request, 'view-awards.html', locals())


def all_awards(request):
    gallery_list=Gallery_Db.objects.all().order_by('-id')
    return render(request, 'all-awards.html', locals())




def invalid(request):
    return render(request, 'invalid-activation.html', locals())



class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser == 1:
            pass
        else:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)




def handler(request, *args, **argv):
    return render(request, "404.html", locals())


def handler50(request):
    return render(request, "404.html", locals())

def index(request):
    gallery_list = Gallery_Db.objects.all().order_by('-id')[:9]
    faq_list = Faq_Db.objects.all().order_by('-id')[:6]
    blog_list = Blog_Db.objects.all().order_by('-id')[:3]
    testimonial_list = Testimonial_Db.objects.all().order_by('-id')[:6]
    course_list = Course_Db.objects.all().order_by('-id')[:6]
    return render(request , 'index.html',locals())

def policy(request):
    return render(request , 'policy.html',locals())


def blog(request):
    recent_blog_list = Blog_Db.objects.all().order_by('-id')[:8]
    blog_list = Blog_Db.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'blogs.html',locals())


def blog_details(request, slug):
    recent_blog_list=Blog_Db.objects.all().order_by('-id')[:8]
    blog_list=Blog_Db.objects.filter(slug=slug)
    return render(request , 'blog-details.html',locals())



def buy_course(request,pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            course_data = Course_Db.objects.get(id=pk)
            course_list = Course_Db.objects.filter(id=pk)
        else:
            user_list = User_Profile.objects.get(user_id=request.user.id)
            course_data = Course_Db.objects.get(name=user_list.main_course_category_id.id)
            course_list = Course_Db.objects.filter(name=user_list.main_course_category_id.id)
    else:
        course_data = Course_Db.objects.get(id=pk)
        course_list = Course_Db.objects.filter(id=pk)
    DATA = {'amount': int(course_data.price) * 100, 'currency': 'INR', 'receipt': course_data.name.title, 'payment_capture': 1}
    amount = int(course_data.price) * 100
    order_data = client.order.create(data=DATA)
    return render(request , 'buy-course.html',locals())


def paymentstatus(request,pair):
    payment_id = pair
    resp = client.payment.fetch(payment_id)
    print(resp)
    rp_id = resp['id']
    rp_order_id = resp['order_id']
    description = resp['description']
    email = resp['email']
    print(email,description)
    d = ({'email': email, 'username': request.user.username, 'WEB_SITE_URL': WEB_SITE_URL})
    plaintext = get_template('email-template/email.txt')
    htmly = get_template('email-template/payment-succuss-email.html')
    subject, from_email, to = "Welcome To Tajinder's English Classes Payment Successfully !", settings.DEFAULT_FROM_EMAIL, email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    #msg.send()


    # print(rp_id,rp_order_id )
    return render(request, 'payment-successful.html', locals())




@login_required(login_url="sign_in")
def tec_courses(request):
    if request.user.user_type == 2:
        main_course_category_list =Main_Course_Category_Db.objects.all().order_by('-id')
        _list =User_Profile.objects.filter(user_id=request.user.id)
        for xxx in _list:
            list = Sub_Course_Category_Db.objects.filter(main_course_category_id=xxx.main_course_category_id.id)
            co_list = Course_Content_Db.objects.filter(main_course_category_id=xxx.main_course_category_id.id)
    else:
        messages.success(request, "You don't have permission to access the content on website. \n Go to the Mobile Application for demo \n or \n Contact Administrator to access the content.!")
    return render(request , 'tec-courses.html',locals())



def load_sub_course_category_front(request):
    super_course_category_id = request.GET.get('super_course_category_id')
    # print(super_course_category_id)
    list = Sub_Course_Category_Db.objects.filter(super_course_category_id=super_course_category_id)
    co_list = Course_Content_Db.objects.filter(super_course_category_id=super_course_category_id)
    return render(request, 'load_sub_course_category_front.html',locals())



@login_required(login_url="sign_in")
def course_details(request,pk ,sub_id):
    if request.user.user_type == 2:
        pk = int(pk)
        list = Course_Content_Db.objects.filter(sub_course_category_id=sub_id,trash=1)
        main_list = Course_Content_Db.objects.filter(pk=pk,trash=1)
        for i in list:
            coure_name = i.main_course_category_id.title
        user_list = Images_data.objects.filter(course_id=pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        messages.success(request,"You don't have permission to access the content on website. \n Go to the Mobile Application for demo \n or \n Contact Administrator to access the content.!")
    return render(request , 'course-details.html',locals())


def verify_email(request):
    return render(request , 'verify-email.html')


def tec_pdf(request):
    return render(request , 'tec-pdf.html')

def crash_courses(request):
    course_list = Course_Db.objects.all().order_by('-id')[:6]
    return render(request , 'crash-courses.html',locals())


def enroll_now(request):
    return render(request , 'enroll-now.html')

def change_password(request):
    if request.user.is_superuser == 1:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your Password was successfully updated!')

            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request , 'admin/change-password.html',locals())

def sign_in(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            try:
                username = User.objects.get(email=email.lower()).username
                user = authenticate(request,username=username, password=password)
            except:
                user = None
                messages.error(request, "Your Email Address or Password was not recognized")
            if user is not None:
                auth.login(request, user)
                if request.user.is_superuser == 1:
                    return redirect(reverse('dashboard'))
                else:
                    logout(request)
                    return render(request, 'account-verify1.html', locals())
            else:
                messages.error(request, "Your Email Address or Password was not recognized")
        else:
            return render(request, 'sign-in.html', locals())

    else:
        form = UserLoginForm()
    return render(request , 'sign-in.html',locals())



class Sign_Up(SuccessMessageMixin,CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign-up.html'
    def post(self, request, *args, **kwargs):
        form =self.form_class(request.POST)
        countryCode = request.POST['countryCode']
        print(countryCode)
        if form.is_valid():
            form_1 = form.save()
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            get_ct = '+'+countryCode+phone
            pn = phonenumbers.parse(get_ct)
            country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
            main_course_category_id = form.cleaned_data.get('main_course_category_id')
            user_profile = User_Profile()
            user_profile.user_id = form_1
            user_profile.main_course_category_id = main_course_category_id
            user_profile.mobile = get_ct
            user_profile.city = city
            user_profile.country = country.name
            user_profile.exp_date = datetime.date.today() + datetime.timedelta(days=1)
            user_profile.save()
            to_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            current_site = get_current_site(request)
            use_https = False
            d = ({'email': to_email,'username':username, 'WEB_SITE_URL': WEB_SITE_URL})
            plaintext = get_template('email-template/email.txt')
            htmly = get_template('email-template/welcome.html')
            subject, from_email, to = "Welcome To Tajinder's English Classes", settings.DEFAULT_FROM_EMAIL, to_email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            #msg.send()
            return render(request, 'account-verify.html', locals())
        return render(request, self.template_name, locals())
    def get(self, request, *args, **kwargs):
        form  = self.form_class
        return render(request,self.template_name,locals())


class Contact_us_save(View):
    model = Contact_Us
    form_class = Contact_Us_Form
    template_name = 'contact-meesage.html'
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            d = ({'email': email,'WEB_SITE_URL':WEB_SITE_URL})
            plaintext = get_template('email-template/email.txt')
            htmly = get_template('email-template/confirm-contact.html')
            subject, from_email, to = "Welcome To Tajinder's English Classes. Thank you for Contact us", settings.DEFAULT_FROM_EMAIL, email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            #msg.send()
            # messages.success(request, "Thank you for Contact us")
            return render(request, self.template_name, locals())
        messages.success(request, "Something went wrong")
        return render(request,self.template_name,locals())




def register_send_mails(emails):
    d = ({'email': emails,'WEB_SITE_URL':WEB_SITE_URL})
    plaintext = get_template('email-template/email.txt')
    htmly = get_template('email-template/welcome.html')
    subject, from_email, to = "Welcome To Tajinder's English Classes", settings.DEFAULT_FROM_EMAIL, emails
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    #msg.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        # register_send_mails(request.user.email)

        return redirect(reverse('verify_email'))
    else:
        return redirect(reverse('invalid'))

        # return HttpResponse('Activation link is invalid!')






class Dashboard(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/dashboard.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().count()
        context['guest'] = User.objects.filter(user_type=0,is_staff=0).count()
        context['teacher'] = User.objects.filter(user_type=1).count()
        context['student'] = User.objects.filter(user_type=2).count()
        context['paid'] = User.objects.filter(user_type=3).count()
        context['Category_Db'] = Main_Course_Category_Db.objects.all().count()
        context['Batch'] = Batch_Db.objects.all().count()
        # all_user = User.objects.all().count()
        return context



# users
def profile(request):
    return render(request , 'admin/profile.html')






class List_All_Contact(LogoutIfNotStaffMixin,TemplateView):
    model = Contact_Us
    template_name = 'admin/contact-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context


class Delete_Contact(SuccessMessageMixin, LogoutIfNotStaffMixin,View):
    model = Contact_Us
    success_message ='Contact Deleted Successfully'
    success_url = reverse_lazy('contact_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)



class User_Edit(LogoutIfNotStaffMixin,View):
    model = User_Profile
    template_name = 'admin/user-edit.html'
    def get(self,request,*args, **kwargs):
        user_id = kwargs['pk']
        list = self.model.objects.filter(user_id=user_id)
        Main_Course_Category_list = Main_Course_Category_Db.objects.all()

        return render(request,self.template_name,locals())
    def post(self,request,*args, **kwargs):
        user_id = request.POST['user_id']
        exp_date = request.POST['exp_date']
        user_type = request.POST['user_type']
        main_course_category_id = request.POST['main_course_category_id']
        main_course_category_id = Main_Course_Category_Db.objects.get(id=main_course_category_id)
        exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
        if int(user_type) == 1:
            User.objects.filter(pk=user_id).update(user_type=user_type,is_staff=1)
        else:
            User.objects.filter(pk=user_id).update(user_type=user_type,is_staff=0)
        self.model.objects.filter(user_id=user_id).update(exp_date=exp_date,main_course_category_id=main_course_category_id)
        list = self.model.objects.filter(user_id=user_id)
        Main_Course_Category_list = Main_Course_Category_Db.objects.all()
        messages.success(request, "User Updated Successfully")
        return render(request,self.template_name,locals())



def multi_user_edit(request):
    if request.method == "POST":
        form= Multi_User_Edit_Form(request.POST)
        user_type = request.POST['user_type']
        exp_date = request.POST['exp_date']
        exp_date = datetime.datetime.strptime(exp_date, "%Y-%m-%d").date()
        if form.is_valid():
            for xxx in form.cleaned_data['students']:
                if int(user_type) == 1:
                    User.objects.filter(id=xxx.id).update(user_type=user_type,is_staff=1)
                    User_Profile.objects.filter(user_id=xxx.id).update(exp_date=exp_date)
                else:
                    User.objects.filter(id=xxx.id).update(user_type=user_type,is_staff=0)
                    User_Profile.objects.filter(user_id=xxx.id).update(exp_date=exp_date)
            messages.success(request, "User Updated Successfully")
    else:
        form = Multi_User_Edit_Form()
    return render(request, 'admin/multi-user-edit.html', locals())




class List_All_User(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/user-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context



class Delete_User(SuccessMessageMixin, LogoutIfNotStaffMixin,View):
    model = User_Profile
    success_message ='User Deleted Successfully'
    success_url = reverse_lazy('users')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(user_id=id).delete()
        User.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)




class List_Paid_User(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/user-paid.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context

class List_Students_User(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/students.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context

class List_Guest_User(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/guest.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context

class List_Teacher_User(LogoutIfNotStaffMixin,TemplateView):
    model = User_Profile
    template_name = 'admin/teachers.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context





# batches


class Add_Batch(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Batch_Db
    form_class = Batch_Form
    success_url = reverse_lazy('view_batches')
    success_message =' Batch Added Successfully'
    template_name = 'admin/batch-add.html'



class List_Batch(LogoutIfNotStaffMixin,TemplateView):
    model = Batch_Db
    template_name = 'admin/batch-list.html'
    #  = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context



class Edit_Batch(SuccessMessageMixin, LogoutIfNotStaffMixin,UpdateView):
    model = Batch_Db
    form_class = Batch_Form
    template_name = 'admin/batch-edit.html'
    success_message ='Batch Updated Successfully'
    success_url = reverse_lazy('view_batches')




class Delete_Batch(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Batch_Db
    success_message ='Batch Deleted Successfully'
    success_url = reverse_lazy('view_batches')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)

# batches


#Main_Course_Category
class Add_Main_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Main_Course_Category_Db
    form_class = Main_Course_Category_Form
    success_url = reverse_lazy('list_course_category')
    success_message =' Main Course Category Added Successfully'
    template_name = 'admin/course-category-add.html'




class List_Main_Course_Category(LogoutIfNotStaffMixin,TemplateView):
    model = Main_Course_Category_Db
    template_name = 'admin/course-category-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context




class Delete_Main_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Main_Course_Category_Db
    success_message ='Main Course Category Deleted Successfully'
    success_url = reverse_lazy('list_course_category')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


class Edit_Main_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Main_Course_Category_Db
    form_class = Main_Course_Category_Form
    template_name = 'admin/course-category-edit.html'
    success_message ='Main Course Category Updated Successfully'
    success_url = reverse_lazy('list_course_category')



class Add_Super_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Super_Course_Category_Db
    form_class = Super_Course_Category_Form
    success_url = reverse_lazy('course_super_category_list')
    success_message =' Super Course Category Added Successfully'
    template_name = 'admin/course-super-category-add.html'



class List_Super_Course_Category(LogoutIfNotStaffMixin,ListView,):
    model = Super_Course_Category_Db
    template_name = 'admin/course-super-category-list.html'
    paginate_by = 10  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super(List_Super_Course_Category, self).get_context_data(**kwargs)
        list = Super_Course_Category_Db.objects.all()
        id = self.request.GET.get('id')
        if id != None:
            list = Super_Course_Category_Db.objects.filter(main_course_category_id=id)
        print(id)
        main_list = Main_Course_Category_Db.objects.all()
        paginator = Paginator(list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        context['list'] = list
        context['main_list'] = main_list
        return context



class Delete_Super_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Super_Course_Category_Db
    success_message ='Super Course Category Deleted Successfully'
    success_url = reverse_lazy('course_super_category_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


class Edit_Super_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Super_Course_Category_Db
    form_class = Super_Course_Category_Form
    template_name = 'admin/course-super-category-edit.html'
    success_message ='Super Course Category Updated Successfully'
    success_url = reverse_lazy('course_super_category_list')



# Sub_Course_Category
class Add_Sub_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Sub_Course_Category_Db
    form_class = Sub_Course_Category_Form
    success_url = reverse_lazy('course_sub_category_list')
    success_message =' Sub Course Category Added Successfully'
    template_name = 'admin/course-sub-category-add.html'



def load_main_course_category(request):
    main_course_category_id = request.GET.get('main_course_category_id')
    print(main_course_category_id)
    list = Super_Course_Category_Db.objects.filter(main_course_category_id=main_course_category_id)
    return render(request, 'admin/main_course_category_dropdown.html',locals())


def load_sub_course_category(request):
    super_course_category_id = request.GET.get('super_course_category_id')
    print(super_course_category_id)
    list = Sub_Course_Category_Db.objects.filter(super_course_category_id=super_course_category_id)
    return render(request, 'admin/main_course_category_dropdown.html',locals())

def load_user(request):
    main_course_category_id = request.GET.get('main_course_category_id')
    print(main_course_category_id)
    if main_course_category_id =='':
        userList = User.objects.filter(user_type__in = [1,2])
    else:
        list = User_Profile.objects.filter(main_course_category_id=main_course_category_id)
        userList = User.objects.filter(Q(user_profile__in=list) | Q(user_type=1)).order_by('user_type')
    for ls in userList:
        print(ls.username, ls.user_type)
    return render(request, 'admin/user_dropdown.html',locals())





class List_Sub_Course_Category(LogoutIfNotStaffMixin,ListView):
    model = Sub_Course_Category_Db
    template_name = 'admin/course-sub-category-list.html'
    paginate_by = 10  # if pagination is desired
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['list'] = self.model.objects.all().order_by('-id')
    #     return context

    def get_context_data(self, **kwargs):
        context = super(List_Sub_Course_Category, self).get_context_data(**kwargs)
        list = Sub_Course_Category_Db.objects.all()

        id = self.request.GET.get('id')
        if id != None:
            list = Sub_Course_Category_Db.objects.filter(super_course_category_id=id)
        print(id)

        main_list = Super_Course_Category_Db.objects.all()

        paginator = Paginator(list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)

        context['list'] = list
        context['main_list'] = main_list
        return context






class Delete_Sub_Course_Category(SuccessMessageMixin, LogoutIfNotStaffMixin,View):
    model = Sub_Course_Category_Db
    success_message ='Sub Course Category Deleted Successfully'
    success_url = reverse_lazy('course_sub_category_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


class Edit_Sub_Course_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Sub_Course_Category_Db
    form_class = Sub_Course_Category_Form
    template_name = 'admin/course-sub-category-edit.html'
    success_message ='Sub Course Category Updated Successfully'
    success_url = reverse_lazy('course_sub_category_list')





class Add_Course_Content(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Course_Content_Db
    form_class = Course_Content_Form
    def get(self, request, *args, **kwargs):
        form = Course_Content_Form()
        return render(request, 'admin/course-content-add.html',locals())
    def post(self, request, *args, **kwargs):
        form = Course_Content_Form(request.POST,request.FILES)
        if form.is_valid():
           xxx =form.save()
           if xxx.pdf:
               aaa = xxx.pdf.path
               # content_data = self.model.objects.get(id=xxx.id)
               ext = aaa.split('.')
               if smart_str(ext[1]) != 'pdf':
                   if smart_str(ext[1]) == 'txt':
                       pdf = FPDF()
                       pdf.add_page()
                       pdf.set_font("Arial", size=8)
                       f = open(aaa, "r")
                       for x in f:
                           pdf.cell(200, 6, txt=x, ln=3, align='l')
                       pdf.output(ext[0] + '.pdf')
                       bbb_1 = ext[0].replace(BASE_DIR + '/uploads/', '')
                       self.model.objects.filter(id=xxx.id).update(pdf=bbb_1 + '.pdf')
                   elif smart_str(ext[1]) == 'jpg' or smart_str(ext[1]) == 'png':
                       print("Successfully save");
                   else:
                       listener = ('127.0.0.1', 2002)
                       converter = DocumentConverter(listener)
                       converter.convert(aaa, smart_str(ext[0]) + '.pdf')
                       print(BASE_DIR + '/ieltsclasses/uploads/')
                       bbb = ext[0].replace(BASE_DIR + '/uploads/', '')
                       self.model.objects.filter(id=xxx.id).update(pdf=bbb + '.pdf')
                       pages = convert_from_path(ext[0] + '.pdf', 100)
           messages.success(request, 'Course Content Added Successfully')
           return redirect('course_content_list')


                       # i = 1
                   # for page in pages:
                   #     i += 1
                   #     page.save(ext[0] + str(i) + '.jpg', 'JPEG')
                   #     xxx = ext[0] + str(i) + '.jpg'
                   #     bbb__ = xxx.replace(BASE_DIR + '/uploads/', '')
                   #     Images_data.objects.create(course_id=content_data, image=bbb__)
               # elif smart_str(ext[1]) == 'pdf':
                       # pages = convert_from_path(aaa, 100)
                       # i = 1
                       # for page in pages:
                       #     i += 1
                       #     page.save(ext[0] + str(i) + '.jpg', 'JPEG')
                       #     xxx = ext[0] + str(i) + '.jpg'
                       #     bbb__ = xxx.replace(BASE_DIR + '/uploads/', '')
                       #     Images_data.objects.create(course_id=content_data, image=bbb__)
           # form = self.form_class()

        return render(request, 'admin/course-content-add.html', locals())


class List_Course_Content(LogoutIfNotStaffMixin,TemplateView):
    model = Course_Content_Db
    template_name = 'admin/course-content-list.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.filter(trash=1)
        return context



#
# class Edit_Course_Content(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
#     model = Course_Content_Db
#     form_class = Course_Content_Form
#     template_name = 'admin/course-content-edit.html'
#     success_message ='Course Content Update Successfully'
#     success_url = reverse_lazy('course_content_list')
#

class Edit_Course_Content(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Course_Content_Db
    form_class = Course_Content_Form
    template_name = 'admin/course-content-edit.html'
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        instance= self.model.objects.get(id=id)
        form = Course_Content_Form(instance=instance)
        return render(request, self.template_name, locals())
    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        instance = self.model.objects.get(id=id)
        form = Course_Content_Form(request.POST, request.FILES,instance=instance)
        if form.is_valid():
           xxx =form.save()
           if xxx.pdf:
               aaa = xxx.pdf.path
               content_data = self.model.objects.get(id=xxx.id)
               ext = aaa.split('.')
               if smart_str(ext[1]) != 'pdf':
                   if smart_str(ext[1]) == 'txt':
                       pdf = FPDF()
                       pdf.add_page()
                       pdf.set_font("Arial", size=8)
                       f = open(aaa, "r")
                       for x in f:
                           pdf.cell(200, 6, txt=x, ln=3, align='l')
                       pdf.output(ext[0] + '.pdf')
                       bbb_1 = ext[0].replace(BASE_DIR + '/uploads/', '')
                       self.model.objects.filter(id=xxx.id).update(pdf=bbb_1 + '.pdf')
                   else:
                       listener = ('127.0.0.1', 2002)
                       converter = DocumentConverter(listener)
                       converter.convert(aaa, smart_str(ext[0]) + '.pdf')
                       print(BASE_DIR + '/ieltsclasses/uploads/')
                       bbb = ext[0].replace(BASE_DIR + '/uploads/', '')
                       self.model.objects.filter(id=xxx.id).update(pdf=bbb + '.pdf')
                       pages = convert_from_path(ext[0] + '.pdf', 100)
           messages.success(request, 'Course Content Updated Successfully')
           return redirect('course_content_list')



                   # i = 1
                   # for page in pages:
                   #     i += 1
                   #     page.save(ext[0] + str(i) + '.jpg', 'JPEG')
                   #     xxx = ext[0] + str(i) + '.jpg'
                   #     bbb__ = xxx.replace(BASE_DIR + '/uploads/', '')
                   #     Images_data.objects.create(course_id=content_data, image=bbb__)
               # elif smart_str(ext[1]) == 'pdf':
                       # pages = convert_from_path(aaa, 100)
                       # i = 1
                       # for page in pages:
                       #     i += 1
                       #     page.save(ext[0] + str(i) + '.jpg', 'JPEG')
                       #     xxx = ext[0] + str(i) + '.jpg'
                       #     bbb__ = xxx.replace(BASE_DIR + '/uploads/', '')
                       #     Images_data.objects.create(course_id=content_data, image=bbb__)
        return render(request, self.template_name, locals())


class Delete_Course_Content(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Course_Content_Db
    success_message ='Course Content Deleted Successfully'
    success_url = reverse_lazy('course_content_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).update(trash=0)
        messages.error(request,self.success_message)
        return redirect('course_content_list')




class Add_Course(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Course_Db
    form_class = Course_Form
    success_url = reverse_lazy('course_list')
    success_message ='Course Added Successfully'
    template_name = 'admin/course-add.html'




class List_Course(LogoutIfNotStaffMixin,TemplateView):
    model = Course_Db
    template_name = 'admin/course-list.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context

class Delete_Course(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Course_Db
    success_message ='Course Deleted Successfully'
    success_url = reverse_lazy('course_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


class Edit_Course(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Course_Db
    form_class = Course_Form
    template_name = 'admin/course-edit.html'
    success_message ='Course Updated Successfully'
    success_url = reverse_lazy('course_list')






def fee_list(request):
    return render(request , 'admin/course-fee-list.html')
# courses

# blog
class Add_Blog_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Blog_Category_Db
    form_class = Blog_Category_Form
    success_url = reverse_lazy('list_blog_category')
    success_message =' Blog Category Added Successfully'
    template_name = 'admin/blog-category-add.html'




class List_Blog_Category(TemplateView,LogoutIfNotStaffMixin):
    model = Blog_Category_Db
    template_name = 'admin/blog-category-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context


class Delete_Blog_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Blog_Category_Db
    success_message ='Blog Category Deleted Successfully'
    success_url = reverse_lazy('list_blog_category')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


class Edit_Blog_Category(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Blog_Category_Db
    form_class = Blog_Category_Form
    template_name = 'admin/blog-category-edit.html'
    success_message ='Blog Category Updated Successfully'
    success_url = reverse_lazy('list_blog_category')




class List_Blog(TemplateView,LogoutIfNotStaffMixin):
    model = Blog_Db
    template_name = 'admin/blog-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.filter(trash=1)
        return context


class Add_Blog(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Blog_Db
    form_class = Blog_Form
    success_url = reverse_lazy('blog_list')
    success_message =' Blog Post Added Successfully'
    template_name = 'admin/blog-add.html'




class Edit_Blog(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Blog_Db
    form_class = Blog_Form
    template_name = 'admin/blog-edit.html'
    success_message ='Blog Post Updated Successfully'
    success_url = reverse_lazy('blog_list')



class Delete_Blog(SuccessMessageMixin, LogoutIfNotStaffMixin,View):
    model = Blog_Db
    success_message ='Blog Post Deleted Successfully'
    success_url = reverse_lazy('blog_list')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).update(trash=0)
        messages.error(request,self.success_message)
        return redirect('blog_list')

# FAQs



class Add_Faq(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Faq_Db
    form_class = Faq_Form
    success_url = reverse_lazy('view_faqs')
    success_message =' FAQ Added Successfully'
    template_name = 'admin/faq-add.html'



class Edit_Faq(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Faq_Db
    form_class = Faq_Form
    template_name = 'admin/faq-edit.html'
    success_message ='FAQ Updated Successfully'
    success_url = reverse_lazy('view_faqs')



class List_Faq(TemplateView,LogoutIfNotStaffMixin):
    model = Faq_Db
    template_name = 'admin/faq-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context



class Delete_Faq(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Faq_Db
    success_message ='FAQ Deleted Successfully'
    success_url = reverse_lazy('view_faqs')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


# FAQs

# Testimonials

class Add_Testimonial(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Testimonial_Db
    form_class = Testimonial_Form
    success_url = reverse_lazy('view_testimonials')
    success_message =' New Testimonial Added Successfully'
    template_name = 'admin/testimonial-add.html'


class List_Testimonial(TemplateView,LogoutIfNotStaffMixin):
    model = Testimonial_Db
    template_name = 'admin/testimonial-list.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context


class Edit_Testimonial(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Testimonial_Db
    form_class = Testimonial_Form
    template_name = 'admin/testimonial-edit.html'
    success_message ='Testimonial Updated Successfully'
    success_url = reverse_lazy('view_testimonials')


class Delete_Testimonial(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Testimonial_Db
    success_message ='Testimonial Deleted Successfully'
    success_url = reverse_lazy('view_testimonials')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request,self.success_message)
        return redirect('view_testimonials')

# Testimonials

# gallery
class List_Photos(TemplateView,LogoutIfNotStaffMixin):
    model = Gallery_Db
    template_name = 'admin/gallery-view.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context


class Add_Photos(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Gallery_Db
    form_class = Photos_Form
    success_url = reverse_lazy('view_gallery')
    success_message =' New Photo Added Successfully'
    template_name = 'admin/gallery-add-photo.html'



class Edit_Photos(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Gallery_Db
    form_class = Photos_Form
    template_name = 'admin/gallery-view.html'
    def post(self,requset,*args,**kwargs):
        id = requset.POST['id']
        instance = self.model.objects.get(id=id)
        form =self.form_class(requset.POST,requset.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.success(requset,'Photo Updated Successfully')
            list = self.model.objects.all()
            return render(requset,self.template_name,locals())



class Delete_Photos(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Gallery_Db
    success_message ='Photo Deleted Successfully'
    success_url = reverse_lazy('view_gallery')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request, self.success_message)
        return redirect(self.success_url)


# gallery



class List_Blog_Trash(TemplateView,LogoutIfNotStaffMixin):
    model = Blog_Db
    template_name = 'admin/trash-blog.html'
    #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.filter(trash=0)
        return context


class Restore_Blog(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Blog_Db
    success_message ='Blog Restored Successfully'
    success_url = reverse_lazy('view_blog_trash')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).update(trash=1)
        messages.error(request,self.success_message)
        return redirect('view_blog_trash')


class Delete_Blog_Permanent(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Blog_Db
    success_message ='Blog Deleted Successfully'
    success_url = reverse_lazy('view_blog_trash')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request,self.success_message)
        return redirect('view_blog_trash')



class List_Course_Content_Trash(LogoutIfNotStaffMixin,TemplateView):
    model = Course_Content_Db
    template_name = 'admin/trash-course-content.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.filter(trash=0)
        return context



class Restore_Course_Content(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Course_Content_Db
    success_message ='Course Content Restored Successfully'
    success_url = reverse_lazy('view_course_content_trash')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).update(trash=1)
        messages.error(request,self.success_message)
        return redirect('view_course_content_trash')

class Delete_Course_Content_Permanent(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Course_Content_Db
    success_message ='Course Content Deleted Successfully'
    success_url = reverse_lazy('view_course_content_trash')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request,self.success_message)
        return redirect('view_course_content_trash')


# Trash

# notifications
class Add_notification(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    def get(self,request,*args, **kwargs):
        list = Batch_Db.objects.all().order_by('-id')
        form = Notification__Form()
        return render(request, 'admin/notification-add.html',locals())
    def post(self,request,*args, **kwargs):
        list = Batch_Db.objects.all()
        batch_id = request.POST.getlist('batch')
        form = Notification__Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            notification_id= Notification_Db.objects.latest('id')
            # print(notification_id.id)
            if len(batch_id) != 0:
                image = form.cleaned_data.get('image')
                print(image)
                # id = form.cleaned_data.get('id')
                # print(id)
                details = form.cleaned_data.get('details')
                print(details)
                print('------------------------')
                if image or details:
                    messages.success(request,'Notification Successfully Sent')
                    for i in batch_id:
                        list =  Batch_Db.objects.filter(id=i)
                        for x in list:
                            for b in x.students.all():
                                form_1 = Notification_Student_Form(request.POST, request.FILES)
                                form_11 =form_1.save(commit=False)
                                form_11.student_id=b.id
                                form_11.notification_id=notification_id.id
                                form_11.save()


                                # Student_Notification_Db.objects.create(notification_id=notification_id.id,student_id=b.id)

                                devices = FCMDevice.objects.filter(user_id=b.id)
                                aa ={'data':form.data,'notification_code':1}
                                devices.send_message(title="TECOnline",body="NeW Message",data={"test":aa})
                    return redirect('view_notification')
                    # list = Batch_Db.objects.all().order_by('-id')
                else:
                    messages.success(request, 'Please select image or text field')
            else:
                messages.success(request, 'Please select atleast one "Batch" ')
        # else:
        #
        #     messages.success(request,'Something  went wrong')
        return render(request, 'admin/notification-add.html',locals())



class Notification_List(LogoutIfNotStaffMixin,TemplateView):
    template_name = 'admin/notification-list.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Notification_Db.objects.all().order_by('-id')
        return context


class Delete_Notification(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Notification_Db
    success_message ='Notification Deleted Successfully'
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request,self.success_message)
        return redirect('view_notification')


#live ----------------------------
class Add_Live(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    def get(self,request,*args, **kwargs):
        list = Batch_Db.objects.all().order_by('-id')
        form = Live__Form()
        return render(request, 'admin/live-add.html',locals())
    def post(self,request,*args, **kwargs):
        list = Batch_Db.objects.all()
        batch_id = request.POST.getlist('batch')
        form = Live__Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            notification_id= Live_Db.objects.latest('id')
            # print(notification_id.id)
            if len(batch_id) != 0:
                image = form.cleaned_data.get('image')
                print(image)
                # id = form.cleaned_data.get('id')
                # print(id)
                details = form.cleaned_data.get('details')
                print(details)
                print('------------------------')
                if image or details:
                    messages.success(request,'Live Successfully Sent')
                    for i in batch_id:
                        list =  Batch_Db.objects.filter(id=i)
                        for x in list:
                            for b in x.students.all():
                                form_1 = Live_Student_Form(request.POST, request.FILES)
                                form_11 =form_1.save(commit=False)
                                form_11.student_id=b.id
                                form_11.notification_id=notification_id.id
                                form_11.save()


                                # Student_Notification_Db.objects.create(notification_id=notification_id.id,student_id=b.id)

                                devices = FCMDevice.objects.filter(user_id=b.id)
                                aa ={'data':form.data,'notification_code':1}
                                devices.send_message(title="TECOnline",body="NeW Message",data={"test":aa})
                    return redirect('view_live')
                    # list = Batch_Db.objects.all().order_by('-id')
                else:
                    messages.success(request, 'Please select image or text field')
            else:
                messages.success(request, 'Please select atleast one "Batch" ')
        # else:
        #
        #     messages.success(request,'Something  went wrong')
        return render(request, 'admin/live-add.html',locals())



class Live_List(LogoutIfNotStaffMixin,TemplateView):
    template_name = 'admin/live-list.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Live_Db.objects.all().order_by('-id')
        return context


class Delete_Live(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Live_Db
    success_message ='Live Deleted Successfully'
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        Live_Notification_Db.objects.filter(notification_id=id).delete()
        messages.error(request,self.success_message)
        return redirect('view_live')


def edit_notification(request):
    return render(request, 'admin/notification-edit.html')
# notifications

#Plans
class Add_Plan(SuccessMessageMixin,LogoutIfNotStaffMixin,CreateView):
    model = Plan_Db
    form_class = Plan_Form
    success_url = reverse_lazy('plan_list')
    success_message =' Plan Added Successfully'
    template_name = 'admin/add-plan.html'




class Plan_List(LogoutIfNotStaffMixin,TemplateView):
    model = Plan_Db
    template_name = 'admin/plan-list.html'
    # #paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.model.objects.all().order_by('-id')
        return context



class Edit_Plans(SuccessMessageMixin,LogoutIfNotStaffMixin,UpdateView):
    model = Plan_Db
    form_class = Plan_Form
    template_name = 'admin/edit-plan.html'
    success_message ='Plan Updated Successfully'
    success_url = reverse_lazy('plan_list')



class Delete_Plan(SuccessMessageMixin,LogoutIfNotStaffMixin,View):
    model = Plan_Db
    success_message ='Plan Deleted Successfully'
    success_url = reverse_lazy('view_blog_trash')
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        self.model.objects.filter(id=id).delete()
        messages.error(request,self.success_message)
        return redirect('plan_list')


# admin Templates end


def serve_protected_document(request, file):
    document = get_object_or_404(Course_Db, image="/course_photo/" + file)

    # Split the elements of the path
    path, file_name = os.path.split(file)

    response = FileResponse(document.file,)
    response["Content-Disposition"] = "attachment; filename=" + file_name

    return response



