from django.urls import path
from app import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    path('', views.home, name=''),
    path('analyzer', views.analyzer, name='analyzer'),
    path('visualization', views.visualization, name='visualization'),
    path('index', views.index, name='index'),
    path('search_vis', views.search_vis, name='search_vis'),
    path('messageautomation', views.messageautomation, name='messageautomation'),
]
