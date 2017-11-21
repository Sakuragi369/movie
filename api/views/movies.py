#!/usr/bin/env python
# coding: utf-8

from rest_framework import viewsets
from rest_framework.decorators import list_route
from api.api_serializers import api_serializer_deco, common_serializers


class MovieViewSet(viewsets.GenericViewSet):
    u"""電影操作."""

    @list_route(
        methods=['POST'],
        url_path='movie/list',
        serializer_class=common_serializers.MovieListSerializer)
    @api_serializer_deco(u'电影列表')
    def movie_list(self, request, serializer_data=None):
        pass

    @list_route(
        methods=['POST'],
        url_path='movie/detail',
        serializer_class=common_serializers.MovieListSerializer)
    @api_serializer_deco(u'电影详情')
    def movie_detail(self, request, serializer_data=None):
        pass
