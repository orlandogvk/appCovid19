from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('date/',views.dateForm,name='by_date'),
    path('country/',views.countryCovid,name='country'),
    path('country-date/',views.countryDate,name='country_date'),
    path('', views.home, name='home'),
]

