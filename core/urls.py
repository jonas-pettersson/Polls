from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='polls_list'),
    path('detail/<int:pk>', views.detail, name='poll_detail'),
    path('results/<int:pk>', views.results, name='poll_result'),
    path('vote/<int:pk>', views.vote, name='vote'),
]
