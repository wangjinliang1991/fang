# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'newhouse'
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    # 几居室
    house_style = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 区域
    district = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 楼盘详情页的url
    origin_url = scrapy.Field()

class ESFItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'esf'
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名字
    title = scrapy.Field()
    # 小区卖点
    name = scrapy.Field()
    # 几室几厅
    house_style = scrapy.Field()
    # 面积
    house_area = scrapy.Field()
    # 层高
    house_floor = scrapy.Field()
    # 方位
    house_direction = scrapy.Field()
    # 房屋年限
    house_year = scrapy.Field()
    # 备注信息
    house_append = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 楼盘详情页的url
    origin_url = scrapy.Field()