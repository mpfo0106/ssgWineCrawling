import scrapy

class SsgWineItem(scrapy.Item):
    product_id = scrapy.Field()
    product_kor_name = scrapy.Field()
    product_eng_name = scrapy.Field()
    product_description = scrapy.Field()
    content_info = scrapy.Field()
    product_img = scrapy.Field()
    feature = scrapy.Field()
