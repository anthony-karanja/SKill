from django.urls import path
from . import views

urlpatterns = [
    path('skill/', views.SkillLogin.as_view(), name="skill"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('', views.HomeTopic.as_view(), name="home"),
    path('room/<str:pk>/', views.HomeRoom.as_view(), name="room"),
    # path('profile/<str:pk>/', views.userProfile.as_view(), name="user-profile"),
    path('update-room/<str:pk>/', views.MessageRetrieveUpdateDestroy.as_view(), name="update-room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]