from .models import Question, Choice
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


#Форма регистрации
class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'password1', 'password1')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }


#Форма редактирования
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

    avatar = forms.ImageField(label="Аватар", required=False)


#Форма авторизация
class LoginForm(AuthenticationForm):
    pass


#Форма удаления аккаунта
class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Удалить аккаунт', required=True)


#Форма добавления опроса
class AddSurveyForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'image', 'slug', 'life_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


#Форма добавления варианта ответа
class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
