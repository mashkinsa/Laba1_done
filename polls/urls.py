from django.conf.urls.static import static
from django.urls import path

from sitesurvey import settings
from .views import index, survey, login_view, register, add_survey, results, logout_view, profile, edit_profile, delete_profile

urlpatterns = [
    path('', index, name='index'),
    path('survey/<slug:survey_slug>/', survey, name='survey'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('add_survey/', add_survey, name='add_survey'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile//', delete_profile, name='delete_profile'),
    path('survey/<slug:survey_slug>/results/', results, name='results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
