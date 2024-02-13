from django.contrib import admin
from .models import User, Testing, Category, Question, Variant


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avg_result', 'rating', 'reg_date')
    list_filter = ('avg_result', 'rating', 'reg_date')


@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_date', 'result', 'test_time', 'category')
    list_filter = ('user', 'test_date', 'category')


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
