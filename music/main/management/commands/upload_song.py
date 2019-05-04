import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd
from main.models import Song

class Command(BaseCommand):
    help = 'Upload songs'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            total = df['Genre'].count()
            for row in range(total):
                title = df['Title'][row]
                singer = df['Singer'][row]
                year = df['Year'][row]
                duration = df['Duration'][row]
                genre = df['Genre'][row]
                song, created = Song.objects.get_or_create(
                    title=title,
                    artist=singer,
                    release_date=year,
                    genre=genre,
                    duration=duration
                )
            print('success')
        except Exception as e:
            print('Exception occured', e)

