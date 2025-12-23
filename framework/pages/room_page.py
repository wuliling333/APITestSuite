"""
Room Page - Room服务页面对象
"""
from typing import Dict, Any, Optional
from .base_page import BasePage


class RoomPage(BasePage):
    """Room服务页面对象"""
    
    def __init__(self, client):
        super().__init__(client, 'Room')
    
    def get_user_state(self, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取用户状态"""
        if request_data is None:
            request_data = {}
        return self.call_api('GetUserState', request_data)
    
    def create_team(self, game_mode: int = 1, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """创建队伍"""
        if request_data is None:
            request_data = {}
        request_data['game_mode'] = game_mode
        return self.call_api('CreateTeam', request_data)
    
    def join_team(self, team_id: int = None, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """加入队伍"""
        if request_data is None:
            request_data = {}
        if team_id is not None:
            request_data['team_id'] = team_id
        return self.call_api('JoinTeam', request_data)
    
    def leave_team(self, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """离开队伍"""
        if request_data is None:
            request_data = {}
        return self.call_api('LeaveTeam', request_data)
    
    def get_team_info(self, team_id: int = None, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取队伍信息"""
        if request_data is None:
            request_data = {}
        if team_id is not None:
            request_data['team_id'] = team_id
        return self.call_api('GetTeamInfo', request_data)
    
    def change_ready_state(self, ready: bool = True, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """改变准备状态"""
        if request_data is None:
            request_data = {}
        request_data['ready'] = ready
        return self.call_api('ChangeReadyState', request_data)
    
    def start_game_from_team(self, team_id: int = None, map_id: int = 1, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """从队伍开始游戏"""
        if request_data is None:
            request_data = {}
        if team_id is not None:
            request_data['team_id'] = team_id
        request_data['map_id'] = map_id
        return self.call_api('StartGameFromTeam', request_data)
    
    def match(self, map_id: int = 1, difficulty: int = 1, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """匹配"""
        if request_data is None:
            request_data = {}
        request_data['map_id'] = map_id
        request_data['difficulty'] = difficulty
        return self.call_api('Match', request_data)
    
    def cancel_match(self, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """取消匹配"""
        if request_data is None:
            request_data = {}
        return self.call_api('CancelMatch', request_data)
    
    def get_game_info(self, game_id: int = None, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取游戏信息"""
        if request_data is None:
            request_data = {}
        if game_id is not None:
            request_data['game_id'] = game_id
        return self.call_api('GetGameInfo', request_data)
    
    def get_team_id_from_state(self) -> Optional[int]:
        """从用户状态获取team_id"""
        result = self.get_user_state()
        if self.is_success(result):
            response = self.get_response(result)
            if 'getuserstate' in response:
                state = response['getuserstate']
                return state.get('team_id')
        return None
    
    def get_game_id_from_state(self) -> Optional[int]:
        """从用户状态获取game_id"""
        result = self.get_user_state()
        if self.is_success(result):
            response = self.get_response(result)
            if 'getuserstate' in response:
                state = response['getuserstate']
                return state.get('game_id')
        return None



