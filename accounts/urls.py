from django.urls import path
from .views import SettingsPageView
from accounts import views as user_views

urlpatterns = [
    path('settings/', SettingsPageView.as_view(), name='settings')
]
