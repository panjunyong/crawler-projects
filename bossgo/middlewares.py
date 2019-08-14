# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from twisted.internet.defer import DeferredLock
import requests
import json
from bossgo.models import ProxyModle


class BossgoSpiderMiddleware(object):
    pass


class GoBossUserAgentDownloadMiddleware(object):
    USER_AGENT = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36'
    ]

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENT)
        request.headers['User-Agent'] = user_agent

class IPProxyDownloadMiddleware(object):
    PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

    def __init__(self):
        super(IPProxyDownloadMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self,request,spider):
        if "proxy" not in request.meta or self.current_proxy.is_expiring:
            self.update_proxy()
        request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self,request,response,spider):
        if response.status != 200 or "captcha" in response.url:
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print("这个代理被拉了黑名单：%s" %self.current_proxy)
            self.update_proxy()
            return request
        return response

    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print("重新获取一个代理：",text)
            result = json.loads(text)
            if len(result['data']) > 0:
                data = result['data'][0]
                proxy_model = ProxyModle(data)
                self.current_proxy = proxy_model
        self.lock.release()

