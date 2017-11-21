# -*- coding: utf-8 -*-
from api import SlashOptionRouter

from views import movies
router = SlashOptionRouter()

router.register(r'account', movies.MovieViewSet, base_name='movie')

urlpatterns = router.urls
