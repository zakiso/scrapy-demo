# -*- coding: utf-8 -*-  
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from auto.items import AutoItem

class AutoSpider(Spider):
    name = "auto"
    allowed_domains = ["car.autohome.com.cn"]
    start_urls = [
        "http://car.autohome.com.cn/"
        ]
    
    def parse(self,response):
        sel = Selector(response)
        brandSites = sel.xpath('//div[@class]/span[@class]')
        brandUrls = []
        for brandSite in brandSites:
            brandUrl = brandSite.xpath('a[@href]/@href').extract()
            try:
                url = "http://car.autohome.com.cn" + brandUrl[0]
                print url
                brandUrls.append(url)
            except Exception, e:
                pass
        
        for carListUrl in brandUrls:
            yield Request(carListUrl,callback=self.parseBrand)
            

    def parseBrand(self,response):
        sel = Selector(response)
        carLists = sel.xpath("//div[contains(@class='list-cont',@data-value)]")
        carBrand = sel.xpath("//h1[@class='seo-text']/text()").extract()
        print carBrand[0].encode('utf-8')
        items = []
        for car in carLists:
            carType = car.xpath("//div[@class='main-title']/a/text()").extract()
            carLevel = car.xpath("//div/ul[@class='lever-ul']/li[not(a|div|span)]/text()").extract()
            carStructure = car.xpath("//div/ul[@class='lever-ul']/li[not(div|span)]/a/text()").extract()
            carGearbox = car.xpath("//div/ul[@class='lever-ul']/li[4]/a/text()").extract()
            carEngine = car.xpath("//div/ul[@class='lever-ul']/li[not(@class|div|a)]/span[@title]/a[@href]/text()").extract()
            carPrice = car.xpath("//span[@class]/span[@class='font-arial']/text()").extract()
            engineInfo = ''
            for engine in carEngine:
                engineInfo = engineInfo + " " + engine.encode('utf-8')
            # carGearbox = info.xpath("a/text()").extract()
            try:
                item = AutoItem()
                item['brand'] = carBrand[0].encode('utf-8')
                item['model'] = carType[0].encode('utf-8')
                item['level'] = carLevel[0].encode('utf-8')
                item['structure'] = carStructure[0].encode('utf-8')
                item['price'] = carPrice[0].encode('utf-8')
                item['engine'] = engineInfo
                item['gearbox'] = carGearbox[0].encode('utf-8')
                items.append(item)
            except Exception, e:
                print e
            return items
        
        #如果有下一页的继续抓取下一页
        carNextPageUrls = car.xpath("//div[@class='page']/a[not(@class)]/@href").extract()  

        for pageUrl in carNextPageUrls:
            nextPageUrl = "http://car.autohome.com.cn" + pageUrl
            self.make_requests_from_url(nextPageUrl).replace(callback=self.parseNextPage)
        
    def parseNextPage(self,response):
        sel = Selector(response)
        carLists = sel.xpath("//div[contains(@class='list-cont',@data-value)]")
        print "parseNextPage"
        for car in carLists:
            carType = car.xpath("div[@class='main-title']/a/text()").extract()
            print "carlists"
            try:
                print carType[0].encode('utf-8')
                print "running!!!!"
            except Exception, e:
                pass
    