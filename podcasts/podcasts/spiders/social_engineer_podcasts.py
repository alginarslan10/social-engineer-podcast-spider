# -*- coding: utf-8 -*-
import scrapy
#from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider#, Rule
from podcasts.items import PodcastsItem

class SocialEngineerPodcastsSpider(CrawlSpider):
    name = 'social-engineer-podcasts'
    allowed_domains = ['www.social-engineer.org','hwcdn.libsyn.com']
    start_urls = ['http://www.social-engineer.org']
    max_id=17

    #rules = (
    #    Rule(LinkExtractor(allow='http://www.social-engineer.org/category/podcast/page/*'), callback='get_shownotes', follow=True),
    #)
    
    def start_requests(self):
        page_urls=[]
        for i in range(self.max_id):page_urls.append('https://www.social-engineer.org/category/podcast/page/'+str(i))
        
        for page_url in page_urls:
            yield scrapy.Request(url=page_url,callback=self.get_shownotes)
    
    def get_shownotes(self,response):
        shownote_urls = response.css("a.button-large::attr(href)").extract()
        
        for shownote_url in shownote_urls:
            yield response.follow(url=shownote_url,callback=self.parse_item)
    
    def get_download(self,response):
        download_url = response.css("a.button-large::attr(href)").extract_first()
        
        
        yield response.follow(download_url,callback=self.parse_item)
        
    def parse_item(self, response):
        file_url = response.css("a.button-large::attr(href)").extract_first()
        file_url = response.urljoin(file_url)
        item = PodcastsItem()
        item['file_urls'] = [file_url]
        yield item
