import pandas as pd
from .models import UserSong
from sklearn.model_selection import train_test_split
from . import Recommenders


def get_recommendation(user):
    df = pd.DataFrame(list(UserSong.objects.filter(user=user).values('user', 'song', 'times').order_by('-times').distinct())) # create pandas dataframe from databse

    train_data, test_data = train_test_split(df, test_size=0.20, random_state=0) # obtain test datasets
    pm = Recommenders.popularity_recommender_py()
    pm.create(train_data, 'user', 'song') # test case creation

    return pm.recommend(user) # recommend and return the recommended song list

