# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AutoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    brand = Field()
    model = Field()
    level = Field()
    structure = Field()
    price = Field()
    engine = Field()
    gearbox = Field()
