# -*- coding: utf-8 -*-
import scrapy
import json
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    #allowed_domains = ["dmoz.org"]
    # http://soa.dooioo.com/api/v4/online/house/ershoufang/search?access_token=7poanTTBCymmgE0FOn1oKp&channel=ershoufang&cityCode=sh&client=wap&limit_count=20&limit_offset=0

    # access_token
    # channel=ershoufang
    # cityCode=sh
    # client=wap
    # limit_count=20
    # limit_offset=0

    # district_id
    # district_name 区

    # bizcircle_id
    # bizcircle_name 板块

    # p=p4  =>  p4: 200-300,  p5: 300-500
    # b=b200to280  => 200-280万

    start_urls = [
       'http://soa.dooioo.com/api/v4/online/house/ershoufang/search?access_token=7poanTTBCymmgE0FOn1oKp&b=b200to500&channel=ershoufang&cityCode=sh&client=wap&limit_count=20&limit_offset=0&s=s1'
    ]

    def increase_offset(self, url, num):
        url_parsed = urlparse.urlparse(url)
        query = dict(urlparse.parse_qsl(url_parsed.query))
        query['limit_offset'] = 20 + int(query['limit_offset'])
        query_str = urlencode(query)
        url_parsed = url_parsed._replace(query=query_str)
        return url_parsed.geturl()

    def parse(self, response):
        result = json.loads(response.body)
        for item in result['data']['list']:
            yield item

        total_count = result['data']['total_count']
        has_more_data = result['data']['has_more_data']

        if has_more_data == 1:
            new_url = self.increase_offset(response.url, 20)
            print "get new url: ", new_url
            yield scrapy.Request(new_url, callback=self.parse)

