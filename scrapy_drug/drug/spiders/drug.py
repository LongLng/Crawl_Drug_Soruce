import re
import string
import requests
import scrapy
from scrapy.http import Request
import os
import scrapy
from items import DrugItem
import time
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import json

headers = {
    "accept": "*/*",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "x5QVBx45-eNqqBU5TThzMS85b4FJfY5Z67Pw",
    "cookie": "cf_chl_2=06d1f7a6cfeb2b1; cf_chl_prog=x15; cf_clearance=HbcESmswj3STAru.rnighD5taOb1WmtPpdiS741bssI-1663918527-0-250; _csrf=EHokb9_ak8apUmSMr0SbYM6Q; ConstructorioID_client_id=054ac361-c911-4db0-831c-a116e19561f7; ConstructorioID_session_id=1; _scid=4db1e1a2-f838-438b-8077-2c78f3b90f3d; _gcl_au=1.1.1639553116.1663918530; IR_gbd=flightclub.com; _gid=GA1.2.1343616897.1663918531; _sctr=1|1663866000000; __cf_bm=N_LTN.Xyu.tvdcRjxn_IHho8O471WLyiir2doDjn43U-1663919603-0-AeVANhX2hKdd9M2IFQ6Fw7SP2R2AiPnpU6NKRzDJzBPPsOOvJ6IjN1SIIqw18u1bVb5nPPbC93HFATe6M4BDIXw=; _gat_mpgaTracker1=1; _ga_GMJ0RMZHDX=GS1.1.1663918530.1.1.1663919641.0.0.0; _ga=GA1.1.1014569429.1663918531; IR_12612=1663919641964%7C0%7C1663919641964%7C%7C; ConstructorioID_session={\"sessionId\":1,\"lastTime\":1663919657436}; _xsrf=x5QVBx45-eNqqBU5TThzMS85b4FJfY5Z67Pw; OptanonConsent=isIABGlobal=false&datestamp=Fri+Sep+23+2022+14%3A54%3A17+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=6.14.0&hosts=&consentId=cb548e20-a594-46b3-88a6-bd4a7910b8b5&interactionCount=1&landingPath=https%3A%2F%2Fwww.flightclub.com%2Fcatalogsearch%2Fresult%3Fquery%3DYEEZY%2520SLIDES&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}


class Crawl1(scrapy.Spider):
    start_urls = ['https://dav.gov.vn']
    name = "dav_gov"
    headers = headers
    type = 'drug'

    def parse(self, response):
        # for page in range(1, 3):
        #     print("Page", page)
        #     link = f'https://danasilk.en.alibaba.com/productgrouplist-916210345-{page}/110_245cm.html?spm=a2700.shop_plgr.98.6'
        # link = f'https://dewangfangzhi.en.alibaba.com/search/product?SearchText=poncho'
        # yield scrapy.Request(link, headers=self.headers, callback=self.process_page)

        for page in range(1, 244):
            link = f'https://dav.gov.vn/tra-cuu-thuoc-page{page}.html'
            yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)

    # def process_page(self, response):
    #     links = response.xpath(
    #         "//div[@class='icbu-product-card vertical large product-item']/a/@href").extract()
    #     for link in links:
    #         yield scrapy.Request((f'https://{link}'), callback=self.saveFile)

    def saveFile(self, response):
        link = 'dav.gov.vn'
        item = DrugItem()
        # titles = response.xpath("//table[@class='table table-bordered']/tbody/tr/td[4]/text()").extract()
        titles = response.xpath("//table[@class='table table-bordered']/tbody/tr").extract()
        for idx, value in enumerate(titles):
            item['name'] = response.xpath(
                "//table[@class='table table-bordered']/tbody/tr[%s]/td[4]/text()" % (idx + 1)).extract()[0]
            item['drug_no'] = response.xpath(
                "//table[@class='table table-bordered']/tbody/tr[%s]/td[7]/text()" % (idx + 1)).extract()[0]
            item['source_link'] = link
            item['drug_base'] = None
            item['category'] = None
            item['effect'] = None
            item['type'] = self.type
            yield item
            # yield {
            #     "Title": i,
            # }


