from django.contrib import admin
from django.urls import path
from tips import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upvote/<int:tip_id>/', views.upvote, name='upvote'),
    path('downvote/<int:tip_id>/', views.downvote, name='downvote'),
    path('delete/<int:tip_id>/', views.delete_tip, name='delete_tip'),
]
