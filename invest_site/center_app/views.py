from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from rest_framework import generics

from .forms import *
from .models import Course, Lecture, Task
from .serializers import ChatSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    form = LoginForm()
    return render(request, 'center_app/login/index.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'center_app/register/index.html', {'form': form})

class ChatView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        message = serializer.validated_data['message']
        room_name = self.kwargs['room_name']

        # Send message to room group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

def home_page(request):
    return render(request, 'center_app/home_page1/index.html')


@login_required(login_url='login')
def create_course(request):
    if request.method == 'POST':
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            # course.users = request.user
            course.save()
            return redirect(reverse('edit_course', args=[course.id]))
    else:
        form = CourseCreateForm()
    return render(request, 'center_app/create_course/index.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = CourseEditForm(instance=course)
    lecture_form = LectureCreateForm()
    if request.method == 'POST':

        if 'course_form' in request.POST:
            form = CourseEditForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('edit_course', course_id=course.id)
        if 'lecture_form' in request.POST:
            lecture_form = LectureCreateForm(request.POST, request.FILES)
            print(lecture_form.errors)
            if lecture_form.is_valid():
                lecture = lecture_form.save(commit=False)
                lecture.course = course
                lecture.save()
                return redirect('edit_course', course_id=course.id)

    context = {
        'course': course,
        'form': form,
        'lectures': Lecture.objects.filter(course_id=course),
        'lecture_form': lecture_form,
    }
    return render(request, 'center_app/edit_course/index.html', context)


def edit_lecture(request, course_id, lecture_number):
    course = get_object_or_404(Course, pk=course_id)
    lecture = get_object_or_404(Lecture, course=course, number=lecture_number)
    tasks = Task.objects.filter(lecture=lecture)

    form = LectureEditForm(instance=lecture)
    task_form = TaskForm()
    answer_form = AnswerForm()

    if request.method == 'POST':
        if 'edit_lecture' in request.POST:
            form = LectureEditForm(request.POST, instance=lecture)
            if form.is_valid():
                form.save()
                return redirect('edit_lecture', course_id=course_id, lecture_number=lecture_number)

        if 'create_task' in request.POST:
            task_form = TaskForm(request.POST)
            answer_form = AnswerForm(request.POST)
            if task_form.is_valid() and answer_form.is_valid():
                # Обе формы валидны, выполняем запрос
                task = task_form.save(commit=False)
                task.lecture = lecture
                task.save()

                answer = answer_form.save(commit=False)
                answer.task = task
                answer.save()

                tasks = Task.objects.filter(lecture=lecture)
                form = TaskForm(instance=task)
                answer_form = AnswerForm()
                return render(request, 'center_app/edit_lecture/index.html',
                              {'form': form, 'tasks': tasks, 'course': course,
                               'lecture': lecture, 'answer_form': answer_form,
                               'task': task,})
            else:
                # Одна из форм не валидна, выводим ошибки
                form = TaskForm()
                return render(request, 'center_app/edit_lecture/index.html',
                              {'form': form, 'answer_form': answer_form,
                               'course': course, 'lecture': lecture, 'task_form': task_form,})

        elif 'edit_task' in request.POST:
            task_id = int(request.POST.get('task_id'))
            task = get_object_or_404(Task, lecture=lecture, pk=task_id)
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('edit_lecture', course_id=course_id, lecture_number=lecture_number)

    return render(request, 'center_app/edit_lecture/index.html', {'form': form, 'course': course, 'lecture': lecture,
                                                                  'tasks': tasks, 'task_form': task_form,
                                                                  'answer_form': answer_form})

def edit_task(request, course_id, lecture_number, task_id, id_ans):
    course = get_object_or_404(Course, pk=course_id)
    lecture = get_object_or_404(Lecture, course=course, number=lecture_number)
    task = get_object_or_404(Task, lecture=lecture, pk=task_id)
    answer = get_object_or_404(Answer, task_id=task_id, pk=id_ans)
    form = TaskForm(instance=task)
    answer_form = AnswerForm()
    if 'edit_task' in request.POST:
        # task_id = request.POST.get('task_id')
        # task = Task.objects.get(id=task_id)
        task_form = TaskForm(request.POST, instance=task)
        answer_form = AnswerForm(request.POST, instance=answer)
        if task_form.is_valid() and answer_form.is_valid():
            # Обе формы валидны, выполняем запрос
            task = task_form.save(commit=False)
            task.lecture = lecture
            task.save()

            answer = answer_form.save(commit=False)
            answer.task = task
            answer.save()

            tasks = Task.objects.filter(lecture=lecture)
            form = TaskForm(instance=task)
            answer_form = AnswerForm()
            return render(request, 'center_app/edit_task/index.html',
                          {'form': form, 'tasks': tasks, 'course': course,
                           'lecture': lecture, 'answer_form': answer_form,
                           'task': task})
        else:
            # Одна из форм не валидна, выводим ошибки
            form = TaskForm()
            return render(request, 'center_app/edit_task/index.html',
                          {'form': form, 'answer_form': answer_form,
                           'course': course, 'lecture': lecture, 'task_form': task_form})

    return render(request,'center_app/edit_task/index.html', {
        'course': course, 'lecture': lecture, 'task': task, 'answer': answer,
        'form': form, 'answer_form': answer_form,
    })


def all_course(request):
    all_courses = Course.objects.all()
    context = {
        "all_courses": all_courses,
    }
    return render(request, 'center_app/all_course/index.html', context=context)


def my_course_view(request):
    course = Course.objects.filter(users=request.user)
    return render(request, 'center_app/my_course/index.html', {
        'course': course,
    })

def course_info(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lecture = Lecture.objects.filter(course=course)
    return render(request, 'center_app/course_info_user/index.html', {
        'course': course, 'lecture': lecture,
    })

def lecture_info(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lecture = get_object_or_404(Lecture, course=course)
    return render(request, 'center_app/lecture_info/index.html', {
        'course': course, 'lecture': lecture,
    })

# def test_submit(request, course_id, lecture_id):
#     course = get_object_or_404(Course, id=course_id)
#     lecture = get_object_or_404(Lecture, id=lecture_id, course=course)
#
#     if request.method == 'POST':
#         for task_with_answers in tasks_with_answers:
#             selected_answer_id = int(request.POST['task{}'.format(task_with_answers.task.id)])
#             selected_answer = Answer.objects.get(id=selected_answer_id)
#             if selected_answer.is_correct:
#                 # сохранить результат правильного ответа для текущего пользователя
#             else:
#                 # сохранить результат неправильного ответа для текущего пользователя
#
#         # перенаправить на страницу результатов теста
#         return redirect('test-result', course_id=course.id, lecture_id=lecture.id)
#
#     context = {'course': course, 'lecture': lecture, 'tasks_with_answers': tasks_with_answers}
#     return render(request, 'center_app/test/submit.html', context)
#
# def test_result(request, course_id, lecture_id):
#     course = get_object_or_404(Course, id=course_id)
#     lecture = get_object_or_404(Lecture, id=lecture_id, course=course)
#
#     user_answers = Answer.objects.filter(user=request.user, task__lecture=lecture)
#     score = sum([answer.is_correct for answer in user_answers])
#
#     context = {'course': course, 'lecture': lecture, 'score': score}
#     return render(request, 'center_app/test/result.html', context)