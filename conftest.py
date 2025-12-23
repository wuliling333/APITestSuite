"""
pytest配置文件 - 提供全局fixtures
"""
import pytest
import sys
import os

# 添加框架路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework.client import APIClient
from framework.config import Config
from framework.pages import HallPage, RoomPage, SocialPage


@pytest.fixture(scope="session")
def config():
    """配置fixture"""
    return Config()


@pytest.fixture(scope="session")
def api_client(config):
    """API客户端fixture（会话级别，所有测试共享）"""
    client = APIClient(config)
    
    # 登录
    if not client.login():
        pytest.fail("登录失败")
    
    # 连接Gate
    if not client.connect_gate():
        pytest.fail("Gate连接失败")
    
    yield client
    
    # 清理
    client.close()


@pytest.fixture(scope="session")
def hall_page(api_client):
    """Hall页面对象fixture"""
    return HallPage(api_client)


@pytest.fixture(scope="session")
def room_page(api_client):
    """Room页面对象fixture"""
    return RoomPage(api_client)


@pytest.fixture(scope="session")
def social_page(api_client):
    """Social页面对象fixture"""
    return SocialPage(api_client)


@pytest.fixture(scope="session")
def current_uid(hall_page):
    """获取当前用户UID"""
    result = hall_page.fetch_self_full_user_info()
    if hall_page.is_success(result):
        response = hall_page.get_response(result)
        if 'fetchselffulluserinfo' in response:
            full_info = response['fetchselffulluserinfo']
            if 'full_user_info' in full_info:
                return full_info['full_user_info'].get('uid')
    return hall_page.client.uid if hall_page.client.uid else None



