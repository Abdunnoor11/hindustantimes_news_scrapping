import scrapy


class NewsspiderSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['https://www.jugantor.com/']
    start_urls = ['https://www.hindustantimes.com/topic']

    def parse(self, response):
        for link in response.css('.tpcTags a::attr(href)'):        
            yield response.follow(link.get(), callback=self.parse_news_topics)                  
    
    def parse_news_topics(self, response):
        for link in response.css('.listingPage .hdg3 a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_news_page, meta={'cat':1 })                  

    def parse_news_page(self, response):
        try:
            yield {             
                'date_posted': response.css('#dataHolder .dateTime::text').get()[11:],
                'title': response.css('#dataHolder .hdg1::text').get(),
                'auther': response.css('#dataHolder .byLineAuthor a::text').get(),
                'article_content': "".join(response.css('#dataHolder .detail *::text').getall()).replace("\n",""),          
                'tags': response.css('.storyTopics .tpsList a::text').getall()[:-1],
                'link': response.url,        
            }
        except:
            pass

