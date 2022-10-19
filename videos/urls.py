from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('course/<int:pk>', courseDetails, name="courseDetails"),
    path('course/topic/<int:pk>', topicDetails, name="topicDetails"),
    path('course/topic/<int:pk>/check', facultyCheck, name="facultyCheck"),
    path('course/topic/<int:pk>/show_video', showVideo, name="showVideo"),
    path('course/topic/result/<int:pk>', topicResult, name="topicResult"),
    path("login", include("django.contrib.auth.urls"), name="login"),
    path("register/", register, name="register"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# Hello this is a test line