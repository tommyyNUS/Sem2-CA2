# -*- coding: utf-8 -*-
#import packages
import datetime
import scrapy
from ImageScraper.items import AnimalImage

class AnimalSpider(scrapy.Spider):
	name = "pyimagesearch-animal-spider"
	start_urls = ["https://pixabay.com/photos/search/elephants/"]
    
def parse(self, response):
		# let's only gather Time U.S. magazine covers
		url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")
		yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_page)

def parse_page(self, response):
		# loop over all cover link elements that link off to the large
		# cover of the magazine and yield a request to grab the cove
		# data and image
		for href in response.xpath("//@div[@class='item'/@a/@href]"):
			yield scrapy.Request(href.xpath("@href").extract_first(),
				self.parse_covers)
 
		# extract the 'Next' link from the pagination, load it, and
		# parse it
		next = response.css("div.pages").xpath("a[contains(., 'Next page')]")
		yield scrapy.Request(next.xpath("@href").extract_first(), self.parse_page)

def parse_image(self, response):
		# grab the URL of the cover image
		img = response.css(".art-cover-photo figure a img").xpath("@src")
		imageURL = img.extract_first()
 
		# grab the title and publication date of the current issue
		title = response.css(".content-main-aside h1::text").extract_first()

		# yield the result
		yield AnimalImage(title=title, file_urls=[imageURL])