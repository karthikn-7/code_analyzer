from django.urls import path
from .views import *

urlpatterns = [
    path("Question/",createQuestion.as_view(),name="questions"),
    path("Result/",ResultAPI.as_view(),name="submitResult"),
]
