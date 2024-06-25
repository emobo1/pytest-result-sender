
import pytest
import requests
from datetime import datetime, timedelta
data = {
    "passed" : 0,
    "failed" : 0,
}

def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == 'call':
        print('本次用例的执行结果',report.outcome)



def pytest_collection_finish(session: pytest.Session):
    #用例加载完成之后,包含了全部的用例
    data['total'] = len(session.items)
    print('用例的总数:',data['total'])

def pytest_configure(config:pytest.Config):
    #配置加载完毕之后,测试用例执行之前执行
    data['startTime'] = datetime.now()
    data['send_when'] = config.getinit("send_when")
    data['send_api'] = config.getinit("send_api")
    print(f"{datetime.now()} pytest开始执行")

def pytest_unconfigure():
    #配置加载完毕之后运行,所有测试用例执行后执行
    data['endTime'] = datetime.now()
    print(f"{datetime.now()} pytest结束执行")

    data['duration'] = data['endTime'] - data['startTime']
    data['passed_rate'] = data['passed'] / data['total'] * 100
    print(data)
    # assert timedelta(seconds=3) > data['duration'] >= timedelta(seconds=2.5)
    # assert data['total'] == 3
    # assert data['passed'] == 2
    # assert data['failed'] == 1
    # assert data['passed_rate'] == 0

    #集成测试
    send_result
def send_result(result):
    if data['send_when'] == 'on_fail' and data['failed'] == 0:
        #配置了失败才发送,但是如果没有失败,则不发送
        return

    if not data['send_api']:
        #如果没有配置发送地址,不发送
        return

    url = data['send_api'] #动态发送到指定位置

    content = f"""
    pytest自动化测试结果

    测试时间: {data['endTime']}<br/>
    用例数量: {data['total']} <br/>
    执行时长: 50s <br/>
    测试通过: 2
    测试失败: 1
    测试通过率: 

    测试报告地址: http://baidu.com
    """

    #家try-catch如果遇到发送地址有错,或着拒绝了请求,那么抛出异常,不发送
    try :
        requests.post(url,
                  json={
                      "msgtype": "markdown",
                      "markdown": {
                          "content": content
                      }}
                  )
    except Exception:
        pass

    data['send_done'] = 1 #发送成功执行