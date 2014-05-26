from operator import itemgetter

from django import template
from django.utils import timezone
from opps.quizzes.models import ContainerPollChoice, ContainerDuel

register = template.Library()


@register.assignment_tag(takes_context=True)
def can_vote_in_quiz(context, quiz):
    request = context.get('request')
    if not request:
        return False
    return quiz.can_vote(request)


@register.assignment_tag(takes_context=True)
def get_channel_result(context, channel):
    results = {}

    containerpollchoices = ContainerPollChoice.objects.filter(
        containerpoll__published=True,
        containerpoll__date_available__lte=timezone.now(),
        containerpoll__channel_id=channel.pk
    ).only('container', 'votes')

    for container_choice in containerpollchoices:
        container = container_choice.container
        votes = container_choice.votes
        if container not in results:
            results[container] = 0

        results[container] += votes

    containerduel_list = ContainerDuel.objects.filter(
        published=True,
        date_available__lte=timezone.now(),
        channel_id=channel.pk
    ).only('container1', 'container1_votes', 'container2', 'container2_votes')

    for containerduel in containerduel_list:
        if containerduel.container1 not in results:
            results[containerduel.container1] = 0

        if containerduel.container2 not in results:
            results[containerduel.container2] = 0

        results[containerduel.container1] += containerduel.container1_votes
        results[containerduel.container2] += containerduel.container2_votes

    results_list = results.items()
    results_list.sort(reverse=True, key=itemgetter(1))
    return results_list
