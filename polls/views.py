from audioop import reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddSurveyForm, RegistrationForm, LoginForm, EditProfileForm, DeleteAccountForm
from .models import Question, Choice, UserProfile, Vote

#Здесь представления страниц


#Главная страница с опросами
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            surveys = Question.objects.all()
        else:
            surveys = [q for q in Question.objects.all() if q.is_active]
        return render(request, 'polls/index.html', {'title': 'Опросы', 'surveys': surveys})
    else:
        return redirect('login')


#Выход
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


#Регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, avatar=form.cleaned_data['avatar'])
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})


#Авторизация
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'polls/login.html', {'form': form})


#Редактирование профиля
@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.userprofile  # Получаем связанный UserProfile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():  # Проверяем валидность формы
            form.save() # Сохраняем изменения в форме
            user_profile.save()  # Сохраняем изменения в UserProfile
            if 'avatar' in request.FILES: # Проверяем, загружен ли новый аватар
                user_profile.avatar = request.FILES['avatar'] # Обновляем аватар
                user_profile.save() # Сохраняем изменения в UserProfile
                return redirect('profile')  # Переход после успешного обновления
            return redirect('profile')  # Переход после успешного обновления
    else:
        form = EditProfileForm(instance=user)  # Для GET-запроса
        return render(request, 'polls/edit_profile.html', {'form': form})



#Удаление аккаунта
@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_delete']:
            request.user.delete()
            logout(request)
            return redirect('index')
    else:
        form = DeleteAccountForm()
    return render(request, 'polls/delete_profile.html', {'form': form})

#Опрос
def survey(request, survey_slug):
    survey = get_object_or_404(Question, slug=survey_slug)
    choices = survey.choice_set.all()
    # Проверяем, активен ли опрос
    if not survey.is_active:
        return render(request, 'polls/results.html',
                      {'survey': survey, 'choices': choices, 'message': "Этот опрос больше не доступен."})
    data = {
        'title': survey.title,
        'choices': choices,
        'survey': survey,
    }
    # Проверяем, проголосовал ли пользователь в этом опросе
    if Vote.objects.filter(user=request.user, question=survey).exists():
        return render(request, 'polls/results.html', {
            'survey': survey,
            'choices': choices,
            'message': "Вы уже проголосовали в этом опросе."
        })

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.votes += 1
        choice.save()
        # Сохраняем голос пользователя в базе данных
        Vote.objects.create(user=request.user, question=survey, choice=choice)
        return redirect('results', survey_slug=survey.slug)

    return render(request, 'polls/survey.html', data)

#Результаты
@login_required
def results(request, survey_slug):
    survey = get_object_or_404(Question, slug=survey_slug)
    choices = survey.choice_set.all()
    return render(request, 'polls/results.html', {'survey': survey, 'choices': choices})

#Добавить опрос
@login_required
def add_survey(request):
    if request.method == 'POST':
        form = AddSurveyForm(request.POST, request.FILES)
        choices = request.POST.getlist('choice_text') # Получаем список вариантов ответов
        if form.is_valid() and all([choice.strip() != '' for choice in choices]):
            question = form.save() # Сохраняем вопрос
            for choice_text in choices:
                Choice.objects.create(question=question, choice_text=choice_text) # Создаем вариант ответа
            return redirect('index')
    else:
        form = AddSurveyForm()
    data = {
    'title': 'Создать опрос',
    'form': form,
    }
    return render(request, 'polls/add_survey.html', data)


#Профиль
@login_required
def profile(request):
    user = request.user
    return render(request, 'polls/profile.html', {'user': user})


#Страница не найдена 404
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")


#Голосование
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Проверяем, проголосовал ли пользователь уже, используя сессию
    if request.session.get(f'voted_{question_id}'):
        return HttpResponseForbidden("Вы уже проголосовали в этом опросе.")
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        # Сохраняем информацию о голосе в сессии
        request.session[f'voted_{question_id}'] = True
        choice.votes += 1
        choice.save()
        return redirect('results', question_id=question.id)
    return render(request, 'polls/survey.html', {'question': question})

