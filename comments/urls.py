from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('update-comment/<str:pk>/', views.update_comment, name='update-comment'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
]