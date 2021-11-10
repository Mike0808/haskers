from django.urls import path
from . import views
from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, \
    tagged, question_vote, answer_vote, answer, AnswerUpdateView, AnswerDeleteView, SearchResultsListView, answer_right

app_name = "questions"

urlpatterns = [
    path(r'', QuestionListView.as_view(), name='question_list'),
    path('create_question/', QuestionCreateView.as_view(), name="create_question"),
    path('question_detail/<uuid:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question_update/<uuid:pk>/', QuestionUpdateView.as_view(), name="question_update"),
    path('question_delete/<uuid:pk>/', QuestionDeleteView.as_view(), name="question_delete"),
    path('create_answer/', answer, name='create_answer'),
    path('question_tag/<slug:slug>/', tagged, name="tagged"),
    path('question_vote/', question_vote, name="question_vote"),
    path('answer_vote/', answer_vote, name="answer_vote"),
    path('answer_right/', answer_right, name="answer_right"),
    path('answer_update/<uuid:pk>/', AnswerUpdateView.as_view(), name="answer_update"),
    path('answer_delete/<uuid:pk>/', AnswerDeleteView.as_view(), name="answer_delete"),


]
