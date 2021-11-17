from datetime import timedelta

from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='answer_filter')
def answer_filter(answers, question_id):
    return answers.filter(question_id=question_id).count()


@register.filter(name='days_until')
def days_until(date):
    delta = timezone.now() - date
    print(delta)
    if delta > timedelta(days=1):
        return 'asked ' + str(delta.days) + ' days ago'
    return 'asked today'
