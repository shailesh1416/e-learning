from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse("dashboard"))
        else:
            return redirect(reverse("dashboard"))


def dashboard(request):
    try:
        if request.user:
            allCourses  = Course.objects.all()
            admissions = Admission.objects.filter(user=request.user)
            courses = []
            for admission in admissions:
                courses.append(Course.objects.get(pk=admission.course.id))

            return render(request, 'dashboard.html', {'myCourses': courses,'allCourses':allCourses})
    except TypeError:
        return redirect('login')


def courseDetails(request, pk):
    try:
        if request.user:
            print(1)
            course = Course.objects.get(pk=pk)
            topics = Video.objects.filter(course=pk)
            # Creating  sidebar
            sidebar = {}
            for top in topics:
                if top.sectionName in sidebar:
                    sidebar[top.sectionName].append(top)
                else:
                    sidebar[top.sectionName] = [top]

            # checking cimpleted topics completed
            completedTopics = []
            for topic in topics:
                complete = VideoViews.objects.filter(
                    video=topic, user=request.user)
                if complete:
                    completedTopics.append(topic.id)

            # calculating next topic
            if len(completedTopics) > 0:
                lastLesson = Video.objects.get(pk=completedTopics[-1]).lessonNo
                nextTopic = Video.objects.filter(
                    lessonNo__gt=lastLesson, course=course).first()
                if nextTopic is None:
                    nextTopic = topics.first()
            else:
                nextTopic = topics.first()
            return render(request, 'courseDetails.html',
                {
                    'isActive' : True if len(topics)>0 else False,
                    'sidebar': sidebar,
                    'course': course,
                    'topics': topics,
                    'completedTopics': completedTopics,
                    'nextTopic': nextTopic,
                    'nextSection': nextTopic.sectionName if len(topics)>0 else False})
    except TypeError:
        print(1)
        return redirect('login')


def topicDetails(request, pk):
    try:
        if request.user:
            topic = Video.objects.get(pk=pk)
            course = Course.objects.get(pk=topic.course.id)
            sections = Section.objects.filter(course=course)
            topics = Video.objects.filter(course=course.id)

            # creating sidebar menu
            sidebar = {}
            for top in topics:
                if top.sectionName in sidebar:
                    sidebar[top.sectionName].append(top)
                else:
                    sidebar[top.sectionName] = [top]

            # checking if topic completed
            completedTopics = []
            for t in topics:
                complete = VideoViews.objects.filter(
                    video=t, user=request.user)
                if complete:
                    completedTopics.append(t.id)

            # calculating current topic to view
            if len(completedTopics) > 0:
                lastLesson = Video.objects.get(pk=completedTopics[-1]).lessonNo
                nextTopic = Video.objects.filter(
                    lessonNo__gt=lastLesson, course=course).first()
                if nextTopic is None:
                    nextTopic = topics.first()
            else:
                nextTopic = topics.first()

            # Geting mcq for this topic
            mcqs = Mcq.objects.filter(topic=topic)
            facultyCheck = mcqs.filter(facultyCheck=True).count()
            if facultyCheck >0:
                dofacultyCheck = True
            else:
                dofacultyCheck = False
            completed = VideoViews.objects.filter(
                video=topic, user=request.user)

            # checking if mcq for this topic is completed
            if completed:
                completed = True
            else:
                completed = False
            return render(request, 'topicDetails.html',
                {
                    'sidebar': sidebar,
                    'course': course,
                    'sections': sections,
                    'topic': topic,
                    'completed': completed,
                    'mcqs': mcqs,
                    'dofacultyCheck':dofacultyCheck,
                    'completedTopics': completedTopics,
                    'nextTopic': nextTopic,
                    'nextSection': nextTopic.sectionName
                }
            )
    except TypeError:
        return redirect('login')


def topicResult(request, pk):
    try:
        if request.user:
            data = request.POST
            # change
            mcqs = Mcq.objects.filter(topic=pk,facultyCheck=False)
            video = Video.objects.get(pk=pk)
            courseId = video.course
            completed = VideoViews.objects.filter(
                video=video, user=request.user)
            score = 0
            if mcqs:
                for mcq in mcqs:
                    if data[str(mcq.id)] == mcq.answer:
                        score += 1
                result = str(round(score/len(mcqs)*100, 1))
            else:
                result = False
            if completed:
                completed = True
            else:
                if score == len(mcqs) or not result:
                    videoView = VideoViews.objects.create(
                        user=request.user, 
                        video=video,
                        # changes
                        faculty = request.user,
                        )
                    videoView.save()
                completed = False

            nextTopic = Video.objects.filter(
                    lessonNo__gt=video.lessonNo, course=video.course).first()
            if nextTopic is None:
                    nextTopic = video
            return render(request, 'topicResult.html', {'result': result, 'score': score, 'total': len(mcqs), 'success': score == len(mcqs), 'course': courseId, 'completed': completed,'nextTopic':nextTopic.id})
    except TypeError:
        return redirect('login')


def facultyCheck(request,pk):
    if request.user:
        password = request.GET.get('password')
        topic = Video.objects.get(pk=pk)
        mcqs = Mcq.objects.filter(topic=topic,facultyCheck=True)
        try:
            faculty = FacultyCheck.objects.get(password = password)
            facultyUser = User.objects.get(pk=faculty.id)
            videoView = VideoViews.objects.create(
                user=request.user, 
                video=topic,
                faculty = facultyUser,
            )
            videoView.save()
        except  FacultyCheck.DoesNotExist:
            return render(request, 'facultyCheck.html',{'message':"Wrong Password"})
        return render(request, 'facultyCheck.html',{'mcqs':mcqs})


def showVideo(request,pk):
    print('hrllo')
    if request.user:
        password = request.GET.get('password')
        videoLink = Video.objects.get(pk=pk).videoLink
        try:
            faculty = FacultyCheck.objects.get(password = password)
        except  FacultyCheck.DoesNotExist:
            return render(request, 'showVideo.html',{'message':"Wrong Password"})
        return render(request, 'showVideo.html',{'videoLink':videoLink})

