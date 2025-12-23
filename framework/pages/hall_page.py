"""
Hall Page - Hall服务页面对象
"""
from typing import Dict, Any, Optional
from .base_page import BasePage


class HallPage(BasePage):
    """Hall服务页面对象"""
    
    def __init__(self, client):
        super().__init__(client, 'Hall')
    
    def fetch_self_full_user_info(self, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取自己的完整用户信息"""
        if request_data is None:
            request_data = {}
        return self.call_api('FetchSelfFullUserInfo', request_data)
    
    def fetch_simple_user_info(self, target_uid: int = None, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取简单用户信息"""
        if request_data is None:
            request_data = {}
        if target_uid is not None:
            request_data['target_uid'] = target_uid
        return self.call_api('FetchSimpleUserInfo', request_data)
    
    def update_nickname(self, nickname: str, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """更新昵称"""
        if request_data is None:
            request_data = {}
        request_data['nickname'] = nickname
        return self.call_api('UpdateNickname', request_data)
    
    def sell_item(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """出售物品"""
        return self.call_api('SellItem', request_data)
    
    def buy_item(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """购买物品"""
        return self.call_api('BuyItem', request_data)
    
    def stash_to_backpack(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """从仓库移动到背包"""
        return self.call_api('StashToBackpack', request_data)
    
    def backpack_to_stash(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """从背包移动到仓库"""
        return self.call_api('BackpackToStash', request_data)
    
    def exchange_backpack_item(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """交换背包物品"""
        return self.call_api('ExchangeBackpackItem', request_data)
    
    def debug_add_cash(self, amount: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """调试：添加现金"""
        if request_data is None:
            request_data = {}
        request_data['amount'] = amount
        return self.call_api('DebugAddCash', request_data)
    
    def debug_add_item(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """调试：添加物品"""
        return self.call_api('DebugAddItem', request_data)
    
    def get_current_uid(self) -> Optional[int]:
        """获取当前用户UID"""
        result = self.fetch_self_full_user_info()
        if self.is_success(result):
            response = self.get_response(result)
            if 'fetchselffulluserinfo' in response:
                full_info = response['fetchselffulluserinfo']
                if 'full_user_info' in full_info:
                    return full_info['full_user_info'].get('uid')
        return self.client.uid if self.client.uid else None



