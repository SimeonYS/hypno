import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import HypnoItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class HypnoSpider(scrapy.Spider):
	name = 'hypno'
	start_urls = ['https://www.hypotecnibanka.cz/o-bance/pro-media/tiskove-zpravy/page:1/?_mf_form_sent_=pressreleasefilter&category=0&date_from=2020-03-04&date_to=2021-03-04&keywords=']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="arrow-li"][2]/a/@href | //li[@class="arrow-li"]/a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//div[@class="documentRelease"]//text()').getall()[2]
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="documentText"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=HypnoItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
