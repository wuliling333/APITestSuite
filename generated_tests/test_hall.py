"""
自动生成的Hall服务测试代码
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


class TestHall(unittest.TestCase):
    """Hall服务测试"""
    
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
    

    def test_fetchselffulluserinfo(self):
        """测试 FetchSelfFullUserInfo 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Hall',
            method='FetchSelfFullUserInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'FetchSelfFullUserInfo',
            'method': 'FetchSelfFullUserInfo',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: FetchSelfFullUserInfo")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ FetchSelfFullUserInfo 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ FetchSelfFullUserInfo 测试通过")

    def test_fetchsimpleuserinfo(self):
        """测试 FetchSimpleUserInfo 接口"""
        request_data = {'target_uid': self.current_uid if hasattr(self, 'current_uid') else self.client.uid}
        
        result = self.client.call_rpc(
            service='Hall',
            method='FetchSimpleUserInfo',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'FetchSimpleUserInfo',
            'method': 'FetchSimpleUserInfo',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: FetchSimpleUserInfo")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ FetchSimpleUserInfo 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ FetchSimpleUserInfo 测试通过")

    def test_updatenickname(self):
        """测试 UpdateNickname 接口"""
        request_data = {'nickname': 'TestNickname_123'}
        
        result = self.client.call_rpc(
            service='Hall',
            method='UpdateNickname',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'UpdateNickname',
            'method': 'UpdateNickname',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: UpdateNickname")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ UpdateNickname 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ UpdateNickname 测试通过")

    def test_sellitem(self):
        """测试 SellItem 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Hall',
            method='SellItem',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'SellItem',
            'method': 'SellItem',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: SellItem")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ SellItem 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ SellItem 测试通过")

    def test_buyitem(self):
        """测试 BuyItem 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Hall',
            method='BuyItem',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'BuyItem',
            'method': 'BuyItem',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: BuyItem")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ BuyItem 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ BuyItem 测试通过")

    def test_stashtobackpack(self):
        """测试 StashToBackpack 接口（前置条件：从仓库获取有效的unique_id和背包空cell_id）"""
        # 前置条件：获取用户信息，找到仓库中的物品和背包中的空格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {user_info_result.get('error_message', '未知错误')}")
        
        user_info = user_info_result.get('response', {})
        full_user_info = user_info.get('fetchselffulluserinfo', {}).get('full_user_info', {})
        stash = full_user_info.get('stash', {})
        backpack = full_user_info.get('backpack', {})
        
        # 从仓库中找到有效的物品（unique_id > 0）
        unique_id = 0
        for item in stash.get('items', []):
            if isinstance(item, dict) and item.get('unique_id', 0) > 0:
                unique_id = item.get('unique_id')
                break
        
        # 从背包中找到空的格子（carried_item 为空或 item_id == 0）
        cell_id = 0
        for cell in backpack.get('cells', []):
            if isinstance(cell, dict):
                carried_item = cell.get('carried_item', {})
                if not carried_item or (isinstance(carried_item, dict) and carried_item.get('item_id', 0) == 0):
                    cell_id = cell.get('cell_id', 0)
                    if cell_id >= 0:  # cell_id 可以是 0
                        break
        
        if unique_id == 0:
            self.skipTest("前置条件失败：仓库中没有有效的物品")
        if cell_id == 0:
            self.skipTest("前置条件失败：背包中没有空的格子")
        
        # 使用获取到的 unique_id 和 cell_id 调用接口
        request_data = {'unique_id': unique_id, 'cell_id': cell_id}
        
        result = self.client.call_rpc(
            service='Hall',
            method='StashToBackpack',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'StashToBackpack',
            'method': 'StashToBackpack',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: StashToBackpack")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ StashToBackpack 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ StashToBackpack 测试通过")

    def test_backpacktostash(self):
        """测试 BackpackToStash 接口（前置条件：从背包获取有效的cell_id）"""
        # 前置条件：获取用户信息，找到背包中有物品的格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {user_info_result.get('error_message', '未知错误')}")
        
        user_info = user_info_result.get('response', {})
        full_user_info = user_info.get('fetchselffulluserinfo', {}).get('full_user_info', {})
        backpack = full_user_info.get('backpack', {})
        
        # 从背包中找到有物品的格子（carried_item 不为空且 item_id > 0）
        cell_id = 0
        for cell in backpack.get('cells', []):
            if isinstance(cell, dict):
                carried_item = cell.get('carried_item', {})
                if isinstance(carried_item, dict) and carried_item.get('item_id', 0) > 0:
                    cell_id = cell.get('cell_id', 0)
                    if cell_id >= 0:  # cell_id 可以是 0
                        break
        
        if cell_id == 0:
            self.skipTest("前置条件失败：背包中没有有效的物品")
        
        # 使用获取到的 cell_id 调用接口
        request_data = {'cell_id': cell_id}
        
        result = self.client.call_rpc(
            service='Hall',
            method='BackpackToStash',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'BackpackToStash',
            'method': 'BackpackToStash',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: BackpackToStash")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ BackpackToStash 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ BackpackToStash 测试通过")

    def test_exchangebackpackitem(self):
        """测试 ExchangeBackpackItem 接口（前置条件：从背包获取两个有效的cell_id）"""
        # 前置条件：获取用户信息，找到背包中的两个格子
        user_info_result = self.client.call_rpc('Hall', 'FetchSelfFullUserInfo', {})
        if not user_info_result.get('success'):
            self.skipTest(f"前置条件失败：无法获取用户信息 - {user_info_result.get('error_message', '未知错误')}")
        
        user_info = user_info_result.get('response', {})
        full_user_info = user_info.get('fetchselffulluserinfo', {}).get('full_user_info', {})
        backpack = full_user_info.get('backpack', {})
        
        # 从背包中找到两个格子（至少需要两个格子）
        cells = backpack.get('cells', [])
        if len(cells) < 2:
            self.skipTest("前置条件失败：背包中格子数量不足")
        
        source_cell_id = cells[0].get('cell_id', 0)
        target_cell_id = cells[1].get('cell_id', 0)
        
        if source_cell_id == 0 or target_cell_id == 0:
            self.skipTest("前置条件失败：无法获取有效的 cell_id")
        
        # 使用获取到的 cell_id 调用接口
        request_data = {'source_cell_id': source_cell_id, 'target_cell_id': target_cell_id}
        
        result = self.client.call_rpc(
            service='Hall',
            method='ExchangeBackpackItem',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'ExchangeBackpackItem',
            'method': 'ExchangeBackpackItem',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: ExchangeBackpackItem")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ ExchangeBackpackItem 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ ExchangeBackpackItem 测试通过")

    def test_debugaddcash(self):
        """测试 DebugAddCash 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Hall',
            method='DebugAddCash',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'DebugAddCash',
            'method': 'DebugAddCash',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: DebugAddCash")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DebugAddCash 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ DebugAddCash 测试通过")

    def test_debugadditem(self):
        """测试 DebugAddItem 接口"""
        request_data = {}
        
        result = self.client.call_rpc(
            service='Hall',
            method='DebugAddItem',
            request_data=request_data
        )
        
        # 保存测试结果用于报告
        self.test_result = {
            'name': 'DebugAddItem',
            'method': 'DebugAddItem',
            'request': request_data,
            'response': result,  # 保存完整的result，包括success、response、error_code、error_message
            'error_code': result.get('error_code', 200),
            'error_message': result.get('error_message', ''),
            'success': result.get('success', False),
            'preconditions': []
        }
        
        # 打印请求和响应信息（无论成功或失败）
        print(f"\n============================================================")
        print(f"测试接口: DebugAddItem")
        print(f"请求参数: {safe_json_dumps(request_data)}")
        print(f"响应数据: {safe_json_dumps(result.get('response', {}))}")
        print(f"响应码: {result.get('error_code', 200)}")
        if result.get('error_message'):
            print(f"错误信息: {result.get('error_message')}")
        print(f"============================================================")
        
        # 断言
        if not result.get('success', False):
            error_msg = result.get('error_message', '未知错误')
            print(f"\n✗ DebugAddItem 测试失败: {error_msg}")
            self.assertTrue(False, f"API调用失败: {error_msg}")
        else:
            print(f"\n✓ DebugAddItem 测试通过")

if __name__ == '__main__':
    unittest.main()
