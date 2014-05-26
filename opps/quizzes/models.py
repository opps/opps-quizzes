# coding: utf-8

from django.db import models
from django.db.models import Q, F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.containers.models import Container
from opps.core.managers import PublishableManager

from .forms import BaseQuizForm


class QuizManager(PublishableManager):

    def all_opened(self):
        return super(QuizManager, self).get_query_set().filter(
            date_available__lte=timezone.now(),
            published=True
        ).filter(
            Q(date_end__gte=timezone.now()) | Q(date_end__isnull=True)
        )


class BaseQuiz(Container):
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)
    show_results = models.BooleanField(_(u'show results'), default=False)

    @property
    def is_opened(self):
        now = timezone.now()
        self.date_available = self.date_available or now
        if not self.date_end and self.date_available <= now:
            return True
        elif not self.date_end and self.date_available > now:
            return False
        return now >= self.date_available and now <= self.date_end

    @property
    def cookie_name(self):
        return "opps_quiz_{0}".format(self.pk)

    def __unicode__(self):
        return self.title

    def get_form(self, *args, **kwargs):
        kwargs.update({'instance': self})
        return BaseQuizForm(*args, **kwargs)

    def can_vote(self, request):
        if self.cookie_name in request.COOKIES:
            return False
        return True

    def get_choices(self):
        raise NotImplementedError

    def get_result(self):
        raise NotImplementedError

    objects = QuizManager()

    class Meta:
        abstract = True


class ContainerPoll(BaseQuiz):
    def get_choices(self):
        return self.choices.all()

    def get_result(self):
        return [
            (c.container, c.votes) for c in self.choices.order_by('-votes')
        ]

    def vote(self, request, choice):
        if not self.can_vote(request):
            return False
        if not self.pk:
            return False

        return choice.vote()

    class Meta:
        verbose_name = _(u'container poll')
        verbose_name_plural = _(u'containers polls')


class ContainerPollChoice(models.Model):
    container = models.ForeignKey(
        Container,
        verbose_name=_(u'container'),
    )
    containerpoll = models.ForeignKey(
        ContainerPoll,
        verbose_name=_(u'container poll'),
        related_name='choices'
    )
    votes = models.PositiveIntegerField(_(u'votes'), default=0)
    order = models.PositiveIntegerField(_(u'order'), default=0)

    class Meta:
        ordering = ['order', ]
        unique_together = ('container', 'containerpoll')
        verbose_name = _(u'container poll choice')
        verbose_name_plural = _(u'containers polls choices')

    def __unicode__(self):
        return self.container.title

    def vote(self):
        if not self.pk:
            return False

        ContainerPollChoice.objects.filter(pk=self.pk).update(
            votes=F('votes') + 1
        )
        return True


class ContainerDuel(BaseQuiz):
    container1 = models.ForeignKey(
        Container,
        verbose_name=u'container 1',
        related_name='containerduel1'
    )
    container1_votes = models.PositiveIntegerField(
        _(u'container1 votes'),
        default=0
    )
    container2 = models.ForeignKey(
        Container,
        verbose_name=u'container 2',
        related_name='containerduel2'
    )
    container2_votes = models.PositiveIntegerField(
        _(u'container2 votes'),
        default=0
    )

    def get_result(self):
        return [
            (self.container1, self.container1_votes),
            (self.container2, self.container2_votes),
        ]

    def get_choices(self):
        return Container.objects.filter(
            Q(pk=self.container1.pk) | Q(pk=self.container2.pk)
        )

    def vote(self, request, choice):
        if not self.can_vote(request):
            return False

        if not self.pk:
            return False

        if choice.pk == self.container1.pk:
            ContainerDuel.objects.filter(pk=self.pk).update(
                container1_votes=F('container1_votes') + 1
            )
            return True
        elif choice.pk is self.container2.pk:
            ContainerDuel.objects.filter(pk=self.pk).update(
                container2_votes=F('container2_votes') + 1
            )
            return True

        return False

    class Meta:
        verbose_name = _(u'container duel')
        verbose_name_plural = _(u'containers duels')
