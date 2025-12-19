#!/usr/bin/env python3
"""
检查所有接口的请求参数，对照服务器协议定义
"""
import os
import sys
import yaml
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 从proto文件读取的接口定义（手动整理，因为需要解析proto）
PROTO_DEFINITIONS = {
    'Hall': {
        'FetchSelfFullUserInfo': {'request': {}, 'response': {'full_user_info': 'FullUserInfo'}},
        'FetchSimpleUserInfo': {'request': {'target_uid': 'int64'}, 'response': {'simple_user_info': 'SimpleUserInfo'}},
        'UpdateNickname': {'request': {'nickname': 'string'}, 'response': {'nickname': 'string'}},
        'SellItem': {'request': {'unique_id_list': 'repeated int32'}, 'response': {'success': 'bool'}},
        'BuyItem': {'request': {'item_id_list': 'repeated int64'}, 'response': {'success': 'bool'}},
        'StashToBackpack': {'request': {'unique_id': 'int32', 'cell_id': 'int32'}, 'response': {'success': 'bool', 'backpack': 'BackpackInfo'}},
        'BackpackToStash': {'request': {'cell_id': 'int32'}, 'response': {'success': 'bool', 'backpack': 'BackpackInfo'}},
        'ExchangeBackpackItem': {'request': {'source_cell_id': 'int32', 'target_cell_id': 'int32'}, 'response': {'success': 'bool', 'backpack': 'BackpackInfo'}},
        'DebugAddCash': {'request': {'amount': 'int64'}, 'response': {'success': 'bool'}},
        'DebugAddItem': {'request': {'item_id': 'int64'}, 'response': {'success': 'bool'}},
    },
    'Room': {
        'GetUserState': {'request': {}, 'response': {'team_id': 'int64', 'game_id': 'int64'}},
        'CreateTeam': {'request': {'game_mode': 'int32'}, 'response': {'team_info': 'RoomTeamInfo'}},
        'JoinTeam': {'request': {'team_id': 'int64'}, 'response': {'team_info': 'RoomTeamInfo'}},
        'LeaveTeam': {'request': {'team_id': 'int64'}, 'response': {'success': 'bool'}},
        'GetTeamInfo': {'request': {'team_id': 'int64'}, 'response': {'team_info': 'RoomTeamInfo'}},
        'ChangeReadyState': {'request': {'team_id': 'int64', 'ready': 'bool'}, 'response': {'success': 'bool'}},
        'StartGameFromTeam': {'request': {'team_id': 'int64', 'map_id': 'int32', 'difficulty': 'int32'}, 'response': {'success': 'bool'}},
        'Match': {'request': {'team_id': 'int64', 'map_id': 'int32', 'difficulty': 'int32'}, 'response': {'success': 'bool'}},
        'CancelMatch': {'request': {'team_id': 'int64'}, 'response': {'success': 'bool'}},
        'GetGameInfo': {'request': {'game_id': 'int64'}, 'response': {'game_info': 'RoomGameInfo'}},
    },
    'Social': {
        'SendMessage': {'request': {'conv_id': 'string', 'scene': 'int32', 'scene_id': 'int64', 'to_uid': 'int64', 'content': 'ChatMsgContent', 'client_msg_id': 'string'}, 'response': {'msg_id': 'string', 'conv_id': 'string', 'seq': 'int64', 'send_time_ms': 'int64'}},
        'PullMsgs': {'request': {'conv_id': 'string', 'scene': 'int32', 'scene_id': 'int64', 'start_seq': 'int64', 'count': 'int32', 'reverse': 'bool'}, 'response': {'msgs': 'repeated ChatMessage', 'has_more': 'bool', 'min_seq': 'int64', 'max_seq': 'int64'}},
        'RevokeMsg': {'request': {'conv_id': 'string', 'seq': 'int64'}, 'response': {'success': 'bool'}},
        'DeleteMsg': {'request': {'conv_id': 'string', 'seqs': 'repeated int64'}, 'response': {'deleted_count': 'int32'}},
        'AddReaction': {'request': {'conv_id': 'string', 'seq': 'int64', 'reaction_id': 'int32'}, 'response': {'success': 'bool', 'total_count': 'int32'}},
        'RemoveReaction': {'request': {'conv_id': 'string', 'seq': 'int64', 'reaction_id': 'int32'}, 'response': {'success': 'bool', 'total_count': 'int32'}},
        'GetReactions': {'request': {'conv_id': 'string', 'seq': 'int64'}, 'response': {'reactions': 'repeated ReactionDetail'}},
        'GetSingleChatConvList': {'request': {}, 'response': {'convs': 'repeated SingleChatConvInfo'}},
        'MarkRead': {'request': {'conv_id': 'string', 'read_seq': 'int64'}, 'response': {'success': 'bool'}},
        'GetFansList': {'request': {'limit': 'int32', 'offset': 'int32'}, 'response': {'fans': 'repeated SimpleUserInfo'}},
        'GetFollowList': {'request': {'limit': 'int32', 'offset': 'int32'}, 'response': {'follows': 'repeated SimpleUserInfo'}},
        'GetFriendList': {'request': {'limit': 'int32', 'offset': 'int32'}, 'response': {'friends': 'repeated SimpleUserInfo'}},
        'Follow': {'request': {'target_uid': 'int64'}, 'response': {'success': 'bool'}},
        'Unfollow': {'request': {'target_uid': 'int64'}, 'response': {'success': 'bool'}},
    }
}

