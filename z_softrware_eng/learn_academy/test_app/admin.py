from django.contrib import admin
from .models import Course, TeamMember, Testimonial , categories , lecturer , message

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'duration')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'bio')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'date')

@admin.register(categories)
class categoriesAdmin(admin.ModelAdmin):
    list_display = ('title' , 'number' ,'picture')


@admin.register(lecturer)
class lecturerAdmin(admin.ModelAdmin):
    list_display = ('name' ,'category' ,'picture')


@admin.register(message)
class messageAdmin(admin.ModelAdmin):
    list_display = ('name' ,'level' , 'message' ,'picture')
