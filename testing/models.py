from django.db import models
from django.contrib.auth.models import User


# electrical safety qualification groups for grouping questions by complexity
class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


# table to save every test results for all users
class Testing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_datetime = models.DateTimeField(auto_now_add=True)
    result = models.FloatField(default=0.0)  # result of testing in percents
    test_duration = models.DurationField(null=True)  # time to solve the test
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "test_datetime"
        ordering = ["-test_datetime"]

    def __str__(self):
        return f"user: {self.user}, date: {self.test_datetime}, result: {self.result}"


class Question(models.Model):
    q_text = models.CharField(max_length=512)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    reference = models.CharField(max_length=32, default=None)  # reference to a regulatory act

    class Meta:
        ordering = ["?"]

    def __str__(self):
        return f"{self.q_text}"


# variants for all questions
class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    var_order = models.CharField(max_length=1, null=True)  # entire order of variants for every question
    var_text = models.CharField(max_length=256)
    is_right = models.BooleanField()  # right / wrong variant

    def __str__(self):
        return f"{self.var_text}"


class TestingQuestion(models.Model):
    """Model represents table for many-to-many relation between Question and Testing
    with additional data about choice"""
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    testing = models.ForeignKey(Testing, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)  # choice for every question in testing
