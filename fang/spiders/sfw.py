# -*- coding: utf-8 -*-
import re

import requests
import scrapy
from ..items import NewhouseItem,ESFItem
from scrapy_redis.spiders import RedisSpider

class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    # start_urls = ['http://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls"

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('./td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r'\s','',province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue

            city_td = tds[1]
            city_links = city_td.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('./text()').get()
                city_url = city_link.xpath('./@href').get()
                if 'bj.' in city_url:
                    city_newhouse_url = 'http://newhouse.fang.com/house/s/'
                    city_esf_url = 'http://esf.fang.com/'
                else:
                    city_newhouse_url = re.sub("fang.com","newhouse.fang.com/house/s",city_url)
                    city_esf_url = re.sub("fang.com","esf.fang.com",city_url)
                # print(province,city)
                # print(city_esf_url,city_newhouse_url)
                yield scrapy.Request(url=city_newhouse_url,callback=self.parse_newhouse,meta={'info':(province,city)},dont_filter=True)
                yield scrapy.Request(url=city_esf_url,callback=self.parse_esf,meta={'info':(province,city),})
            #     break
            # break



    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath('//div[contains(@class,"nl_con")]/ul/li')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name:
                name = name.strip()
            else:
                continue

            house_style = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            # house_style = list(filter(lambda x:x.endswith("居"),house_style))
            area = ''.join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            area = re.sub('－|/	|\s','',area)
            address = li.xpath('.//div[@class="address"]/a/@title').get()
            district = li.xpath('.//div[@class="address"]/a/span/text()').get()
            district = re.sub('\s|\[|\]','',str(district))
            # print(district)
            sale = ''.join(li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').getall())
            price = ''.join(li.xpath('.//div[@class="nhouse_price"]//text()').getall()).strip()
            origin_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            item = NewhouseItem(name=name,house_style=house_style,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url,province=province,city=city)
            yield item

        next_url = response.xpath('.//div[@class="page"]//li/a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={'info':(province,city)})



    def parse_esf(self,response):
        province,city = response.meta.get('info')
        # if "北京" in city:
        #     response = requests.get('http://esf.fang.com/')

        dls = response.selector.xpath('//div[contains(@class,"shop_list")]/dl')
        for dl in dls:
            name = dl.xpath('.//dd/h4/a/@title').get()
            if name:
                name = name.strip()
            else:
                continue

            infos = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
            infos = list(map(lambda x:re.sub('\s','',x),infos))
            for info in infos:
                if info.endswith("厅"):
                   house_style  = info
                elif info.endswith("㎡"):
                   house_area  = info
                elif "层" in info:
                    house_floor = info
                elif "向" in info:
                    house_direction = info
                elif "年" in info:
                    house_year = info.replace('建','')

            house_append = dl.xpath('.//p[contains(@class,"label")]/span/text()').get()
            if not house_append:
                continue
            address = ''.join(dl.xpath('.//p[@class="add_shop"]//span/text()').getall())
            title = ''.join(dl.xpath('.//p[@class="add_shop"]/a/@title').getall())
            price = ''.join(dl.xpath('.//dd[@class="price_right"]/span[position()=1]//text()').getall())
            unit = ''.join(dl.xpath('.//dd[@class="price_right"]/span[position()=2]//text()').getall())
            origin_url = dl.xpath('.//dd/h4/a/@href').get()
            origin_url = response.urljoin(origin_url)
            item = ESFItem(name=name,house_style=house_style,house_area=house_area,house_year=house_year,house_append=house_append,house_floor=house_floor,house_direction=house_direction,address=address,price=price,unit=unit,origin_url=origin_url,title=title,province=province,city=city)
            yield item

        next_url = response.xpath('//div[@class="page_al"]/p[position()=1]/a/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta={'info':(province,city)})







