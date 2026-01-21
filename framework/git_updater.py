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
            print(f"正在克隆仓库（浅克隆，只拉取最新代码）...")
            cmd = [
                'git', 'clone',
                '-b', self.branch,
                '--depth', '1',
                '--single-branch',
                self.repo_url,
                self.repo_path
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
            print(f"✓ 仓库克隆成功: {self.repo_path}")
            
            # 初始化并更新子模块（可选，首次克隆时可能需要）
            # 如果只需要proto文件，可以跳过子模块
            print("提示: 跳过子模块初始化（如果只需要proto文件）")
            # self._update_submodules()  # 注释掉以加快速度
        except subprocess.TimeoutExpired:
            print("✗ 克隆超时（超过5分钟），请检查网络连接")
            raise
        except subprocess.CalledProcessError as e:
            print(f"✗ 克隆失败: {e.stderr}")
            raise
    
    def _pull_update(self):
        """拉取更新"""
        try:
            # 检查是否有更新（快速检查）
            print("检查远程更新...")
            cmd = ['git', 'fetch', '--dry-run', 'origin', self.branch]
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
            
            # 如果输出为空，说明没有更新
            if not result.stdout.strip() and not result.stderr.strip():
                print("✓ 仓库已是最新，无需更新")
                return
            
            # 有更新，执行拉取
            print("发现更新，开始拉取...")
            cmd = ['git', 'fetch', 'origin', self.branch]
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, text=True)
            
            # 然后reset到最新
            cmd = ['git', 'reset', '--hard', f'origin/{self.branch}']
            subprocess.run(cmd, cwd=self.repo_path, check=True, capture_output=True, text=True)
            
            print(f"✓ 仓库更新成功")
            
            # 更新子模块（可选，如果子模块很多可以跳过）
            self._update_submodules()
        except subprocess.CalledProcessError as e:
            print(f"✗ 更新失败: {e.stderr}")
            raise
    
    def _update_submodules(self):
        """更新子模块（快速模式，只更新已初始化的子模块）"""
        try:
            # 检查是否有子模块
            cmd = ['git', 'submodule', 'status']
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
            
            if not result.stdout.strip():
                # 没有子模块，跳过
                return
            
            print("更新Git子模块（快速模式）...")
            # 使用 --remote 和 --merge 快速更新，不递归初始化所有子模块
            # 只更新已存在的子模块
            cmd = ['git', 'submodule', 'update', '--remote', '--merge']
            subprocess.run(cmd, cwd=self.repo_path, check=False, capture_output=True, text=True, timeout=60)
            print("✓ 子模块更新完成")
        except subprocess.TimeoutExpired:
            print("⚠ 子模块更新超时，跳过（不影响主流程）")
        except subprocess.CalledProcessError as e:
            print(f"⚠ 子模块更新失败: {e.stderr}")
            print("  提示: 子模块更新失败不影响主流程，可以继续使用")
        except Exception as e:
            print(f"⚠ 子模块更新异常: {e}")
            print("  提示: 子模块更新失败不影响主流程，可以继续使用")

