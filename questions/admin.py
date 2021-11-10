from django.contrib import admin
from .models import Question, Answer


# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
    list_display = ("title", "author", "tags",)


admin.site.register(Question, QuestionAdmin)
