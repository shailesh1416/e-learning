from django.contrib import admin

from .models import *
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'description','inOrder']


admin.site.register(Section, SectionAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_filter = ('course','sectionName')
    search_fields = ['title']
    list_display = ['title', 'lessonNo', 'sectionName', 'course','hideVideo']


admin.site.register(Video, VideoAdmin)


class VideoViewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'faculty', 'timeOfView']
    list_filter = ['user', 'video', 'faculty', 'timeOfView']


admin.site.register(VideoViews, VideoViewsAdmin)

class McqAdmin(admin.ModelAdmin):
    list_filter = ['topic',]
    search_fields = ['question',]
    list_display = ['question', 'answer', 'topic']


admin.site.register(Mcq, McqAdmin)


class AdmissionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Admission, AdmissionAdmin)

class FacultyCheckAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'password']
admin.site.register(FacultyCheck, FacultyCheckAdmin)

# attendence
class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'inTime', 'outTime']


admin.site.register(Attendence, AttendenceAdmin)

