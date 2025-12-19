"""
自动生成的Room服务测试代码
"""
import unittest
import sys
import os
import json

# 添加框架路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.client import APIClient
from framework.config import Config


def safe_json_dumps(obj, indent=2, ensure_ascii=False):
    """安全地将对象转换为JSON字符串，处理protobuf对象"""
    def convert_to_dict(val):
        # 检查是否是 protobuf 消息对象
        if hasattr(val, 'DESCRIPTOR') and hasattr(val, 'SerializeToString'):
            try:
                from google.protobuf.json_format import MessageToDict
                return MessageToDict(val, including_default_value_fields=True, preserving_proto_field_name=True)
            except:
                # 如果 MessageToDict 失败，尝试手动转换
                result = {}
                try:
                    for field_descriptor in val.DESCRIPTOR.fields:
                        field_name = field_descriptor.name
                        field_value = getattr(val, field_name)
                        if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                            result[field_name] = [convert_to_dict(item) for item in field_value]
                        elif field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                            if field_value:
                                result[field_name] = convert_to_dict(field_value)
                        else:
                            result[field_name] = field_value
                except:
                    pass
                return result
        elif isinstance(val, dict):
            return {k: convert_to_dict(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [convert_to_dict(item) for item in val]
        else:
            return val
    
    try:
        converted = convert_to_dict(obj)
        return json.dumps(converted, indent=indent, ensure_ascii=ensure_ascii, default=str)
    except Exception as e:
        # 如果转换失败，返回字符串表示
        return str(obj)


class TestRoom(unittest.TestCase):
    """Room服务测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.config = Config()
        cls.client = APIClient(cls.config)
        
        # 登录
        if not cls.client.login():
            raise Exception("登录失败")
        
        # 连接Gate
        if not cls.client.connect_gate():
            raise Exception("Gate连接失败")
        
        # 获取当前用户的UID（用于需要target_uid的接口）
        try:
            result = cls.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {})
            if result.get('success'):
                response = result.get('response', {})
                # 提取UID
                if 'fetchselffulluserinfo' in response:
                    full_info = response['fetchselffulluserinfo']
                    if 'full_user_info' in full_info:
                        cls.current_uid = full_info['full_user_info'].get('uid', cls.client.uid)
                    else:
                        cls.current_uid = cls.client.uid
                else:
                    cls.current_uid = cls.client.uid
            else:
                cls.current_uid = cls.client.uid
        except:
            cls.current_uid = cls.client.uid
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        if cls.client:
            cls.client.close()
    

    def test_getuserstate(self):
        """测试 GetUserState 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetUserState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetUserState',
            'method': 'GetUserState',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetUserState")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetUserState 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetUserState 测试通过")

    def test_createteam(self):
        """测试 CreateTeam 接口"""
        request_data = {'game_mode': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'CreateTeam',
            'method': 'CreateTeam',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: CreateTeam")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CreateTeam 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ CreateTeam 测试通过")

    def test_jointeam(self):
        """测试 JoinTeam 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 JoinTeam
        request_data = {'team_id': team_id}
        
        result = self.client.call_rpc(
            service='Room',
            method='JoinTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'JoinTeam',
            'method': 'JoinTeam',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': ['创建队伍 (CreateTeam)', '获取 team_id']
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: JoinTeam")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ JoinTeam 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ JoinTeam 测试通过")

    def test_getteaminfo(self):
        """测试 GetTeamInfo 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 GetTeamInfo
        request_data = {'team_id': team_id}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetTeamInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetTeamInfo',
            'method': 'GetTeamInfo',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetTeamInfo")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetTeamInfo 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetTeamInfo 测试通过")

    def test_changereadystate(self):
        """测试 ChangeReadyState 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 ChangeReadyState（设置为准备状态）
        request_data = {'team_id': team_id, 'ready': True}
        
        result = self.client.call_rpc(
            service='Room',
            method='ChangeReadyState',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'ChangeReadyState',
            'method': 'ChangeReadyState',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: ChangeReadyState")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ChangeReadyState 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ ChangeReadyState 测试通过")

    def test_startgamefromteam(self):
        """测试 StartGameFromTeam 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'StartGameFromTeam',
            'method': 'StartGameFromTeam',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: StartGameFromTeam")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StartGameFromTeam 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ StartGameFromTeam 测试通过")

    def test_match(self):
        """测试 Match 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 Match（需要 map_id）
        request_data = {'team_id': team_id, 'map_id': 1}
        
        result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'Match',
            'method': 'Match',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: Match")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ Match 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ Match 测试通过")

    def test_cancelmatch(self):
        """测试 CancelMatch 接口（前置条件：先创建队伍并开始匹配）"""
        # 前置条件1：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 前置条件2：开始匹配（使队伍状态变为匹配中）
        # Match 需要 map_id，使用默认值 1
        match_result = self.client.call_rpc(
            service='Room',
            method='Match',
            request_data={'team_id': team_id, 'map_id': 1}
        )
        
        if not match_result.get('success'):
            self.skipTest(f"前置条件失败：无法开始匹配 - {match_result.get('error_message', '未知错误')}")
        
        # 使用获取到的 team_id 调用 CancelMatch
        request_data = {'team_id': team_id}
        
        result = self.client.call_rpc(
            service='Room',
            method='CancelMatch',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'CancelMatch',
            'method': 'CancelMatch',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: CancelMatch")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ CancelMatch 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ CancelMatch 测试通过")

    def test_getgameinfo(self):
        """测试 GetGameInfo 接口（前置条件：先创建队伍并开始游戏）"""
        # 前置条件1：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 前置条件2：开始游戏（获取 game_id）
        start_game_result = self.client.call_rpc(
            service='Room',
            method='StartGameFromTeam',
            request_data={'team_id': team_id, 'map_id': 1}
        )
        
        if not start_game_result.get('success'):
            self.skipTest(f"前置条件失败：无法开始游戏 - {start_game_result.get('error_message', '未知错误')}")
        
        # 从开始游戏的响应中获取 game_id（需要通过 GetUserState 获取）
        user_state_result = self.client.call_rpc('Room', 'GetUserState', {})
        game_id = 0
        if user_state_result.get('success'):
            user_state = user_state_result.get('response', {})
            if 'getuserstate' in user_state:
                game_id = user_state['getuserstate'].get('game_id', 0)
        
        if game_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 game_id")
        
        # 使用获取到的 game_id 调用 GetGameInfo
        request_data = {'game_id': game_id}
        
        result = self.client.call_rpc(
            service='Room',
            method='GetGameInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'GetGameInfo',
            'method': 'GetGameInfo',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: GetGameInfo")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ GetGameInfo 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ GetGameInfo 测试通过")

    def test_leaveteam(self):
        """测试 LeaveTeam 接口（前置条件：先创建队伍）"""
        # 前置条件：先创建队伍
        create_result = self.client.call_rpc(
            service='Room',
            method='CreateTeam',
            request_data={'game_mode': 1}
        )
        
        if not create_result.get('success'):
            self.skipTest(f"前置条件失败：无法创建队伍 - {create_result.get('error_message', '未知错误')}")
        
        # 从创建队伍的响应中获取 team_id
        create_response = create_result.get('response', {})
        team_id = 0
        if 'createteam' in create_response:
            team_info = create_response['createteam'].get('team_info', {})
            team_id = team_info.get('team_id', 0)
        
        if team_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 team_id")
        
        # 使用获取到的 team_id 调用 LeaveTeam
        request_data = {'team_id': team_id}
        
        result = self.client.call_rpc(
            service='Room',
            method='LeaveTeam',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'LeaveTeam',
            'method': 'LeaveTeam',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: LeaveTeam")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ LeaveTeam 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ LeaveTeam 测试通过")

if __name__ == '__main__':
    unittest.main()
