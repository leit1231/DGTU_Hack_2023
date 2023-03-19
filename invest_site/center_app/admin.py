from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import *

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'is_admin',)
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", 'first_name', 'last_name', "password1", "password2"),
            },
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class MyUserAdmin(UserAdmin):
    pass



class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    inlines = [AnswerInline]

class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 0
    inlines = [TaskInline]


class CourseSetting(admin.ModelAdmin):
    filter_horizontal = ('users',)
    inlines = [LectureInline]

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Course, CourseSetting)
admin.site.register(Lecture)
admin.site.register(Task)
admin.site.register(Answer)