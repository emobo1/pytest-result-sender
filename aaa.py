'''
调用接口调用群机器人
'''
import requests

url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c45b1cc7-42af-479b-9ca6-14ff0146479d'

content = """
pytest自动化测试结果

测试时间: XXX-XXXX-XX<br/>
用例数量: 100 <br/>
执行时长: 50s <br/>
测试通过: 2
测试失败: 1
测试通过率: 

测试报告地址: http://baidu.com
"""
requests.post(url,
              json={
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }}
              )