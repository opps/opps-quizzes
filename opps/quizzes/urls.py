# coding:utf-8

from django.conf.urls import patterns, url

from .views import QuizzesDetail


urlpatterns = patterns(
    "",
    url(
      r'',
      QuizzesDetail.as_view(),
      name='detail_quizzes'
    ),
)