from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Erorr', views.unauthorized, name='unauthorized'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('about', views.about, name='about'),
    path('logout', views.logoutUser, name='logout'),
    path('Tasks', views.Tasks, name='Tasks')
]