def check_test_cases():
    """检查所有测试用例的请求参数"""
    print("=" * 80)
    print("检查所有接口的请求参数（对照服务器协议）")
    print("=" * 80)
    
    test_cases_dir = 'test_cases'
    all_issues = []
    
    for service_name in ['hall', 'room', 'social']:
        yaml_file = f"{test_cases_dir}/{service_name}/test_{service_name}.yaml"
        if not os.path.exists(yaml_file):
            print(f"\n⚠ {service_name.upper()} 服务: 测试用例文件不存在: {yaml_file}")
            continue
        
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'test_cases' not in data:
            print(f"\n⚠ {service_name.upper()} 服务: 测试用例文件为空或格式错误")
            continue
        
        service_cap = service_name.capitalize()
        proto_defs = PROTO_DEFINITIONS.get(service_cap, {})
        
        print(f"\n{'='*80}")
        print(f"{service_cap.upper()} 服务接口检查:")
        print(f"{'='*80}")
        
        for method_name, test_case in data['test_cases'].items():
            request_data = test_case.get('request', {})
            proto_def = proto_defs.get(method_name, {})
            
            if not proto_def:
                print(f"\n⚠ {method_name}: 未找到协议定义")
                all_issues.append(f"{service_cap}.{method_name}: 未找到协议定义")
                continue
            
            expected_request = proto_def.get('request', {})
            print(f"\n接口: {method_name}")
            print(f"  协议定义请求参数: {json.dumps(expected_request, indent=2, ensure_ascii=False)}")
            print(f"  测试用例请求参数: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
            
            # 检查参数是否匹配
            issues = []
            for param_name, param_type in expected_request.items():
                if param_name not in request_data:
                    if 'repeated' not in param_type and param_type not in ['bool', 'int32', 'int64', 'string']:
                        # 复杂类型可能为空，不报错
                        pass
                    elif param_type in ['bool', 'int32', 'int64']:
                        # 基本类型如果缺失，可能是问题
                        issues.append(f"缺少参数: {param_name} ({param_type})")
            
            if issues:
                print(f"  ⚠ 问题: {', '.join(issues)}")
                all_issues.append(f"{service_cap}.{method_name}: {', '.join(issues)}")
            else:
                print(f"  ✓ 请求参数正确")
    
    print(f"\n{'='*80}")
    print("总结:")
    print(f"{'='*80}")
    if all_issues:
        print(f"发现 {len(all_issues)} 个问题:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("✓ 所有接口的请求参数都正确")
    
    return all_issues

if __name__ == '__main__':
    check_test_cases()

