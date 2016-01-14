# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Music(models.Model):
    mdid = models.CharField(max_length=30, blank=True)
    artist = models.CharField(max_length=50)
    track = models.CharField(max_length=50)
    is_recomm = models.IntegerField(blank=True, default=0)
    playlist_id = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "%s" % (self.track,)
