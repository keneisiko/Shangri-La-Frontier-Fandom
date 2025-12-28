from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fandom/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Профили
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    
    # Посты
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:pk>/like/', views.post_like, name='post_like'),
    
    # Обсуждения
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:pk>/edit/', views.discussion_edit, name='discussion_edit'),
    path('discussions/<int:pk>/delete/', views.discussion_delete, name='discussion_delete'),
    
    # Фанфики
    path('fanfics/', views.fanfic_list, name='fanfic_list'),
    path('fanfics/create/', views.fanfic_create, name='fanfic_create'),
    path('fanfics/<int:pk>/', views.fanfic_detail, name='fanfic_detail'),
    path('fanfics/<int:pk>/edit/', views.fanfic_edit, name='fanfic_edit'),
    path('fanfics/<int:pk>/delete/', views.fanfic_delete, name='fanfic_delete'),
    path('fanfics/<int:pk>/like/', views.fanfic_like, name='fanfic_like'),
]

