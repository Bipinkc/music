from django.db import models
from django.conf import settings


# model to store data about songs
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.CharField(max_length=10)
    image = models.ImageField(upload_to='music/banner/', null=True, blank=True)
    genre = models.CharField(max_length=50)
    songfile = models.FileField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


# model to store data about the songs listened by the user
class UserSong(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='song', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="play", on_delete=models.CASCADE)
    times = models.IntegerField(default=0)


# model to store the playlist created by user
class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playlist', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='playlist', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)
