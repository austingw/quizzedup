from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('answer/', views.answer, name='answer'),
    path('new_question/', views.new_question, name='new_question'),
    path('login/', views.custom_login, name='custom_login'),
    path('signup/', views.custom_signup, name='custom_signup'), 
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('history/', views.user_question_history, name='user_question_history')
]