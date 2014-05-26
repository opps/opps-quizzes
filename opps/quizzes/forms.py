# -*- coding: utf-8 -*-

from django import forms


class BaseQuizForm(forms.Form):
    choice = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        super(BaseQuizForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ModelChoiceField(
            queryset=instance.get_choices(),
            widget=forms.RadioSelect,
            empty_label=None
        )
