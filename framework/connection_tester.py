"""
连接测试器 - 测试Gate和Login服务器连接
"""
import socket
import requests
from framework.config import Config


class ConnectionTester:
    """连接测试器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.gate_address = config.get_gate_address()
        self.login_url = config.get_login_url()
    
    def test_all_connections(self) -> bool:
        """测试所有服务器连接"""
        print("=" * 80)
        print("测试服务器连接...")
        print("=" * 80)
        
        gate_ok = self.test_gate()
        login_ok = self.test_login()
        
        if gate_ok and login_ok:
            print("✓ 所有服务器连接正常")
            return True
        else:
            print("✗ 部分服务器连接失败")
            return False
    
    def test_gate(self) -> bool:
        """测试Gate服务器连接"""
        print(f"\n测试Gate服务器: {self.gate_address}")
        try:
            host, port = self.gate_address.split(':')
            port = int(port)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✓ Gate服务器连接成功")
                return True
            else:
                print(f"✗ Gate服务器连接失败: 无法连接到 {host}:{port}")
                return False
        except Exception as e:
            print(f"✗ Gate服务器连接失败: {e}")
            return False
    
    def test_login(self) -> bool:
        """测试Login服务器连接"""
        print(f"\n测试Login服务器: {self.login_url}")
        try:
            response = requests.get(self.login_url, timeout=5)
            print(f"✓ Login服务器连接成功 (状态码: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Login服务器连接失败: {e}")
            return False

