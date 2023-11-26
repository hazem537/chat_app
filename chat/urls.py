from django.urls import path
from .views import index ,signup
from django.contrib.auth import views as auth_views  
urlpatterns = [
    path('', index ,name="index"),
    path('signup/', signup ,name="signup"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    path('login/',auth_views.LoginView.as_view(template_name="chat/login.html"),name="login"),

]
