from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'main'


# urls are used to capture the request from the web browser
# basic structure of url: "path('url_identifier', view_name, name_of_url)"
# the request is then directed to the respective view specified


urlpatterns = [
    path('', index, name='home'),  # url for home page
    path('detail/<int:pk>/', song_detail, name="detail"),  # url for detail of a single song
    path('playlist', playlist, name="playlist"),  # url for the user playlist
    path('genres', genres, name="genres"),  # url for all genre folders
    path('all-songs', all_songs, name="all_songs"),  # url for all songs
    path('list/<slug:genre>/', genre_list, name="genre_list"),  # url for list of songs as per genre
    path('search', search, name='search'),  # for search
    path('add-playlist/<int:pk>/', add_playlist, name='add_playlist'),  # to add playlist of user
    path('usersong/<int:pk>/', add_usersong, name="usersong"),

    # for user authentication
    path('signup', signup, name="signup"),  # url for signup
    path('login', signin, name='login'),  # for login
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # for logout
]
