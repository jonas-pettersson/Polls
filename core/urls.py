from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.polls_list, name='polls_list'),
    path('detail/<int:pk>', views.poll_detail, name='poll_detail'),
    path('results/<int:pk>', views.poll_result, name='poll_result'),
    path('vote/<int:pk>', views.vote, name='vote'),
]
