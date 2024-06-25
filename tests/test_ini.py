import pytest
from pathlib import Path
from pythonproject1 import plugin

pytest_plugins = 'pytester' #我是测试开发

@pytest.fixture(autouse=True)
def mock():
    back_data = plugin.data #将初始data保存
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }

    #创建一个干净的测试环境
    yield
    #恢复测试环境
    plugin.data = back_data


@pytest.mark.parametrize(
    'send_when',
    ['every','on_fail']
)
def test_send_when(send_when,pytester:pytest.Pytester,tmp_path:Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = {send_when}
send_api = https://baidu.com
    """)

    #断言判断配置是否加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini('send_when') == send_when

    pytester.makepyfile( #构造场景,这是一个测试用例
        ...
    )
    pytester.runpytest("-c",str(config_path)) #调用运行该测试用例

    print(plugin.data)
    if send_when == 'every':
        assert plugin.data['send_done'] == 1
    else:
        assert plugin.data.get('send_done') is None

@pytest.mark.parametrize(
    'send_api',
    ['http://baidu.com','']
)
def test_send_api(send_api,pytester:pytest.Pytester,tmp_path:Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(f"""
[pytest]
send_when = every
send_api = {send_api}
        """)

    # 断言判断配置是否加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini('send_when') == send_when

    pytester.makepyfile(  # 构造场景,这是一个测试用例
        ...
    )
    pytester.runpytest("-c", str(config_path))  # 调用运行该测试用例

    print(plugin.data)
    if send_api:
        assert plugin.data['send_done'] == 1
    else:
        assert plugin.data.get('send_done') is None

