# -*- coding: utf-8 -*-
import datetime
import json
import logging

from django.conf import settings
from mongoengine import *

connect('dytt')

logger = logging.getLogger(__name__)


class Movies(Document):
    """movies."""
    name_cn = StringField(max_length=1024)
    name = StringField(max_length=1024)
    year = StringField(max_length=64)
    country = StringField(max_length=64)
    category = StringField(max_length=64)
    language = StringField(max_length=64)
    subtitle = StringField(max_length=64)
    release_date = StringField(max_length=64)  # 上映时间
    score = StringField(max_length=64)
    file_size = StringField(max_length=64)
    movie_duration = StringField(max_length=64)
    director = StringField(max_length=64)
    introduction = StringField(max_length=1024)
    image_url = StringField(max_length=1024)
    download_url = StringField(max_length=1024)

    meta = {
        'ordering': ['-release_data']
    }


class MoviesUrl(Document):
    """列表页电影详情页url"""
    url = StringField(max_length=256)
