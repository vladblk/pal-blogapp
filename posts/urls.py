from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
  path('', views.index, name='index'),
  path('post/<str:pk>/', views.post, name='post'),
  path('create-post/', views.create_post, name='create-post'),
  path('update-post/<str:pk>/', views.update_post, name='update-post'),
  path('delete-post/<str:pk>/', views.delete_post, name='delete-post'),
]