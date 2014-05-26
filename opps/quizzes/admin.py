# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.widgets import OppsEditor
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

from .models import ContainerPoll, ContainerPollChoice, ContainerDuel


@apply_opps_rules('quizzes')
class QuizBaseAdmin(PublishableAdmin):
    actions = ['publish']
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available',
                    'date_end', 'published', 'show_results', 'preview_url']
    list_filter = ["date_end", "date_available", "published", "channel"]
    readonly_fields = ['get_http_absolute_url', 'short_url', 'image_thumb']
    raw_id_fields = ['main_image', 'channel']
    search_fields = ['title', 'slug']


class ContainerPollChoiceInline(admin.TabularInline):
    model = ContainerPollChoice
    fk_name = 'containerpoll'
    raw_id_fields = ['container', ]
    readonly_fields = ['votes', ]
    fieldsets = [(None, {'fields': (
        'container', 'votes')})]
    extra = 0


class ContainerPollAdmin(QuizBaseAdmin):
    inlines = [ContainerPollChoiceInline, ]
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug')}),
        (_(u'Content'), {
            'fields': (('main_image', 'image_thumb',), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', ('date_available', 'date_end'),
                       'show_results')}),
    )


class ContainerDuelAdmin(QuizBaseAdmin):
    readonly_fields = ['get_http_absolute_url', 'short_url', 'image_thumb',
                       'container1_votes', 'container2_votes']
    raw_id_fields = ['main_image', 'channel', 'container1', 'container2']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug')}),
        (_(u'Duel'), {
            'fields': (('container1', 'container1_votes',),
                       ('container2', 'container2_votes',))}),
        (_(u'Content'), {
            'fields': (('main_image', 'image_thumb',), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', ('date_available', 'date_end'),
                       'show_results')}),
    )

admin.site.register(ContainerPoll, ContainerPollAdmin)
admin.site.register(ContainerDuel, ContainerDuelAdmin)
