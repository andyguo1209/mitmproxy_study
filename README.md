以下说明均参考官网【https://docs.mitmproxy.org/stable/addons-events/】

主题
   修改request或者response内容

介绍
  mitmdump无交互界面的命令，与python脚本对接，来源于mitmproxy支持inline script，这里的script指的是python脚本，inline script提供了http、Websocket、tcp等各个时间点事件（events）的hook函数，如http中的request、response等

主要events一览表
   需要修改各种事件内容时，重写以下对应方法，这里主要用的是request、response方法

针对http，常用的API
#http.HTTPFlow 实例 flow
flow.request.headers #获取所有头信息，包含Host、User-Agent、Content-type等字段
flow.request.url #完整的请求地址，包含域名及请求参数，但是不包含放在body里面的请求参数
flow.request.pretty_url #同flow.request.url目前没看出什么差别
flow.request.host #域名
flow.request.method #请求方式。POST、GET等
flow.request.scheme #什么请求 ，如https
flow.request.path # 请求的路径，url除域名之外的内容
flow.request.get_text() #请求中body内容，有一些http会把请求参数放在body里面，那么可通过此方法获取，返回字典类型
flow.request.query #返回MultiDictView类型的数据，url直接带的键值参数
flow.request.get_content()#bytes,结果如flow.request.get_text()
flow.request.raw_content #bytes,结果如flow.request.get_content()
flow.request.urlencoded_form #MultiDictView，content-type：application/x-www-form-urlencoded时的请求参数，不包含url直接带的键值参数
flow.request.multipart_form #MultiDictView，content-type：multipart/form-data
时的请求参数，不包含url直接带的键值参数
#以上均为获取request信息的一些常用方法，对于response，同理
flow.response.status_code #状态码
flow.response.text#返回内容，已解码
flow.response.content #返回内容，二进制
flow.response.setText()#修改返回内容，不需要转码
#以上为不完全列举
示例
#修改response内容，这里是服务器已经有返回了结果，再更改，也可以做不经过服务器处理，直接返回，看需求
def response(flow:http.HTTPFlow)-> None:
    #特定接口需要返回1001结果
    interface_list=["page/**"] #由于涉及公司隐私问题，隐藏实际的接口

    url_path=flow.request.path
    if  url_path.split("?")[0] in  interface_list:
        ctx.log.info("#"*50)
        ctx.log.info("待修改路径的内容："+url_path)
        ctx.log.info("修改成：1001错误返回")
        ctx.log.info("修改前：\n")
        ctx.log.info(flow.response.text)
        flow.response.set_text(json.dumps({"result":"1001","message":"服务异常"}))#修改，使用set_text不用转码
        ctx.log.info("修改后：\n")
        ctx.log.info(flow.response.text)
        ctx.log.info("#"*50)
    elif  flow.request.host in  host_list:#host_list 域名列表，作为全局变量，公司有多个域名，也隐藏
        ctx.log.info("response= "+flow.response.text)
应用
   移动app测试中，为了测试app的容错能力，在不改动数据库或者折腾服务器的情况下，脚本修改request或者response内容【这里也可以选择第三方工具，如fiddler同样支持，看个人需求】，查看app的表现；亦或是根据接口定义检查app的接口请求情况
