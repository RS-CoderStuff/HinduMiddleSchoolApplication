import os
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.encoding import smart_str
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  USER_TYPE_CHOICES = (
      (0, 'guest'),
      (1, 'teacher'),
      (2, 'student'),
      (3, 'paid'),
  )
  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=0)



# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user


class Main_Course_Category_Db(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='category_image')
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Main_Course_Category_Db'
    def __str__(self):
        return self.title




class User_Profile(models.Model):
    user_id = models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    main_course_category_id = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    exp_date =models.DateField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table =  "User_Profile"





class Super_Course_Category_Db(models.Model):
    main_course_category_id = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Super_Course_Category_Db'
    def __str__(self):
        return self.title

class Sub_Course_Category_Db(models.Model):
    main_course_category_id = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    super_course_category_id = models.ForeignKey(Super_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=10000)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Sub_Course_Category_Db'
    def __str__(self):
        return  self.sub_title
    def save(self, *args, **kwargs):
        self.sub_title = self.main_course_category_id.title + ' -> ' + self.super_course_category_id.title + ' -> ' + self.title
        super(Sub_Course_Category_Db, self).save(*args, **kwargs)


class Course_Content_Db(models.Model):
    # main_course_category_id = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    # super_course_category_id = models.ForeignKey(Super_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    sub_course_category_id = models.ManyToManyField(Sub_Course_Category_Db,related_name='sub_course_category_id',null=True,blank=True)
    title = models.CharField(max_length=100,)
    image = models.ImageField(upload_to='course_content')
    pdf = models.FileField(upload_to='course_content')
    details =RichTextField()
    trash = models.BooleanField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    video2 = models.FileField(upload_to='course_content',default="")
    type = models.CharField(max_length=10,default='0')
    students = models.ManyToManyField(User,related_name='students',null=True,blank=True)
    class Meta:
        db_table = 'Course_Content_Db'
    def extension(self):
        name, extension = os.path.splitext(self.video2.name)
        if smart_str(extension) == '.mp4':
            return True
        else:
            return False


class Images_data(models.Model):
    course_id = models.ForeignKey(Course_Content_Db,null=True, blank=True,on_delete=models.CASCADE)
    image = models.FileField(upload_to='course_photo')



class Course_Db(models.Model):
    name = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    price = models.CharField(max_length=100,)
    image = models.FileField(upload_to='course_photo')
    meta_title = models.CharField(max_length=100,)
    meta_description = models.CharField(max_length=1000,)
    meta_keywords = models.CharField(max_length=1000)
    details = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Course_Db'


class Batch_Db(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_time = models.CharField(max_length=1000)
    end_time = models.CharField(max_length=1000)
    students = models.ManyToManyField(User,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Batch_Db'
    def __str__(self):
        return self.name




class Blog_Category_Db(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Blog_Category_Db'
    def __str__(self):
        return self.title



class Blog_Db(models.Model):
    Blog_Category_id = models.ForeignKey(Blog_Category_Db ,null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,)
    image = models.FileField(upload_to='blog_photo')
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User ,null=True, blank=True,on_delete=models.CASCADE)
    trash = models.BooleanField(default=1)
    meta_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=1000)
    meta_keywords = models.CharField(max_length=500)
    details = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Blog_Db'
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog_Db, self).save(*args, **kwargs)


class Faq_Db(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    keywords = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Faq_Db'


class Testimonial_Db(models.Model):
    client_name = models.CharField(max_length=100)
    client_photo = models.FileField(upload_to='client_photo')
    review = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Testimonial_Db'




class Gallery_Db(models.Model):
    gallery_photo = models.FileField(upload_to='gallery_photo')
    alternate_text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Gallery_Db'





class Notification_Db(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='notification')
    details = models.CharField(max_length=1000)
    batch = models.ManyToManyField(Batch_Db,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Notification_Db'
    def __str__(self):
        return self.title


class Student_Notification_Db(models.Model):
    notification_id = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='notification')
    details = models.CharField(max_length=1000)
    batch = models.ManyToManyField(Batch_Db, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Student_Notification_Db'
    def __str__(self):
        return self.title


class Live_Db(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='notification')
    details = models.CharField(max_length=1000)
    live_date = models.CharField(max_length=1000)
    batch = models.ManyToManyField(Batch_Db,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Live_Db'
    def __str__(self):
        return self.title


class Live_Notification_Db(models.Model):
    notification_id = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='notification')
    details = models.CharField(max_length=1000)
    live_date = models.CharField(max_length=1000)
    batch = models.ManyToManyField(Batch_Db, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Live_Notification_Db'
    def __str__(self):
        return self.title



class Contact_Us(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(max_length=1000)
    find = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Contact_Us'



class Plan_Db(models.Model):
    name = models.CharField(max_length=100)
    main_course_category_id = models.ForeignKey(Main_Course_Category_Db,null=True, blank=True,on_delete=models.CASCADE)
    price = models.IntegerField()
    days = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Plan_Db'
    def __str__(self):
        return self.name




