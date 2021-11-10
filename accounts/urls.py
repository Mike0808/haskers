from django.urls import path
# from .views import SignupPageView, SettingsPageView
from accounts import views as user_views
# urlpatterns = [
#     path('signup/', SignupPageView.as_view(), name='signup'),
#     path('settings/', SettingsPageView.as_view(), name='settings'),
# ]
urlpatterns = [
    path('signup/', user_views.register, name='signup'),
    path('settings/', user_views.settings, name='settings'),
]