from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.core.paginator import Paginator
from taggit.models import Tag

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, VoteAnswer, VoteQuestion


class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'question_list'
    queryset = Question.objects.all().\
        annotate(consumption_times=Count('voted')).order_by('-consumption_times', '-created_at')


class QuestionActionMixin:

    form_class = QuestionForm

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)


class QuestionCreateView(LoginRequiredMixin, QuestionActionMixin, CreateView):
    template_name = 'questions/question_form.html'
    common_tags = Question.tags.most_common()[:3]
    models = Question
    success_msg = "Question created!"
    action = "Add"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user
        context['common_tags'] = self.common_tags
        context['question_list'] = Question.objects.all(). \
            annotate(consumption_times=Count('voted')).order_by('-consumption_times', '-created_at')
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        form = AnswerForm
        context = super().get_context_data(**kwargs)
        answers_list = Answer.objects.filter(question_id=self.kwargs.get("pk"))\
            .annotate(consumption_times=Count('voted')).order_by('-consumption_times', '-created_at')
        righ_flag = Answer.objects.filter(question_id=self.kwargs.get("pk"), right_flag=True).count()
        paginator = Paginator(answers_list, 30)
        page = self.request.GET.get('page')
        answers = paginator.get_page(page)
        context['answers'] = answers
        context['question_list'] = Question.objects.all().\
        annotate(consumption_times=Count('voted')).order_by('-consumption_times', '-created_at')
        # context['right_flag_count'] = answers_list['right_flag'].count()
        context['form'] = form
        return context


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'questions/question_form.html'
    action = "Update"
    context_object_name = 'question_update'
    common_tags = Question.tags.most_common()[:3]
    fields = [
        'author',
        'title',
        'text',
        'tags',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_tags'] = self.common_tags
        context['question_list'] = Question.objects.all(). \
            annotate(consumption_times=Count('voted')).order_by('-consumption_times', '-created_at')
        return context


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('questions:question_list')
    action = "Delete"


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    template_name = 'questions/answer_form.html'
    success_url = reverse_lazy('questions:question_list')
    action = "Update"
    context_object_name = 'answer_update'
    fields = [
        'answer_text'
    ]


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy('questions:question_list')
    action = "Delete"


def answer(request):
    user = request.user
    if request.method == "POST":
        answer_text = request.POST.get('answer_text')
        question_id = request.POST.get('question_id')
        questions_list = Question.objects.get(id=question_id)
        _answer, created = Answer.objects.get_or_create(question=questions_list, answer_text=answer_text, author=user)
        _answer.save()
    return redirect('questions:question_list')


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    questions_list = Question.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'questions_list': questions_list,
    }
    return render(request, 'questions/question_list.html', context)


def question_vote(request):
    user = request.user
    if request.method == "POST":
        question_id = request.POST.get('question_id')
        questions_list = Question.objects.get(id=question_id)
        if 'vote' in request.POST.keys():
            questions_list.voted.add(user)
        if 'unvote' in request.POST.keys():
            questions_list.voted.remove(user)
        vote, created = VoteQuestion.objects.get_or_create(user=user, question_id=question_id)
        if not created:
            if vote.polled == 'Poll':
                vote.polled = 'Unpoll'
            else:
                vote.polled = 'Poll'
        vote.save()
    return redirect('questions:question_list')


def answer_vote(request):
    user = request.user
    if request.method == "POST":
        answer_id = request.POST.get('answer_id')
        question_id = request.POST.get('question_id')
        answer_list = Answer.objects.get(id=answer_id)
        if 'answer_vote' in request.POST.keys():
            answer_list.voted.add(user)
        if 'answer_unvote' in request.POST.keys():
            answer_list.voted.remove(user)
        vote, created = VoteAnswer.objects.get_or_create(user=user, answer_id=answer_id)
        if not created:
            if vote.polled == 'Poll':
                vote.polled = 'Unpoll'
            else:
                vote.polled = 'Poll'
        vote.save()
    return redirect('questions:question_detail', question_id)


def answer_right(request):
    if request.method == "POST":
        answer_id = request.POST.get('answer_id')
        question_id = request.POST.get('question_id')
        right_flag = True if request.POST.get('right_flag') == 'on' else False
        answer = Answer.objects.get(id=answer_id)
        answer.right_flag = right_flag
        answer.save()
    return redirect('questions:question_detail', question_id)


class SearchResultsListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'questions/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Question.objects.filter(
            Q(title__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = Answer.objects.all()
        context['answers'] = answers
        return context
