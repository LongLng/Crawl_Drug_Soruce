# -*- coding: utf-8 -*-
# coding=utf-8
import sys

from scrapy import cmdline
from spiders.drug import Crawl6
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# cron_job= */10 * * * * /usr/bin/python3 /home/longlng/scrapy_drug/drug/main.py >> /home/longlng/scrapy_drug/cron.log 2>&1
def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    # process.crawl(Crawl1)
    # process.crawl(Crawl2)
    # process.crawl(Crawl3)
    # process.crawl(Crawl4)
    process.crawl(Crawl6)
    process.start()
    # if name:
    #     cmdline.execute(name.split())


if __name__ == '__main__':
    print('begin main')
    # name = "scrapy crawl dav_gov -O data/dav_gov.csv"
    name = "scrapy crawl drug"
    # main(name)
    main()
    print('exit')
