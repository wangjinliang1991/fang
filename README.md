# 房天下分布式爬取658城市新房和二手房房源

## 分析网页
* 开始页： http://www.fang.com/SoufunFamily.htm
* 重庆为例： 首页： http://cq.fang.com/
            新房：http://cq.newhouse.fang.com/house/s/
            二手房： http://cq.esf.fang.com/
* 特殊例子： 北京 新房：http://newhouse.fang.com/house/s/
                 二手房： http://esf.fang.com/
             海外需要去除
             
## 首页parse
省份信息比较特殊 ，注意去空格
    ``` province = None
    for tr in trs:
        province_text=xxx 
        if province_text:
            province = province_text
            ``` 
 province和city用response的meta传递给下边的解析函数
 ## 新房parse
 * 页面有部分干扰信息，部分房源后面又单独打广告 如特价房广告
 * 房子类型有些属于别墅，如 景粼原著 house_style和其他的不太一致，暂时还是决定保留类型
 * next_url 翻页的时候记得把province和city用meta传过去
 ## 二手房
 * 检查二手房的时候，把parse链接的新房yield注释掉
 * 北京的二手房url总是重定向到成都，302，meta加上禁止重定向后，不解析二手房了  
 方法： 解析的部分将北京的response找到，重新解析，response.selector接受的是HTML语言？
 暂时先不管北京二手房的bug
 
 ## 数据库保存
 pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
    
 
            
                         