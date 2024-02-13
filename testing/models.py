from django.db import models


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=32)
    reg_date = models.DateField(auto_now_add=True)  # date of user registration
    avg_result = models.FloatField()  # average result of all tests
    rating = models.FloatField()  # user rating based of test results and timing

    def __str__(self):
        return f"{self.username}"


# electrical safety qualification groups for grouping questions by complexity
class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


# table to save every test results for all users
class Testing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateField(auto_now_add=True)
    result = models.FloatField()  # result of testing in percents
    test_time = models.DurationField()  # time to solve the test
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"user: {self.user}, date: {self.test_date}, result: {self.result}"


class Question(models.Model):
    q_text = models.CharField(max_length=512)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    reference = models.CharField(max_length=32, default=None)  # reference to a regulatory act

    def __str__(self):
        return f"{self.q_text}"


# variants for all questions
class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    var_text = models.CharField(max_length=256)
    is_right = models.BooleanField()  # right / wrong variant

    def __str__(self):
        return f"{self.var_text}"
