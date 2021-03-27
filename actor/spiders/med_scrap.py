from unittest import result

import scrapy
import unidecode
import apify
from scrapy.exceptions import IgnoreRequest
from scrapy_proxy_pool.policy import BanDetectionPolicy


class PostsSpider(scrapy.Spider):
    name = "medical"

    start_urls = [
        'https://academic.oup.com/eurheartj/issue/41/Supplement_2?page=1'
    ]

    def parse(self, response):

        print("Start")
        for post in response.css('h5.customLink.item-title'):

            full_url = response.urljoin('https://academic.oup.com' + post.css('a').attrib['href'])
            yield scrapy.Request(full_url, callback=self.get_details)

            next_page = response.css('li.PagedList-skipToNext a').attrib['href']

            print(next_page)
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


    def get_details(self, response):
            # This method is called on by the 'parse' method above. It scrapes the URLs
            # that have been extracted in the previous step.

            result = {
                'url': response.url,
                'Introduction': response.css("div.title::text").get(),
                'Introduction_text': unidecode.unidecode(response.css("section.abstract p.chapter-para::text").get()),

                'Aim': response.css("div.title::text")[1].get(),
                'Aim_text': unidecode.unidecode(response.css("section.abstract p.chapter-para::text")[1].get()),

                'Methods': response.css("div.title::text")[2].get(),
                'Methods_text': unidecode.unidecode(response.css("section.abstract p.chapter-para::text")[2].get()),

                'Result': response.css("div.title::text")[3].get(),
                'Result_text': unidecode.unidecode(response.css("section.abstract p.chapter-para::text")[3].get()),

                'Conclusion': response.css("div.title::text")[4].get(),
                'Conclusion_text': unidecode.unidecode(response.css("section.abstract p.chapter-para::text")[4].get())

            }

            #yield result

            #Apify.pushData(result)
            apify.pushData(result)


