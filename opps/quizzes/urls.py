# coding:utf-8

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    "",
    url(r'^quizzes/containerpoll/vote/(?P<pk>\d+)/', views.ContainerPollVoteView.as_view(), name='containerpoll_vote'),
    url(r'^quizzes/containerduel/vote/(?P<pk>\d+)/', views.ContainerDuelVoteView.as_view(), name='containerduel_vote'),
)
