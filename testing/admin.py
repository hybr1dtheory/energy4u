from django.contrib import admin
from .models import Testing, Category, Question, Variant, TestingQuestion


@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_datetime', 'result', 'test_duration', 'category')
    list_filter = ('user', 'test_datetime', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'q_text', 'category', 'reference')
    list_filter = ('category',)


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'var_text', 'is_right')


@admin.register(TestingQuestion)
class TestingQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'testing_id', 'question', 'variant')
    list_filter = ('testing_id',)
