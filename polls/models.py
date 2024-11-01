from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок: ")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL: ")
    description = models.TextField(blank=True,verbose_name="Описание: ")
    image = models.ImageField(upload_to='survey', blank=True, null=True, default=None, verbose_name="Изображение")  # Поле для изображения
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_update']
        indexes = [
            models.Index(fields=['-time_update'])
        ]

    def get_absolute_url(self):
        return reverse('survey', kwargs={'survey_slug': self.slug})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to='user_avatars', blank=True)

    def __str__(self):
        return f'{self.user} Profile'
