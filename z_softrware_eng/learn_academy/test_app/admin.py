from django.contrib import admin
from .models import Course, TeamMember, Testimonial , categories

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
