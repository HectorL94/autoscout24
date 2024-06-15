import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from .brute_force_urls import urls


class CrawlerAutoscout24Spider(CrawlSpider):
    name = "crawler_autoscout24"
    allowed_domains = ["www.autoscout24.it"]
    start_urls = urls
    
    li_car_extractor = LinkExtractor(restrict_xpaths=('//div[contains(@class,"Item")]//a'))

    rules = (Rule(li_car_extractor, callback="parse_item", follow=True),)

    def parse_item(self, response):
        tester = {}
        title = response.xpath('//h1//text()').getall()
        car_prop = response.xpath('//div[contains(@class,"VehicleOverview_itemContainer")]//text()').getall()
        for indice,valor in enumerate(car_prop):
            if indice%2 == 0:
                tester[valor] = car_prop[indice + 1]
        dl_elements = response.xpath('//dl[not(ancestor::div[@id="finance-section"])]')
        for dl_element in dl_elements:
            dt_elements = dl_element.xpath('.//dt')
            dd_elements = dl_element.xpath('.//dd')
            
            for dt_element, dd_element in zip(dt_elements, dd_elements):
                dt_text = dt_element.xpath('string()').get().strip()
                dd_texts = dd_element.xpath('.//text()').getall()
                if len(dd_texts) > 1:
                    dd_text = ', '.join(dd_texts)
                else:
                    dd_text = dd_element.xpath('string()').get().strip()
                
                tester[dt_text] = dd_text
        
        final = {
            'URL': response.url,
            'Marca': title[0],
            'Modello': title[1],
            'Auto': ' '.join(title),
            'Prezzo': response.xpath('//span[contains(@class,"PriceInfo")]/text()').get(),
            'Adress': response.xpath('//a[contains(@class, "LocationWithPin") and starts-with(@href, "https://maps.google.com")]//text()').get() 
        }
        final.update(tester)
        
        yield final