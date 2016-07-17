import scrapy
from settings import USERNAME,PASSWORD
import json

class weiboSpider(scrapy.Spider):
    name = "weibo"
    start_urls = [
        "https://passport.weibo.cn/signin/login"
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"username":USERNAME,"password":PASSWORD},
            method="POST",
            url="https://passport.weibo.cn/sso/login",
            callback=self.after_login
        )

    def after_login(self, response):
        for i in range(5):
            yield scrapy.Request(
                "http://m.weibo.cn/index/feed?format=cards&next_cursor=3997919323927318&page=%s" % (i + 1),
                self.parse_detail
            )

    def parse_detail(self, response):
        objs = json.loads(response.body)
        obj = objs[0]
        for item in obj["card_group"]:
            print item["mblog"]["text"]