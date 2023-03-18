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


class CourseLectureInline(admin.TabularInline):
    model = Lecture


class CourseSetting(admin.ModelAdmin):
    inlines = [CourseLectureInline, ]


class LectureTaskInline(admin.TabularInline):
    model = Task


class LectureSetting(admin.ModelAdmin):
    inlines = [LectureTaskInline, ]



admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Course, CourseSetting)
admin.site.register(Lecture, LectureSetting)
admin.site.register(Task)
admin.site.register(Answer)
