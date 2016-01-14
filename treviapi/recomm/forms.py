# coding: utf-8

from __future__ import unicode_literals
from django import forms
from recomm.models import Music


class MusicEditForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('artist', 'track', 'playlist_id')


class MusicRecommForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('artist', 'track', 'is_recomm', 'playlist_id')
