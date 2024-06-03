from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your models here.

    
class Subject(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50,blank=True, null=True)
    image = models.ImageField(upload_to='profile/', default='sdefault.png')
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def token(self):
        try:
            token = Token.objects.get(user=self.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=self.user)
        return token.key
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Class_name(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Class_name'
        verbose_name_plural = 'Class_names'

class Lesson(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    group = models.ForeignKey(Class_name,on_delete=models.CASCADE)

    is_added = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'




class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50,blank=True, null=True)
    image = models.ImageField(upload_to='profile/', default='sdefault.png')
    group = models.ForeignKey(Class_name,on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def parents(self):
        return Parent.objects.filter(student=self)
    
    @property
    def token(self):
        try:
            token = Token.objects.get(user=self.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=self.user)
        return token.key
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

class Notification(models.Model):
    title = models.CharField(max_length=50,blank=True, null=True)
    text = models.CharField(max_length=50,blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    send_to = models.ManyToManyField(User,related_name='send_to')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

class Mark(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    mark = models.IntegerField("Mark")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.student.user.username} - {self.subject.name} - {self.mark}'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'

class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.student.user.username} - {self.lesson.name} - {self.status}'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

class Parent(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'