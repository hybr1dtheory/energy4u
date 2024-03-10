from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("questions/", views.questions_list, name="questions"),
    path("one_quest/", views.one_quest, name="one_quest"),
    path("one_quest/<int:question_id>/", views.one_quest_id, name="one_quest_id"),
    path("one_quest/<int:question_id>/result/", views.result, name="result"),
    path("questions/test_result", views.test_result, name="test_result"),
    path("exam/", views.exam_categories, name="exam"),
    path("exam/<int:category_id>", views.exam, name="exam_start"),
    path("exam/result", views.exam_result, name="exam_result")
]
