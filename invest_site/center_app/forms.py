from django import forms
from .models import *


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date']

    name = forms.CharField(
        label='Название курса',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название курса',
        }),
    )
    description = forms.CharField(
        label='Описание курса',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание курса',
            'rows': 5,
        }),
    )
    start_date = forms.DateField(
        label='Дата начала курса',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
    )
    end_date = forms.DateField(
        label='Дата окончания курса',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
    )


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date']

    name = forms.CharField(
        label='Название курса',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название курса',
        }),
    )
    description = forms.CharField(
        label='Описание курса',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание курса',
            'rows': 5,
        }),
    )
    start_date = forms.DateField(
        label='Дата начала курса',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
    )
    end_date = forms.DateField(
        label='Дата окончания курса',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
    )


class CourseDeleteForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            label='Вы действительно хотите удалить курс?',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
        )


class LectureCreateForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description']

    title = forms.CharField(
        label='Название лекции',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название лекции',
        }),
    )
    description = forms.CharField(
        label='Описание лекции',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание лекции',
            'rows': 5,
        }),
    )


class LectureUpdateForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description']

    title = forms.CharField(
        label='Название лекции',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название лекции',
        }),
    )
    description = forms.CharField(
        label='Описание лекции',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание лекции',
            'rows': 5,
        }),
    )
