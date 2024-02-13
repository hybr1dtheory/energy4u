from django import forms
from django.core.exceptions import ValidationError
from .models import Question


class QuestionForm(forms.Form):
    question = forms.MultipleChoiceField()

    def clean_question(self):
        data = self.cleaned_data['question']
        if not any(data):
            raise ValidationError("Необхідно вибрати хоча б один варіант.")
        return data
