from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=True, label='Фамилия')
    email = forms.EmailField(max_length=255, required=True, label='Почта')

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image']

class LectureCreateForm(forms.ModelForm):
    file = forms.FileField(required=True, label='Файл')
    class Meta:
        model = Lecture
        fields = ['number', 'title', 'text', 'file']

class LectureEditForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['number', 'title', 'text', 'file']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer1', 'answer2', 'answer3', 'true_answer']
class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'users', 'activated',]




# class CourseUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['name', 'description', 'start_date', 'end_date']
#
#     name = forms.CharField(
#         label='Название курса',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите название курса',
#         }),
#     )
#     description = forms.CharField(
#         label='Описание курса',
#         max_length=500,
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите описание курса',
#             'rows': 5,
#         }),
#     )
#     start_date = forms.DateField(
#         label='Дата начала курса',
#         widget=forms.DateInput(attrs={
#             'class': 'form-control',
#             'type': 'date',
#         }),
#     )
#     end_date = forms.DateField(
#         label='Дата окончания курса',
#         widget=forms.DateInput(attrs={
#             'class': 'form-control',
#             'type': 'date',
#         }),
#     )
#
#
# class CourseDeleteForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'] = forms.CharField(
#             label='Вы действительно хотите удалить курс?',
#             widget=forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'readonly': True,
#             }),
#         )
#
#
# class LectureCreateForm(forms.ModelForm):
#     class Meta:
#         model = Lecture
#         fields = ['title', 'description']
#
#     title = forms.CharField(
#         label='Название лекции',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите название лекции',
#         }),
#     )
#     description = forms.CharField(
#         label='Описание лекции',
#         max_length=500,
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите описание лекции',
#             'rows': 5,
#         }),
#     )
#
#
# class LectureUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Lecture
#         fields = ['title', 'description']
#
#     title = forms.CharField(
#         label='Название лекции',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите название лекции',
#         }),
#     )
#     description = forms.CharField(
#         label='Описание лекции',
#         max_length=500,
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Введите описание лекции',
#             'rows': 5,
#         }),
#     )