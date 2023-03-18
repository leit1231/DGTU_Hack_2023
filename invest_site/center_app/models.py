from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=50,
                                 verbose_name='Фамилия')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    courses = models.ManyToManyField('Course', blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    activated = models.BooleanField(default=True)


class Lecture(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    reading = models.BooleanField(default=False)
    file = models.FileField()


class Task(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    beginen = models.BooleanField(default=True)


class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=255)  # Гении мысли
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    true_answer = models.TextField()  # Отцы рандома