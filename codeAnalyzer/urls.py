from django.urls import path
from .views import *

urlpatterns = [
    path("codeReport/",ReportApi.as_view(),name="codeReport"),
    path("Question/",QuestionListCreateAPI.as_view(),name="questions"),
    path("Result/",ResultAPI.as_view(),name="submitResult"),
]