# class Crawl2(scrapy.Spider):
#     start_urls = ['https://drugbank.vn']
#     name = "drug_bank"
#     headers = headers
#     type = 'drug'
#
#     def parse(self, response):
#         # for page in range(1, 3):
#         #     print("Page", page)
#         #     link = f'https://danasilk.en.alibaba.com/productgrouplist-916210345-{page}/110_245cm.html?spm=a2700.shop_plgr.98.6'
#         # link = f'https://dewangfangzhi.en.alibaba.com/search/product?SearchText=poncho'
#         # yield scrapy.Request(link, headers=self.headers, callback=self.process_page)
#
#         for page in range(1, 512):
#             link = f'https://drugbank.vn/services/drugbank/api/public/thuoc?page={page}&size=20&isHide=ne(Yes)&sort=tenThuoc,asc&sort=id'
#             yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)
#
#     # def process_page(self, response):
#     #     links = response.xpath(
#     #         "//div[@class='icbu-product-card vertical large product-item']/a/@href").extract()
#     #     for link in links:
#     #         yield scrapy.Request((f'https://{link}'), callback=self.saveFile)
#
#     def saveFile(self, response):
#         link = 'drugbank.vn'
#         item = DrugItem()
#         products = json.loads(response.text)
#         for product in products:
#             item['name'] = product['tenThuoc'].strip()
#             item['source_link'] = link
#             item['type'] = self.type
#             yield item
#             # yield {
#             #     "Title": i,
#             # }
#
#
# class Crawl3(scrapy.Spider):
#     start_urls = ['https://dmec.moh.gov.vn']
#     headers = headers
#     name = "dmec"
#     type = 'medical_equipment'
#
#     def parse(self, response):
#
#         for page in range(1, 1312):
#             link = f'https://dmec.moh.gov.vn/cong-khai-phan-loai-ttbyt?p_p_id=vanbancongkhaipl_WAR_trangthietbiyteportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_vanbancongkhaipl_WAR_trangthietbiyteportlet_keyword=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_showHide=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_doanhNghiepPL=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_doanhNghiepDN=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_tenThietBi=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_mucDoRuiDo=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_trangThaiId=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_laThietBiTieuHao=-1&_vanbancongkhaipl_WAR_trangthietbiyteportlet_chungLoaiId=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_ngayGuiTu=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_ngayGuiDen=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_delta=75&_vanbancongkhaipl_WAR_trangthietbiyteportlet_keywords=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_advancedSearch=false&_vanbancongkhaipl_WAR_trangthietbiyteportlet_andOperator=true&_vanbancongkhaipl_WAR_trangthietbiyteportlet_resetCur=false&_vanbancongkhaipl_WAR_trangthietbiyteportlet_cur={page}'
#             yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)
#
#     def saveFile(self, response):
#         link = 'dmec.moh.gov.vn'
#         item = DrugItem()
#         titles = response.xpath("//table[@class='oep-table']/tr/td[2]/text()").extract()
#         for i in titles:
#             item['name'] = i.strip()
#             item['source_link'] = link
#             item['type'] = self.type
#             yield item
#             # yield {
#             #     "Title": i,
#             # }

