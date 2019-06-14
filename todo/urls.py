from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('dashboard/', RedirectView.as_view(url='/dashboard/filters/today')),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/projects/', views.projects, name='projects'),
    path('dashboard/project/<int:id>/', views.project, name='project'),
    path('dashboard/tasks/', views.tasks, name='tasks'),
    path('dashboard/archive/', views.archive, name='archive'),
    path('dashboard/filters/', RedirectView.as_view(url='/dashboard/filters/today')),
    path('dashboard/filters/<str:filter>/', views.filters, name='filters'),
    path('', RedirectView.as_view(url='/dashboard/filters/today')),
]
