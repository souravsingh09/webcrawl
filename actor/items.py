import scrapy
import apify

class PostsSpider(scrapy.Spider):
    name = "medical"

    start_urls = [
        'https://academic.oup.com/eurheartj/issue/41/Supplement_2'
    ]

    def parse(self, response):
        # lst = []

        for post in response.css('h5.customLink.item-title'):

            full_url = response.urljoin('https://academic.oup.com' + post.css('a').attrib['href'])
            print(full_url)
            yield scrapy.Request(full_url,
                                 callback=self.get_details)

    def get_details(self, response):
            # This method is called on by the 'parse' method above. It scrapes the URLs
            # that have been extracted in the previous step.
        # try:
        title_detail = response.css("div.ContentTab h5.abstract-title").extract_first()
        print("Found details: " + title_detail )
        # except:
        #     title_detail = response.css("div.ContentTab h5.abstract-title").extract_first()
        #     print("Found details: pppppp" )


