from django.db import models
from django.contrib.auth.models import User
from time import timezone
from ckeditor.fields import RichTextField
# Create your models here.

# Model for Course

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    courseImage = models.ImageField(upload_to='courses/', blank=True)

    def __str__(self):
        return str(self.name)

class Section(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sectionNo = models.FloatField()
    inOrder = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

# Model for Videos


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sectionName = models.ForeignKey(
        Section, on_delete=models.CASCADE, null=True)
    lessonNo = models.FloatField()
    title = models.CharField(max_length=200)
    description2 = RichTextField(blank=True,verbose_name='Student Instructions')
    videoLink = models.CharField(max_length=500, blank=True)
    hideVideo = models.BooleanField(default=False)
    description = RichTextField(blank=True)
    facultyInstructions = RichTextField(blank=True,verbose_name='Faculty Instructions')
    # newline
    facultyCheck = models.BooleanField(default=False)
    topicImage = models.ImageField(upload_to='topics/', blank=True)

    def __str__(self):
        return self.title

# Model for View on topics


class VideoViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # changes
    faculty = models.ForeignKey(User,on_delete=models.CASCADE,related_name='checked_by', blank=True, default=1)
    timeOfView = models.DateTimeField(auto_now_add=True)


# Model for Mcq with option and correct answer
class Mcq(models.Model):
    topic = models.ForeignKey(Video, on_delete=models.CASCADE)
    question = RichTextField(blank=False)
    facultyCheck = models.BooleanField(default=False)
    questionImage = models.ImageField(upload_to='mcqImages/', blank=True)
    hint = models.CharField(max_length=200, blank=True)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200, blank=True)
    option4 = models.CharField(max_length=200, blank=True)
    answer = models.CharField(max_length=200)

class FacultyCheck(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.faculty)

class Admission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    admissionDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + "("+str(self.course)+")"


class Attendence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inTime = models.DateTimeField(default=None)
    outTime = models.DateTimeField(default=None)
    
