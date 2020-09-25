from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('send_mail/', views.send, name='send'),
    path('data_delete/', views.delete, name='delete'),
    path('data_scrap/', views.scrap, name='scrap')
]