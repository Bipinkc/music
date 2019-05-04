# -*- coding: utf-8 -*-

import importlib
from django.template import Library
from django import template
from django.db.models import Q
from main.models import Song, Playlist

register = Library()

# filters are used to run python scripts from the template directly.
# the filters take an argument and return the result on the basis of that argument

# returns the songs of particular genre
@register.filter
def get_songs(genre):
    return Song.objects.filter(genre=genre)[:8]


# checks if the song is already added to the playlist of the user
@register.filter
def check_playlist(song, user):
    return Playlist.objects.filter(song=song, user=user).exists()


@register.filter
def get_duration(duration):
    return str(duration).split('.')
