from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from .models import Attendence
from django.contrib.auth.models import User
from django.utils import timezone

# @receiver(user_logged_in)
def post_login(sender,user,request,**kwargs):
    print("Logged in")
    currTime = timezone.now()
    attendence = Attendence(user=request.user,inTime=currTime,outTime=currTime)
    attendence.save()

user_logged_in.connect(post_login)



# @receiver(user_logged_out)
def post_logout(sender,user,request,**kwargs):
    print("Logged out")
    attendence = Attendence.objects.filter(user=request.user).order_by('inTime').first()
    attendence.outTime = timezone.now()
    attendence.save()

user_logged_out.connect(post_logout)
