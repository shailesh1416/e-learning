from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.db import connection

from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.

def home(request):
    if request.method == "GET":
        return render(
            request, "registration/landingpage.html"
        )



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
            # getting course details
            allCourses  = Course.objects.all()

            # getting admission details of user
            admissions = Admission.objects.filter(user=request.user)
            courses = []
            for admission in admissions:
                courses.append(Course.objects.get(pk=admission.course.id))
            
            # getting user statistics
            # raw queries
            sql = f'SELECT count(*),date(videos_videoviews.timeOfView) FROM elearning.videos_videoviews where user_id=3  group by date(videos_videoviews.timeOfView);'
            submits = VideoViews.objects.filter(user=request.user)
            cursor = connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchall()
            daywiseSubmits = []
            dates = []
            for i in row:
                daywiseSubmits.append(i[0])
                dates.append(i[1].strftime('%d-%m-%y'))
            
            sql2 = f'''SELECT 
                        round((COUNT(v.course_id)/(select count(*) from videos_video where course_id=v.course_id)*100),1), v.course_id, c.name
                    FROM
                        elearning.videos_videoviews AS vv
                            JOIN
                        elearning.videos_video AS v ON vv.video_id = v.id
                            JOIN
                        elearning.videos_course AS c ON v.course_id = c.id
                    WHERE
                        vv.user_id = {request.user.id}
                    GROUP BY v.course_id
                    '''
            cursor.execute(sql2)
            courseCompleted = cursor.fetchall()                        
            return render(request, 'dashboard.html', 
            {
                'myCourses': courses,
                'allCourses':allCourses,
                'daywiseSubmits':daywiseSubmits,
                'dates':dates,
                'submits':submits[::-1],
                'courseCompleted':courseCompleted
            })

    except TypeError:
        return redirect('login')


def courseDetails(request, pk):
    try:
        if request.user:
            course = Course.objects.get(pk=pk)
            topics = Video.objects.filter(course=pk).order_by('lessonNo')
            topicsCount = len(topics)
            # Creating  sidebar
            sidebar = {}
            for top in topics:
                if top.sectionName in sidebar:
                    sidebar[top.sectionName].append(top)
                else:
                    sidebar[top.sectionName] = [top]

            # checking cimpleted topics completed
            submits = []
            completedTopics = []
            for topic in topics:
                complete = VideoViews.objects.filter(
                    video=topic, user=request.user)
                if complete:
                    submits.append([complete[0].video,complete[0].faculty,complete[0].timeOfView])
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
                    'submits':submits[::-1],
                    'completedTopics': completedTopics,
                    'nextTopic': nextTopic,
                    'percentCompleted' : round((len(completedTopics)+((1 if len(completedTopics)>0 else 0)))/topicsCount*100,1),
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
            # ordering video accouding to llesson no
            topics = Video.objects.filter(course=course.id).order_by('lessonNo')

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
            mcqs = Mcq.objects.filter(topic=pk)
            video = Video.objects.get(pk=pk)
            courseId = video.course
            completed = VideoViews.objects.filter(
                video=video, user=request.user)

            # calculating score for mcqs
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
        try:
            faculty = FacultyCheck.objects.get(password = password)
            facultyUser = User.objects.get(pk=faculty.id)
            videoView = VideoViews.objects.create(
                user=request.user, 
                video=topic,
                faculty = facultyUser,
            )
            print(123)
            videoView.save()
        except  FacultyCheck.DoesNotExist:
            return render(request, 'facultyCheck.html',{'success':False})
        # return render(request, 'facultyCheck.html',{'mcqs':mcqs})
        return render(request, 'facultyCheck.html', {'success':True})


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

