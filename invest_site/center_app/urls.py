from django.urls import path

from .views import *


urlpatterns = [
    path('api/chat/<room_name>/', ChatView.as_view()),
    path('', home_page, name='home'),
    path('create_course/', create_course, name='create'),
    path('courses/', all_course, name='courses'),
    path('courses/edit_course_<int:course_id>/', edit_course, name='edit_course'),
    path('courses/edit_course_<int:course_id>/edit_lec_<int:lecture_number>', edit_lecture, name='edit_lecture'),
    path('courses/edit_course_<int:course_id>/edit_lec_<int:lecture_number>/task_<int:task_id>_<int:id_ans>', edit_task, name='edit_task'),
    path('my_course/', my_course_view, name='my_course'),
    path('my_course/<int:course_id>', course_info, name='course'),
    path('my_course/<int:course_id>/lecture_<int:lecture_number>', lecture_info, name='lecture'),
    path('login/', login_view, name='login'),
    path('register/', signup, name='register'),
    # path('test/<int:course_id>_<int:lecture_id>', test, name='test')
]
