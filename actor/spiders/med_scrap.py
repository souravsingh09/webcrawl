from unittest import result

import apify
import scrapy
import unidecode
from scrapy.exceptions import IgnoreRequest
from scrapy_proxy_pool.policy import BanDetectionPolicy


class PostsSpider(scrapy.Spider):
    name = "medical"

    start_urls = [
        'https://academic.oup.com/eurheartj/issue/41/Supplement_2?page=1'
    ]

    def parse(self, response):
        print("Start")
        next_page = response.css('li.PagedList-skipToNext a').attrib['href']
        print("Start 1")
        if next_page is not None:
            print("Start 2")
            for post in response.css('h5.customLink.item-title'):
                print("Start 3")
                full_url = response.urljoin('https://academic.oup.com' + post.css('a').attrib['href'])
                print("Start 4")
                try:
                    print("Start 5 ")
                    yield scrapy.Request(full_url, callback=self.get_details)
                    print("Start 6")
                    yield response.follow(next_page,callback=self.parse)
                    print("Start 7")
                except :
                    print("lol")


    def get_details(self, response):
            # This method is called on by the 'parse' method above. It scrapes the URLs
            # that have been extracted in the previous step.
        # try:
        #title_detail = response.css("section.abstract p.chapter-para::text").extract_first()
        #print("Found details: " + title_detail )
        #
            #yield{
            try :
                print("Start 9")
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
                print("Start 10")
                yield result
            except:
                print("out of syl")



            #Apify.pushData(result)
            #apify.pushData(output)


