# import re
# import string
# import requests
# import scrapy
# from scrapy.http import Request
# import os
# import scrapy
# from items import DrugItem
# import time
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# import json
# import mysql.connector
# # from _condata import data_readed
#
# headers = {
#     "accept": "*/*",
#     "accept-language": "vi,en-US;q=0.9,en;q=0.8",
#     "content-type": "application/json",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-csrf-token": "x5QVBx45-eNqqBU5TThzMS85b4FJfY5Z67Pw",
#     "cookie": "cf_chl_2=06d1f7a6cfeb2b1; cf_chl_prog=x15; cf_clearance=HbcESmswj3STAru.rnighD5taOb1WmtPpdiS741bssI-1663918527-0-250; _csrf=EHokb9_ak8apUmSMr0SbYM6Q; ConstructorioID_client_id=054ac361-c911-4db0-831c-a116e19561f7; ConstructorioID_session_id=1; _scid=4db1e1a2-f838-438b-8077-2c78f3b90f3d; _gcl_au=1.1.1639553116.1663918530; IR_gbd=flightclub.com; _gid=GA1.2.1343616897.1663918531; _sctr=1|1663866000000; __cf_bm=N_LTN.Xyu.tvdcRjxn_IHho8O471WLyiir2doDjn43U-1663919603-0-AeVANhX2hKdd9M2IFQ6Fw7SP2R2AiPnpU6NKRzDJzBPPsOOvJ6IjN1SIIqw18u1bVb5nPPbC93HFATe6M4BDIXw=; _gat_mpgaTracker1=1; _ga_GMJ0RMZHDX=GS1.1.1663918530.1.1.1663919641.0.0.0; _ga=GA1.1.1014569429.1663918531; IR_12612=1663919641964%7C0%7C1663919641964%7C%7C; ConstructorioID_session={\"sessionId\":1,\"lastTime\":1663919657436}; _xsrf=x5QVBx45-eNqqBU5TThzMS85b4FJfY5Z67Pw; OptanonConsent=isIABGlobal=false&datestamp=Fri+Sep+23+2022+14%3A54%3A17+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=6.14.0&hosts=&consentId=cb548e20-a594-46b3-88a6-bd4a7910b8b5&interactionCount=1&landingPath=https%3A%2F%2Fwww.flightclub.com%2Fcatalogsearch%2Fresult%3Fquery%3DYEEZY%2520SLIDES&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1",
#     "Referrer-Policy": "strict-origin-when-cross-origin"
# }
#
#
# class Crawl5(scrapy.Spider):
#     start_urls = ['https://www.thuocbietduoc.com.vn']
#     headers = headers
#     name = "thuocbietduoc"
#     type = 'drug'
#     mysql_search = ''
#     urls = "data_readed()"
#     drug_no = None
#
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super(Crawl5, self).__init__(*args, **kwargs)
#     #     self.mysql_pipeline = MysqlPipeline(db_params={
#     #         'host': host,
#     #         'user': user,
#     #         'password': password,
#     #         'database': database,
#     #         'port': port,
#     #     })
#
#     def parse(self, response):
#         for i in self.urls:
#             drug_no = i[3].split(',')
#             # if len(drug_no) > 2:
#             print('DRUG_NO', drug_no)
#             print('DRUG_NO[0]', drug_no[0])
#             link = f'https://www.thuocbietduoc.com.vn/defaults/drgsearch?act=DrugSearch&key={drug_no[0]}&opt=DK'
#             yield scrapy.Request(link, headers=self.headers, callback=self.process_page,
#                                  cb_kwargs=dict(drug_no=drug_no[0], id=i[0]))
#         # link = f'https://www.thuocbietduoc.com.vn/defaults/drgsearch?act=DrugSearch&key=VD-26514-17&opt=DK'
#         # yield scrapy.Request(link, headers=self.headers, callback=self.process_page,
#         #                      cb_kwargs=dict(drug_no='VD-26514-17', id=3))
#
#     def process_page(self, response, drug_no, id):
#         links = response.xpath(
#             "//table[@id='dlstThuoc']/tr/td/table/tr[3]/td[2]/a/@href").extract()
#         drug_no_search = response.xpath(
#             "//table[@id='dlstThuoc']/tr/td/table/tr[3]/td[4]/table/tr[6]/td[2]/text()").extract()
#         try:
#             drug_category = response.xpath(
#                 "//table[@id='dlstThuoc']/tr/td/table/tr[3]/td[4]/table/tr[1]/td[2]/text()").extract()[0].replace('\r',
#                                                                                                                   '').replace(
#                 '\t', '').replace('\n', '')
#         except:
#             drug_category = None
#         for idx, link in enumerate(links):
#             link = link.replace('..', '')
#             if drug_no != drug_no_search[idx]:
#                 continue
#             yield scrapy.Request((f'https://www.thuocbietduoc.com.vn/{link}'), callback=self.saveFile,
#                                  cb_kwargs=dict(id=id, id_res=drug_no, drug_category=drug_category))
#
#     def saveFile(self, response, id, id_res, drug_category):
#         link = 'thuocbietduoc.com.vn'
#         item = DrugItem()
#         item['id'] = id
#         item['id_res'] = id_res
#         try:
#             item['drug_no'] = response.xpath(
#                 "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div/span[@class='textdetaildrg']/text()").extract()[
#                 2]
#         except:
#             item['drug_no'] = None
#         try:
#             item['drug_base'] = response.xpath(
#                 "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div/div/span[@class='textdetaildrgI']").extract()[0]
#             item['drug_base'] = re.sub(r'<.*?>', '', item['drug_base'])
#         except:
#             item['drug_base'] = None
#         try:
#             item['category'] = drug_category
#         except:
#             item['category'] = None
#         # item['category'] = response.xpath(
#         #     "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div[4]/span[2]").extract()[0]
#         # item['category'] = re.sub(r'<.*?>', '', item['category'])
#         try:
#             item['effect'] = response.xpath(
#                 "/html/body/div[2]/div/div[1]/div[1]/div[3]/article/div[@class='tbldrg_dt2']/section[@id='chi-dinh']/div") \
#                 .extract()[0]
#             item['effect'] = re.sub(r'<.*?>', '', item['effect'])
#         except:
#             item['effect'] = None
#         item['type'] = self.type
#         item['source_link'] = link
#         yield item
