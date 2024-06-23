
import pytest
import requests
from datetime import datetime, timedelta
data = {}

def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == 'call':
        print('本次用例的执行结果',report.outcome)

def pytest_collection_finish(session: pytest.Session):
    #用例加载完成之后,包含了全部的用例
    data['total'] = len(session.items)
    print('用例的总数:',data['total'])

def pytest_configure():
    #配置加载完毕之后,测试用例执行之前执行
    data['startTime'] = datetime.now()
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

    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c45b1cc7-42af-479b-9ca6-14ff0146479d'

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
    requests.post(url,
                  json={
                      "msgtype": "markdown",
                      "markdown": {
                          "content": content
                      }}
                  )
