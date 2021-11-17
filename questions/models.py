import uuid
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase, TagBase, Tag
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

# Create your models here.
from unidecode import unidecode


class Tags(Tag):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def slugify(self, tag, i=None):
        slug = slugify(unidecode(tag))
        if i is not None:
            slug += "_%d" % i
        return slug


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    tag = models.ForeignKey(Tags, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="question_author")
    title = models.CharField(max_length=255, default="", null=True)
    text = models.TextField()
    voted = models.ManyToManyField(get_user_model(), default=None, blank=True, related_name="voted_question")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=UUIDTaggedItem)

    class Meta:
        ordering = ["-created_at"]

    #
    # def was_updated_recently(self):
    #     return timezone.now() - self.updated_at

    def __str__(self):
        return str(self.title)

    @property
    def num_votes(self):
        return self.voted.all().count()

    def get_absolute_url(self):
        return reverse('questions:question_detail', args=[str(self.id)])


class Answer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer',
    )
    answer_text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="answer_author")
    voted = models.ManyToManyField(get_user_model(), default=None, blank=True, related_name="voted_answer")
    created_at = models.DateTimeField(auto_now_add=True)
    right_flag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.answer_text)

    @property
    def num_votes(self):
        return self.voted.all().count()

    class Meta:
        ordering = ["-created_at"]


VOTE_CHOICES = (
    ('Poll', 'Poll'),
    ('Unpoll', 'Unpoll')
)


class VoteQuestion(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
    polled = models.CharField(choices=VOTE_CHOICES, default='poll', max_length=10)

    class Meta:
        ordering = ["-vote_date"]

    def was_votes_recently(self):
        return timezone.now() - self.vote_date

    def __str__(self):
        return str(self.question)


class VoteAnswer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
    polled = models.CharField(choices=VOTE_CHOICES, default='poll', max_length=10)

    class Meta:
        ordering = ["-vote_date"]

    def __str__(self):
        return str(self.answer)
