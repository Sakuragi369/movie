# -*- coding: utf-8 -*-
import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)


class MovieListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, required=False,
                                 allow_blank=True, allow_null=True, help_text=u'电影名称')


class MovieDetailSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=256, required=True, allow_null=True,
                               allow_blank=True, help_text=u'电影id')
