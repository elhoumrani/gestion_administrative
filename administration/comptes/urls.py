from django.urls import path, include


from comptes import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),
    path('register/', views.register, name='registerUser'),
    
    ]