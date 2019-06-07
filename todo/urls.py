from django.urls import path
from django.conf.urls import url
from . import views
# from django.urls import register_converter


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('', views.entry, name='entry'),
]
