# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.widgets import OppsEditor
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

from .models import Quizzes



@apply_opps_rules('quizzes')
class QuizzesAdmin(PublishableAdmin):
    """ quizzes Admin """


admin.site.register(Quizzes, QuizzesAdmin)