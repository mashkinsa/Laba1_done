from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

#Здесь модели баз данных

#Опросы
class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True,verbose_name="Описание")
    image = models.ImageField(upload_to='survey', blank=True, null=True, default=None, verbose_name="Изображение")  # Поле для изображения
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    life_time = models.PositiveIntegerField(default=300, verbose_name="Время жизни(в сек.)")

    def __str__(self):
        return self.title

    @property #Делает метод доступным как атрибут, тем самым скрывая логику и не меняя класс Question
    def is_active(self):
        return timezone.now() < self.time_update + timedelta(seconds=self.life_time) #Время жизни поста = 5 минут

    class Meta:
        ordering = ['-time_update']
        indexes = [
            models.Index(fields=['-time_update'])
        ]

    def get_absolute_url(self):
        return reverse('survey', kwargs={'survey_slug': self.slug})


#Варианты опроса
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

#Голоса пользователей
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

#Профили пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to='user_avatars', blank=True)

    def __str__(self):
        return f'{self.user} Profile'
