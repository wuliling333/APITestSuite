"""
Social Page - Social服务页面对象
"""
from typing import Dict, Any, Optional, Tuple
from .base_page import BasePage


class SocialPage(BasePage):
    """Social服务页面对象"""
    
    def __init__(self, client):
        super().__init__(client, 'Social')
    
    def send_message(self, content: Dict[str, Any], to_uid: int = 0, scene: int = 4, scene_id: int = 0, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送消息"""
        if request_data is None:
            request_data = {}
        request_data['to_uid'] = to_uid
        request_data['scene'] = scene
        request_data['scene_id'] = scene_id
        request_data['content'] = content
        return self.call_api('SendMessage', request_data)
    
    def pull_msgs(self, conv_id: str, start_seq: int = 0, count: int = 20, reverse: bool = False, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """拉取消息"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['start_seq'] = start_seq
        request_data['count'] = count
        request_data['reverse'] = reverse
        return self.call_api('PullMsgs', request_data)
    
    def revoke_msg(self, conv_id: str, seq: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """撤回消息"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['seq'] = seq
        return self.call_api('RevokeMsg', request_data)
    
    def delete_msg(self, conv_id: str, seqs: list, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """删除消息"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['seqs'] = seqs
        return self.call_api('DeleteMsg', request_data)
    
    def add_reaction(self, conv_id: str, seq: int, reaction_id: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """添加反应"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['seq'] = seq
        request_data['reaction_id'] = reaction_id
        return self.call_api('AddReaction', request_data)
    
    def remove_reaction(self, conv_id: str, seq: int, reaction_id: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """移除反应"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['seq'] = seq
        request_data['reaction_id'] = reaction_id
        return self.call_api('RemoveReaction', request_data)
    
    def get_reactions(self, conv_id: str, seq: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取反应"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['seq'] = seq
        return self.call_api('GetReactions', request_data)
    
    def get_single_chat_conv_list(self, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取单聊会话列表"""
        if request_data is None:
            request_data = {}
        return self.call_api('GetSingleChatConvList', request_data)
    
    def mark_read(self, conv_id: str, read_seq: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """标记已读"""
        if request_data is None:
            request_data = {}
        request_data['conv_id'] = conv_id
        request_data['read_seq'] = read_seq
        return self.call_api('MarkRead', request_data)
    
    def get_fans_list(self, limit: int = 20, offset: int = 0, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取粉丝列表"""
        if request_data is None:
            request_data = {}
        request_data['limit'] = limit
        request_data['offset'] = offset
        return self.call_api('GetFansList', request_data)
    
    def get_follow_list(self, limit: int = 20, offset: int = 0, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取关注列表"""
        if request_data is None:
            request_data = {}
        request_data['limit'] = limit
        request_data['offset'] = offset
        return self.call_api('GetFollowList', request_data)
    
    def get_friend_list(self, limit: int = 20, offset: int = 0, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取好友列表"""
        if request_data is None:
            request_data = {}
        request_data['limit'] = limit
        request_data['offset'] = offset
        return self.call_api('GetFriendList', request_data)
    
    def follow(self, target_uid: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """关注用户"""
        if request_data is None:
            request_data = {}
        request_data['target_uid'] = target_uid
        return self.call_api('Follow', request_data)
    
    def unfollow(self, target_uid: int, request_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """取消关注"""
        if request_data is None:
            request_data = {}
        request_data['target_uid'] = target_uid
        return self.call_api('Unfollow', request_data)
    
    def send_world_chat_message(self, text: str = "test message") -> Tuple[Optional[str], Optional[int]]:
        """
        发送世界聊天消息（用于获取conv_id和seq）
        
        Returns:
            (conv_id, seq) 元组，如果失败返回 (None, None)
        """
        content = {
            'msg_type': 1,
            'text': {'text': text}
        }
        result = self.send_message(content, to_uid=0, scene=4, scene_id=0)
        
        if self.is_success(result):
            response = self.get_response(result)
            if 'sendmessage' in response:
                msg_data = response['sendmessage']
                conv_id = msg_data.get('conv_id', '')
                seq = msg_data.get('seq', 0)
                return (conv_id, seq)
        
        return (None, None)