#
class Crawl4(scrapy.Spider):
    start_urls = ['https://www.google.com.vn']
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Abp.Localization.CultureName=en'
    }
    name = "dichvucong"
    type = 'drug'

    def parse(self, response):
        for i in range(5):
            payload = json.dumps({
                "KichHoat": True,
                "SoDangKyThuoc": {},
                "maxResultCount": 10000,
                "skipCount": i * 10000,
                "sorting": None
            })
            link = "https://dichvucong.dav.gov.vn/api/services/app/soDangKy/GetAllPublicServerPaging"
            yield scrapy.Request(link, headers=self.headers, callback=self.saveFile, method='POST', body=payload)

    # for page in range(1, 1312):
    #     link = f'https://dmec.moh.gov.vn/cong-khai-phan-loai-ttbyt?p_p_id=vanbancongkhaipl_WAR_trangthietbiyteportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_vanbancongkhaipl_WAR_trangthietbiyteportlet_keyword=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_showHide=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_doanhNghiepPL=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_doanhNghiepDN=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_tenThietBi=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_mucDoRuiDo=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_trangThaiId=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_laThietBiTieuHao=-1&_vanbancongkhaipl_WAR_trangthietbiyteportlet_chungLoaiId=0&_vanbancongkhaipl_WAR_trangthietbiyteportlet_ngayGuiTu=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_ngayGuiDen=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_delta=75&_vanbancongkhaipl_WAR_trangthietbiyteportlet_keywords=&_vanbancongkhaipl_WAR_trangthietbiyteportlet_advancedSearch=false&_vanbancongkhaipl_WAR_trangthietbiyteportlet_andOperator=true&_vanbancongkhaipl_WAR_trangthietbiyteportlet_resetCur=false&_vanbancongkhaipl_WAR_trangthietbiyteportlet_cur={page}'
    #     yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)

    # def process_page(self, response):
    #     links = response.xpath(
    #         "//div[@class='icbu-product-card vertical large product-item']/a/@href").extract()
    #     for link in links:
    #         yield scrapy.Request((f'https://{link}'), callback=self.saveFile)

    def saveFile(self, response):
        link = 'dichvucong.dav.gov.vn'
        item = DrugItem()
        products = json.loads(response.text)['result']['items']
        for i in products:
            item['name'] = i['tenThuoc'].strip()
            item['drug_no'] = i['soDangKy'].strip()
            item['drug_base'] = i['thongTinThuocCoBan']['hoatChatChinh'].strip()
            item['category'] = None
            item['effect'] = None
            item['source_link'] = link
            item['type'] = self.type
            print('Connect dichvucong')
            yield item
            # yield {
            #     "Title": i,
            # }


#
#
class Crawl5(scrapy.Spider):
    start_urls = ['https://www.thuocbietduoc.com.vn']
    headers = headers
    name = "thuocbietduoc"
    type = 'drug'

    def parse(self, response):
        # for page in range(1, 3):
        #     print("Page", page)
        #     link = f'https://danasilk.en.alibaba.com/productgrouplist-916210345-{page}/110_245cm.html?spm=a2700.shop_plgr.98.6'
        # link = f'https://dewangfangzhi.en.alibaba.com/search/product?SearchText=poncho'
        # yield scrapy.Request(link, headers=self.headers, callback=self.process_page)
        # link= f'https://dichvucong.dav.gov.vn/congbothuoc/index'
        # yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)
        list_string = list(string.ascii_uppercase)
        for i in list_string:
            for j in list_string:
                for page in range(1, 301, 20):
                    link = f'https://www.thuocbietduoc.com.vn/defaults/drgsearch?act=DrugSearch&key={i}{j}&opt=TT&start={page}'
                    yield scrapy.Request(link, headers=self.headers, callback=self.process_page)

    def process_page(self, response):
        links = response.xpath(
            "//table[@id='dlstThuoc']/tr/td/table/tr[3]/td[2]/a/@href").extract()
        for link in links:
            link = link.replace('..', '')
            yield scrapy.Request((f'https://www.thuocbietduoc.com.vn/{link}'), callback=self.saveFile)

    def saveFile(self, response):
        link = 'thuocbietduoc.com.vn'
        item = DrugItem()
        item['name'] = response.xpath("/html/body/div[2]/div/div[1]/div[1]/div[3]/article/h1/text()").extract()[0]
        item['drug_no'] = response.xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div/span[@class='textdetaildrg']/text()").extract()[2]
        item['drug_base'] = response.xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div/div/span[@class='textdetaildrgI']").extract()[0]
        item['drug_base'] = re.sub(r'<.*?>', '', item['drug_base'])
        item['category'] = response.xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div[4]/span[2]").extract()[0]
        item['category'] = re.sub(r'<.*?>', '', item['category'])
        item['effect'] = response.xpath(
            "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div[@class='tbldrg_dt2']/section[@id='chi-dinh']/div") \
            .extract()[0]
        item['effect'] = re.sub(r'<.*?>', '', item['effect'])
        item['type'] = self.type
        item['source_link'] = link
        print('thuocbietduoc')
        yield item
        # for idx, value in enumerate(titles):
        #     if idx == 0 or idx == 21:
        #         continue
        #     item['name'] = \
        #         response.xpath("//table[@id='dlstThuoc']/tr[%s]/td/table/tr/td[2]/h2/a/text()" % (idx + 1)).extract()[
        #             0].replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').strip()
        #     item['drug_no'] = response.xpath(
        #         "//table[@id='dlstThuoc']/tr[%s]/td/table/tr[3]/td[4]/table/tr[6]/td[2]/text()" % (idx + 1)).extract()
        #     item['source_link'] = link
        #     item['drug_base'] = None
        #     item['category'] = response.xpath(
        #         "//table[@id='dlstThuoc']/tr[%s]/td/table/tr[3]/td[4]/table/tr[1]/td[2]/text()" % (idx + 1)).extract()[
        #         0].replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').strip()
        #     item['effect'] = None
        #     item['type'] = self.type


