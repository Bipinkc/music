from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import get_recommendation
from .forms import LoginForm, SignUpForm


# views are used to process the request from the user and render the result in the template
# the user enters a url and the request is passed to the respective views specified in the url
# view function to render the home page
def index(request):
    # get all the genres in the database
    genres = Song.objects.values('genre').distinct()
    if request.user.is_authenticated:
        if UserSong.objects.filter(user=request.user).count() > 1:
            recommendations = get_recommendation(request.user)
            songs = list(set(recommendations['song']))
            recommended = Song.objects.filter(id__in=songs).distinct()

            # send the data to the index page
            return render(request, 'main/index.html', {'genres': genres, 'recommendations': recommended})
        else:
            return render(request, 'main/index.html', {'genres': genres})

    else:
        return render(request, 'main/index.html', {'genres': genres})


# get the detail of the song selected and return it to the song-detail page
def song_detail(request, *args, **kwargs):
    song = Song.objects.get(pk=kwargs.get('pk'))
    if request.user.is_authenticated:
        if UserSong.objects.filter(user=request.user).count() > 1:
            recommendations = get_recommendation(request.user)
            songs = list(set(recommendations['song']))
            recommended = Song.objects.filter(id__in=songs).distinct()

            return render(request, 'main/song-detail.html', {'song': song, 'recommendations': recommended})
        else:
            return render(request, 'main/song-detail.html', {'song': song})
    else:
        return render(request, 'main/song-detail.html', {'song': song})


# login required to ensure that only logged in user can view the playlist page
# if not logged in, the user is redirected to the login page
@login_required(login_url='/login')
def playlist(request, *args, **kwargs):
    # get all the playlist of user
    songs = Playlist.objects.filter(user=request.user)
    return render(request, 'main/playlist.html', {'songs': songs})


# get the list of all genres
def genres(request, *args, **kwargs):
    genres = Song.objects.values('genre').distinct()
    return render(request, 'main/genres.html', {'genres': genres})


# display all the songs
def all_songs(request):
    # order the songs alphabetically on the basis of their title
    songs = Song.objects.order_by('title')
    return render(request, 'main/allsongs.html', {'songs': songs})


# get the list of all songs belonging to a genre
# accepts the genre name in url and displays the list of songs of those genres
def genre_list(request, *args, **kwargs):
    songs = Song.objects.filter(genre=kwargs.get('genre'))
    return render(request, 'main/genre-list.html', {'songs': songs, 'genre': kwargs.get('genre')})

def web_authenticate(username=None, password=None):
    try:
        if "@" in username:
            user = User.objects.get(email__iexact=username)
        else:
            user = User.objects.get(username__iexact=username)
        if user.check_password(password):
            return authenticate(username=user.username, password=password), False
        else:
            return None, True  # Email is correct
    except User.DoesNotExist:
        return None, False  # false Email incorrect


def signin(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:home'))
                else:
                    return render(request, 'main/login.html',
                                  {'form': form,
                                   'login_username': username
                                   })
            else:
                return render(request, 'main/login.html',
                              {'form': form,
                               'login_username': username,
                               'error': 'Username/Password mismatch.'
                               })
        else:
            if request.POST.get('login_username') is not None:
                login_username = request.POST.get('login_username')
            else:
                login_username = ''
            return render(request, 'main/login.html', {
                'form': form,
                'login_username': login_username,
                'error': 'Username/Password mismatch',
            })
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create(username=username, password=password)
            user.set_password(user.password)
            user.is_active = True
            user.save()
            return redirect('/login')

        else:
            username = request.POST.get('username')
            return render(request, 'main/signup.html', {
                'form': form,
                'username': username,
                'valid_username': True,
                'username_error': False
            })
    else:
        form = SignUpForm()
        return render(request, 'main/signup.html', {
            'form': form,
            'valid_username': True,
            'username_error': False
        })


# get all the songs that match the search parameters
def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        songs = Song.objects.filter(title__icontains=query)[:10]

        return render(request, 'main/search_list.html', {'songs': songs})


# function to add a song to the user playlist
@login_required(login_url='/login')
def add_playlist(request, *args, **kwargs):
    song = Song.objects.get(pk=kwargs.get('pk'))
    user = request.user
    obj, created = Playlist.objects.get_or_create(song=song, user=user)
    if created:
        obj.added_on = datetime.now()

    return redirect(reverse('main:detail', kwargs={'pk': song.pk}))


# add the song to user song table after selecting the song. This is required for recommendation
def add_usersong(request, **kwargs):
    song = Song.objects.get(pk=kwargs.get('pk'))
    if request.user.is_authenticated:
        user_song, created = UserSong.objects.get_or_create(song=song, user=request.user)
        if created:
            user_song.times = 1
            user_song.save()
        else:
            user_song.times = user_song.times + 1
            user_song.save()

        return redirect(reverse('main:detail', kwargs={'pk': song.pk}))
    else:
        return redirect(reverse('main:detail', kwargs={'pk': song.pk}))


