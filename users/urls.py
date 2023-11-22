from django.urls import path
from .views import register,signin,signout


urlpatterns=[
    path('login/',signin,name='signin'),
    path('register/',register,name='register'),
    path('signout/',signout,name='signout')
]