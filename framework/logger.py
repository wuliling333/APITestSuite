"""
框架日志管理器
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class FrameworkLogger:
    """框架日志管理器"""
    
    _instance: Optional['FrameworkLogger'] = None
    _initialized = False
    
    def __new__(cls, log_file: str = "api_test.log", level: str = "INFO"):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_file: str = "api_test.log", level: str = "INFO"):
        """初始化日志管理器"""
        if FrameworkLogger._initialized:
            return
        
        self.log_file = log_file
        self.level = level
        self.logger = logging.getLogger("APITestSuite")
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
            self.logger.propagate = False
            
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else "."
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # 文件处理器（带轮转）
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter(
                '%(levelname)s - %(message)s'
            ))
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        FrameworkLogger._initialized = True
    
    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """记录信息"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录警告"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录错误"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """记录异常（包含堆栈信息）"""
        self.logger.exception(message)


# 创建全局日志实例
logger = FrameworkLogger()

