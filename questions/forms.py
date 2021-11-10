from django import forms

from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = [
          'title', 'text', 'tags',
        ]


class AnswerForm(forms.ModelForm):
    right_flag = forms.BooleanField(required=False)

    class Meta:
        model = models.Answer
        fields = [
            'right_flag'
        ]


