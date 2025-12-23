"""
数据模型定义
使用 dataclass 定义测试用例和配置结构，提高类型安全
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List


@dataclass
class ServerConfig:
    """服务器配置"""
    gate_address: str
    login_url: str


@dataclass
class GitConfig:
    """Git配置"""
    repository: str
    branch: str
    local_path: str
    read_only: bool = True


@dataclass
class TestConfig:
    """测试配置"""
    output_dir: str = "generated_tests"
    report_dir: str = "reports"
    timeout: int = 30


@dataclass
class AppConfig:
    """应用配置"""
    servers: ServerConfig
    git: GitConfig
    services: Dict[str, Dict[str, str]]
    test: TestConfig = field(default_factory=TestConfig)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """从字典创建配置"""
        return cls(
            servers=ServerConfig(**data.get('servers', {})),
            git=GitConfig(**data.get('jinn_server', {})),
            services=data.get('services', {}),
            test=TestConfig(**data.get('test', {}))
        )
    
    def validate(self) -> bool:
        """验证配置有效性"""
        if not self.servers.gate_address:
            raise ValueError("Gate服务器地址不能为空")
        if not self.servers.login_url:
            raise ValueError("Login服务器URL不能为空")
        if not self.git.repository:
            raise ValueError("Git仓库地址不能为空")
        return True


@dataclass
class TestCase:
    """测试用例数据类"""
    case_id: str
    title: str
    priority: str
    preconditions: str
    dimension: str
    method_name: str
    method_url: str
    headers: str
    request_body: str
    expected_status: str
    expected_response: str
    jsonpath_assertion: str
    remark: str
    status: str = "未测试"
    error_message: str = ""
    actual_response: str = ""
    abnormal_type: Optional[str] = None
    server_error: str = ""
    possible_issues: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """从字典创建"""
        # 过滤掉 None 值，使用默认值
        filtered_data = {k: v for k, v in data.items() if v is not None}
        return cls(**filtered_data)

