#!/usr/bin/env python
# coding: utf-8

from rest_framework import viewsets
from rest_framework.decorators import list_route
from api.api_serializers import api_serializer_deco, common_serializers
from orm.movies.models import Movies
from utils.api_util import CommonReturn, CodeMsg


class MovieViewSet(viewsets.GenericViewSet):
    u"""電影操作."""

    @list_route(
        methods=['POST'],
        url_path='movie/list',
        serializer_class=common_serializers.MovieListSerializer)
    @api_serializer_deco(u'电影列表')
    def movie_list(self, request, serializer_data=None):
        items = Movies.objects.all()
        data = []
        for item in items:
            data.append({
                "id": str(item.id),
                "image": item.image_url,
                "name_cn": item.name_cn,
                "year": item.year,
                "category": item.category
            })
        return CommonReturn(CodeMsg.SUCCESS, u'success', data)

    @list_route(
        methods=['POST'],
        url_path='movie/detail',
        serializer_class=common_serializers.MovieDetailSerializer)
    @api_serializer_deco(u'电影详情')
    def movie_detail(self, request, serializer_data=None):
        item = Movies.objects(id=serializer_data.get("id")).first()
        res = {}
        if item:
            res = {
                "name_cn": item.name_cn,
                "name": item.name,
                "year": item.year,
                "country": item.country,
                "category": item.category,
                "language": item.language,
                "subtitle": item.subtitle,
                "release_date": item.release_date,
                "score": item.score,
                "file_size": item.file_size,
                "movie_duration": item.movie_duration,
                "director": item.director,
                "introduction": item.introduction,
                "image_url": item.image_url,
                "download_url": item.download_url
            }

        return CommonReturn(CodeMsg.SUCCESS, u'success', res)
