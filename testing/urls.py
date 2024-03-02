from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("questions/", views.questions_list, name="questions"),
    path("one_quest/", views.one_quest, name="one_quest"),
    path("one_quest/<int:question_id>/", views.one_quest_id, name="one_quest_id"),
    path("one_quest/<int:question_id>/result/", views.result, name="result"),
    path("questions/test_result", views.test_result, name="test_result"),
    path('', include('users.urls')),
]
