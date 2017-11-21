# -*- coding: utf-8 -*-

import urllib2
import re
import requests
from orm.movies.models import Movies, MoviesUrl

url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_2.html"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
headers = {'User-Agent': user_agent}

try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

r_url = re.compile('<b>.*?<a\s*href="(.*?)"\s*class="ulink">', re.DOTALL)

result = ""
segments = r_url.findall(html)
host = 'http://www.ygdy8.net'

for seg in segments:
    result = host + seg
    movie_url = MoviesUrl(url=result)
    movie_url.save()

items = MoviesUrl.objects.all()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Host": "www.ygdy8.net",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
}
for item in items:
    resp = requests.get(item.url, headers=headers, timeout=10)
    resp.encoding = 'gb18030'

    r_name_cn = re.compile(u"◎译　　名(.*?)<br />", re.DOTALL)
    r_name = re.compile(u"◎片　　名(.*?)<br />", re.DOTALL)
    r_year = re.compile(u"◎年　　代(.*?)<br />", re.DOTALL)
    r_country = re.compile(u"◎(产　　地|国　　家)(.*?)<br />", re.DOTALL)
    r_category = re.compile(u"◎类　　别(.*?)<br />", re.DOTALL)
    r_language = re.compile(u"◎语　　言(.*?)<br />", re.DOTALL)
    r_subtitle = re.compile(u"◎字　　幕(.*?)<br />", re.DOTALL)
    r_release_date = re.compile(u"◎上映日期(.*?)<br />", re.DOTALL)
    r_score = re.compile(u"◎(IMDB评分|豆瓣评分)(.*?)<br />", re.DOTALL | re.IGNORECASE)
    r_file_size = re.compile(u"◎文件大小(.*?)<br />", re.DOTALL)
    r_movie_duration = re.compile(u"◎片　　长(.*?)<br />", re.DOTALL)
    r_director = re.compile(u"◎导　　演(.*?)<br />", re.DOTALL)
    r_introduction = re.compile(u"◎简　　介 <br /><br />(.*?)<br />")
    r_image_url = re.compile('border="0".*?src=(.*?) alt="" />', re.DOTALL)
    r_download_url = re.compile('<td.*?bgcolor="#fdfddf">.*?<a.*?>(.*?)</a>', re.DOTALL)

    detail = {
        "name_cn": r_name_cn,
        "name": r_name,
        "year": r_year,
        "country": r_country,
        "category": r_category,
        "language": r_language,
        "subtitle": r_subtitle,
        "release_date": r_release_date,
        "score": r_score,
        "file_size": r_file_size,
        "movie_duration": r_movie_duration,
        "director": r_director,
        "introduction": r_introduction
    }

    images = r_image_url.findall(resp.text)
    urls = r_download_url.findall(resp.text)

    for key in detail:
        m = detail[key].search(resp.text)
        if m:
            field = m.group(m.lastindex).replace('&nbsp;', '').replace(';', ',').strip()
            detail[key] = field
        else:
            detail[key] = None

    movie_obj = Movies.objects(name_cn=detail.get("name_cn"), name=detail.get("name")).first()
    if movie_obj:
        """更新"""
        movie_obj.update(
            name_cn=detail.get("name_cn"),
            name=detail.get("name"),
            year=detail.get("year"),
            country=detail.get("country"),
            category=detail.get("category"),
            language=detail.get("language"),
            subtitle=detail.get("subtitle"),
            release_date=detail.get("release_date"),
            score=detail.get("score"),
            file_size=detail.get("file_size"),
            movie_duration=detail.get("movie_duration"),
            director=detail.get("director"),
            introduction=detail.get("introduction"),
            image_url=images[1] if len(images) >= 2 else '',
            download_url=urls[0] if urls else ''
        )
    else:
        movie_obj = Movies(
            name_cn=detail.get("name_cn"),
            name=detail.get("name"),
            year=detail.get("year"),
            country=detail.get("country"),
            category=detail.get("category"),
            language=detail.get("language"),
            subtitle=detail.get("subtitle"),
            release_date=detail.get("release_date"),
            score=detail.get("score"),
            file_size=detail.get("file_size"),
            movie_duration=detail.get("movie_duration"),
            director=detail.get("director"),
            introduction=detail.get("introduction"),
            image_url=images[1] if len(images) >= 2 else '',
            download_url=urls[0] if urls else ''
        )
        movie_obj.save()
