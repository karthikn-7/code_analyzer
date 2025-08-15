from django.urls import path
from .views import *

urlpatterns = [
    path("register/",RegisterAPI.as_view(),name="register"),
    # path("register/",name="register"),
    # path("get_all_users/",name="getallusers"),
    
]
