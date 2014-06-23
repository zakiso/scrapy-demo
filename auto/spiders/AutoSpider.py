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
        brandSites = sel.xpath("//div[@class]/span[@class]")
        brandUrls = []
        for brandSite in brandSites:
            print brandSite
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
        carLists = sel.xpath("//div[@class='list-cont-main']")
        carBrand = sel.xpath("//h1[@class='seo-text']/text()").extract()
        print carBrand[0].encode('utf-8')
        items = []
        for car in carLists:
            carType = car.xpath("div[@class='main-title']/a/text()").extract()
            carLevel = car.xpath("div[@class='main-lever']/div/ul[@class='lever-ul']/li[not(a|div|span)]/text()").extract()
            carStructure = car.xpath("div[@class='main-lever']/div/ul[@class='lever-ul']/li[not(div|span)]/a/text()").extract()
            carGearboxList = car.xpath("div[@class='main-lever']/div/ul[@class='lever-ul']/li[4]/a")
            carGearbox = ""
            for gear in carGearboxList:
                gearbox = gear.xpath("text()").extract()
                carGearbox = carGearbox + " " + gearbox[0].encode('utf-8')

            carEngineList = car.xpath("div[@class='main-lever']/div/ul[@class='lever-ul']/li[not(@class|div|a)]/span[@title]/a[@href]")
            carPrice = car.xpath("div/div/div/span[@class]/span[@class='font-arial']/text()").extract()
            carEngine = ""
            for engine in carEngineList:
                engineInfo = engine.xpath("text()").extract()
                carEngine = carEngine + " " + engineInfo[0].encode('utf-8')

            try:
                item = AutoItem()
                item['brand'] = carBrand[0].encode('utf-8')
                item['model'] = carType[0].encode('utf-8')
                item['level'] = carLevel[0].encode('utf-8')
                item['structure'] = carStructure[0].encode('utf-8')
                item['price'] = carPrice[0].encode('utf-8')
                item['engine'] = carEngine
                item['gearbox'] = carGearbox
                items.append(item)
            except Exception, e:
                print e
        
        return items
        
    #     carNextPageUrls = sel.xpath("//div[@class='page']/a[not(@class)]/@href").extract() 
    #     解析下一页的数据
    #     for pageUrl in carNextPageUrls:
    #         nextPageUrl = "http://car.autohome.com.cn" + pageUrl
    #         self.make_requests_from_url(nextPageUrl).replace(callback=self.parseNextPage)
        
    # def parseNextPage(self,response):
    #     print 'testtesttest'
    #     sel = Selector(response)
    #     carLists = sel.xpath("//div[contains(@class='list-cont',@data-value)]")
    #     print "parseNextPage"
    #         carType = car.xpath("div[@class='main-title']/a/text()").extract()
    #         try:
    #             print carType[0].encode('utf-8')
    #         except Exception, e:
    #             pass
    # 