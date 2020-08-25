#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2020/8/25 下午1:22
#@Author : guozhenhua
#@Site : 
#@File : get_data.py
#@Software: PyCharm
#获取respoene的数据保存到本地

from mitmproxy import ctx

class Counter:

    def __init__(self):
        self.num = 0



    def request(self, flow):
        if (flow.request.url).find("mp4") != -1:
            ctx.log.info("request_url= " +flow.request.url)
            file_name = open('miliy.txt', 'a+', encoding='utf-8')

            file_name.write(str(self.num)+" "+flow.request.url)
            file_name.write("\r\n")
            file_name.close()
            ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow):
        if (flow.request.url).find("homepage/index") != -1:
            self.num = self.num + 1
            ctx.log.info("response= " + flow.response.text)
            file_name = open('miliy.txt', 'a+', encoding='utf-8')
            file_name.write(str(self.num)+" "+flow.response.text)
            file_name.write("\r\n")
            file_name.close()
            ctx.log.info("We've seen %d flows" % self.num)




addons = [
    Counter()
]
