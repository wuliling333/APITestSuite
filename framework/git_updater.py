"""
Git更新器 - 负责克隆和更新jinn_server仓库
"""
import os
import subprocess
import shutil
from typing import Tuple, Set
from framework.config import Config


class GitUpdater:
    """Git更新器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.repo_path = config.get_jinn_server_path()
        self.repo_url = config.get_jinn_server_repo_url()
        self.branch = config.get_jinn_server_branch()
    
    def check_and_update(self) -> Tuple[bool, Set[str]]:
        """
        检查并更新仓库
        返回: (是否有更新, 新接口集合)
        """
        print("=" * 80)
        print("检查Git仓库更新...")
        print("=" * 80)
        
        if not os.path.exists(self.repo_path):
            print(f"仓库不存在，开始克隆 {self.repo_url}...")
            self._clone_repo()
        else:
            print(f"仓库已存在，检查更新...")
            self._pull_update()
        
        print("✓ Git更新完成")
        
        # 检测新接口（这里先返回空集合，后续实现）
        new_interfaces = set()
        return True, new_interfaces
    
    def _clone_repo(self):
        """克隆仓库"""
        try:
            cmd = [
                'git', 'clone',
                '-b', self.branch,
                '--depth', '1',
                self.repo_url,
                self.repo_path
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ 仓库克隆成功: {self.repo_path}")
            
            # 初始化并更新子模块
            self._update_submodules()
        except subprocess.CalledProcessError as e:
            print(f"✗ 克隆失败: {e.stderr}")
            raise
    
    def _pull_update(self):
        """拉取更新"""
        try:
            # 先fetch
            cmd = ['git', 'fetch', 'origin', self.branch]
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, text=True)
            
            # 然后reset到最新
            cmd = ['git', 'reset', '--hard', f'origin/{self.branch}']
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, text=True)
            
            print(f"✓ 仓库更新成功")
            
            # 更新子模块
            self._update_submodules()
        except subprocess.CalledProcessError as e:
            print(f"✗ 更新失败: {e.stderr}")
            raise
    
    def _update_submodules(self):
        """更新子模块"""
        try:
            print("更新Git子模块...")
            cmd = ['git', 'submodule', 'update', '--init', '--recursive']
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, text=True)
            print("✓ 子模块更新成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠ 子模块更新失败: {e.stderr}")
            # 子模块更新失败不影响主流程