class Crawl6(scrapy.Spider):
    start_urls = ['https://hqmc-cbmp.ehealth.gov.vn:8002']
    headers = {
    "accept": "*/*",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8",
    "accept-encoding":"gzip,deflate,br",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    # "x-csrf-token": "x5QVBx45-eNqqBU5TThzMS85b4FJfY5Z67Pw",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "connection":"keep-alive"
}
    name = "hqmc-cbmp.ehealth"
    type = 'drug'


    def parse(self, response):
        payload = json.dumps({
            'dtid': 'z_qhb',
            'cmd_0': 'onPaging',
            'uuid_0': 'wOCQ02',
            'data_0': '{"":1}'
        })
        link = "https://hqmc-cbmp.ehealth.gov.vn:8002/zkau;jsessionid=C548FA1516ECA97A8E9409FEC49F8E92.jvm1"
        yield scrapy.Request(url=link, headers=self.headers, callback=self.saveFile, method='POST', body=payload)
        # for page in range(1, 244):
        #     link = f'https://dav.gov.vn/tra-cuu-thuoc-page{page}.html'
        #     yield scrapy.Request(link, headers=self.headers, callback=self.saveFile)

    # def process_page(self, response):
    #     links = response.xpath(
    #         "//div[@class='icbu-product-card vertical large product-item']/a/@href").extract()
    #     for link in links:
    #         yield scrapy.Request((f'https://{link}'), callback=self.saveFile)

    def saveFile(self, response):
        link = 'dav.gov.vn'
        item = DrugItem()
        # titles = response.xpath("//table[@class='table table-bordered']/tbody/tr/td[4]/text()").extract()
        titles = response.xpath("//table[@class='table table-bordered']/tbody/tr").extract()
        for idx, value in enumerate(titles):
            item['name'] = response.xpath(
                "//table[@class='table table-bordered']/tbody/tr[%s]/td[4]/text()" % (idx + 1)).extract()[0]
            item['drug_no'] = response.xpath(
                "//table[@class='table table-bordered']/tbody/tr[%s]/td[7]/text()" % (idx + 1)).extract()[0]
            item['source_link'] = link
            item['drug_base'] = None
            item['category'] = None
            item['effect'] = None
            item['type'] = self.type
            yield item 