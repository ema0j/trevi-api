# -*- coding: utf-8 -*-

from recomm.models import Music
from recomm.forms import (MusicEditForm, MusicRecommForm)

from django.shortcuts import (render, redirect)
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse

from recomm.lastfm import LastFM
from recomm.recomm_engine import RecommEngine

from recomm.serializers import RecommSerializer
from rest_framework import generics

import urllib
import urlparse


class MusicList(ListView):
    template_name = "musiclist.html"
    model = Music
    last_request = LastFM()

    def post(self, request, *args, **kwargs):
        form = MusicEditForm(request.POST)
        if form.is_valid():
            form.save()
            rvalue = self.last_request.get_recomm(request.POST)

            for rv in rvalue:
                form_recomm = MusicRecommForm({'artist': rv['artist'], 'track': rv['track'], 'is_recomm': 1})
                form_recomm.save()
        return redirect(reverse('view_music_list'))

    def get_context_data(self, **kwargs):
        context = super(MusicList, self).get_context_data(**kwargs)
        context['form'] = MusicEditForm
        return context


class RecommList(generics.ListCreateAPIView):
    queryset = Music.objects.all()[:5]
    serializer_class = RecommSerializer


class RecommGetLimit(generics.ListCreateAPIView):
    serializer_class = RecommSerializer
    last_request = LastFM()

	#### Use when you have enough data ###
	#rengine = RecommEngine("./db.sqlite3")
	#rengine.run()   

    def get_queryset(self, **kwargs):
        playlist_id = self.kwargs['playlist_id']
        limit = self.kwargs['limit']

        return Music.objects.filter(playlist_id=playlist_id)[:limit]


class RecommUpdateLimit(generics.ListCreateAPIView):
    serializer_class = RecommSerializer
    last_request = LastFM()
	
	#### Use when you have enough data ###
	#rengine = RecommEngine("./db.sqlite3")
	#rengine.run()   

    def get_queryset(self, **kwargs):
        playlist_id = self.kwargs['playlist_id']
        limit = self.kwargs['limit']
        track = self.kwargs['track']
        search = self.last_request.get_search({'track': track, 'limit': limit})
        searched_track = search["results"]["trackmatches"]["track"][0]
        rvalue = self.last_request.get_recomm({'artist': searched_track["artist"], 'track': searched_track["name"], 'limit': limit})
        for rv in rvalue:
            form_recomm = MusicRecommForm({'artist': rv['artist'], 'track': rv['track'], 'is_recomm': 1, 'playlist_id': playlist_id})
            form_recomm.save()
        return rvalue
        #return Music.objects.filter(playlist_id=playlist_id)[:limit]
