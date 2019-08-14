# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bossgo.items import BossgoItem


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101280100-p100116/?query=go&page=1&ka=page-1']

    rules = (
        Rule(LinkExtractor(allow=r'.+\?query=go&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+job_detail/.+'),callback="parse_job", follow=False),
    )

    def parse_job(self, response):
        title = response.xpath("//div[@class='name']/h1/text()").get()
        salary = response.xpath("//div[@class='name']/span/text()").get()
        job_infos = response.xpath("//div[@class='job-banner']//div[@class='info-primary']/p//text()").getall()
        city = job_infos[0]
        work_years = job_infos[1]
        education = job_infos[2]
        company = response.xpath("//div[@class='sider-company']/div[@class='company-info']//text()").getall()
        company = "".join(company).strip()
        desc = response.xpath("//div[@class='job-sec']/div[@class='text']/text()").getall()
        desc = "".join(desc).strip()
        item = BossgoItem(title=title, salary=salary, city=city, work_years=work_years, education=education,company=company, desc=desc)
        yield item
