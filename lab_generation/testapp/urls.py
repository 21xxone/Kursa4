from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/',views.profile, name='profile',),
    path('', views.home, name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('generalInfo/', views.generalInfo, name='generalInfo'),
    path('chapterInfo/', views.chapterInfo, name='chapterInfo'),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
