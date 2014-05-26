# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import ContainerPoll, ContainerDuel


class VoteBaseView(SingleObjectMixin, View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.object.get_form(request.POST)
        response = redirect(self.object.get_absolute_url())
        if form.is_valid():
            choice = form.cleaned_data['choice']
            if self.object.vote(request, choice):
                response.set_cookie(self.object.cookie_name, '1')
        return response


class ContainerPollVoteView(VoteBaseView):
    model = ContainerPoll


class ContainerDuelVoteView(VoteBaseView):
    model = ContainerDuel
