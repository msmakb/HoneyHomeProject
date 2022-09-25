from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Index'),
    path('Erorr', views.unauthorized, name='Unauthorized'),
    path('Dashboard', views.dashboard, name='Dashboard'),
    path('about', views.about, name='About'),
    path('logout', views.logoutUser, name='Logout'),
    path('Tasks', views.tasks, name='Tasks')
]
