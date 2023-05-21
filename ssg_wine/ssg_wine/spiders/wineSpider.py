import time
import re
import scrapy
from ssg_wine.ssg_wine.items import SsgWineItem

class WinespiderSpider(scrapy.Spider):
    name = "wineSpider"

    def start_requests(self):
        url = 'https://www.shinsegae-lnb.com/html/product/wine.html'
        yield scrapy.Request(url, self.parse_product_page, meta={'first_request': True})

    def parse_product_page(self, response): # 페이지

        yield scrapy.Request(response.url, self.parse_product_list, meta={'sequence':0}, dont_filter=True) # 1페이지는 클릭안하고 따로
        for i in range(1,3): #  아마 scrapy의 병렬성 때문에 반복문이여도 모두 1번페이지를 보고 2번페이지 넘어가버려서 3번 페이지가 안나오는거 같다. => 해결못함
            yield scrapy.Request(response.url, self.parse_product_list, meta={'use_selenium': True, 'sequence': i}, dont_filter=True) #next_page는 다음페이지로 이동
#a
    def parse_product_list(self, response): #한페이지에 6개의 상품
        items = SsgWineItem()
        time.sleep(2)
        product_list = response.xpath('//*[@id="productListWrap"]/div[1]/div')
        for product in product_list:
            a_tag = product.xpath('./a')
            viewData = a_tag.xpath('./@onclick').get()
            product_id = re.search(r"viewData\('(\d+)'\)", viewData).group(1)
            items['product_id']=product_id
            product_link = f'https://www.shinsegae-lnb.com/wine/{product_id}'
            time.sleep(1)
            yield scrapy.Request(product_link, self.parse) #상품페이지는 동적으로 작동하지 않아서 셀레니움 작동 안시켜도 무관하다.


    def parse(self, response): # 각 상품
        time.sleep(0.5)
        items = SsgWineItem()
        product_title = response.xpath('//*[@id="container"]/div[3]/div[2]')
        product_kor_name = product_title.xpath('.//div[1]/h3/text()').get()
        product_eng_name = product_title.xpath('.//div[1]/p[1]/text()').get()
        items['product_kor_name'] = product_kor_name
        items['product_eng_name'] = product_eng_name
        product_description_tr = response.xpath('//div[@class="right"]/table/tbody/tr')  # 제품 상세설명 아래 tr 태그
        desList = []
        for tr in product_description_tr:
            des ={}
            des_title = tr.xpath(".//th/text()").get() # 상세설명 타이틀 ex) 'Country / Winery'
            des[des_title] = tr.xpath('.//td/text()').get() # 상세설명 타이틀에 대한 설명 ex) '프랑스 > 루아르 / 도멘 푸르니에'
            desList.append(des)
        items['product_description'] = desList

        content_infos = response.xpath('//div[@class="textDes"]/p')  # TextDes 의 하위 p 태그로 글 담고있는 태그.
        if not content_infos:
            content_infos = response.xpath('//div[@class="textDes"]/div')  # TextDes 의 하위 p 태그로 글 담고있는 태그.
        story = []
        for content_info in content_infos:
            mini_content = content_info.xpath('.//text()').get()
            if mini_content:
                story.append(mini_content)
        items['content_info'] = story


        product_img = response.xpath('//div[contains(@class, "productInner") and contains(@class, "img")]/img/@src').get()  # 이미지 주소 src
        items['product_img'] = f'https://www.shinsegae-lnb.com{product_img}'

        product_features = response.xpath('//div[@class="features"]/dl')  # features 여러개
        three_features = []
        for ftr in product_features:
            feature = {}
            feature_title = ftr.xpath('.//dt/text()').get()
            level = ftr.xpath('.//span[@class="on"]/text()').getall()  # on이 있는것이 현재 레벨
            max_level = max(level)#  on 이 있는것중 제일 큰값
            feature[feature_title] = max_level

            three_features.append(feature)
        items['feature'] = three_features

        yield items

