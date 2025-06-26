from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, profile

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
] 