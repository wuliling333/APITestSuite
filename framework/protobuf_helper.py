"""
Protobuf辅助工具 - 处理protobuf序列化
"""
from typing import Dict, Any


class ProtobufHelper:
    """Protobuf辅助类"""
    
    @staticmethod
    def encode_varint(value: int) -> bytes:
        """编码varint"""
        result = []
        while value >= 0x80:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        result.append(value & 0x7F)
        return bytes(result)
    
    @staticmethod
    def encode_field(field_num: int, wire_type: int, value: bytes) -> bytes:
        """编码protobuf字段"""
        tag = (field_num << 3) | wire_type
        return bytes([tag]) + value
    
    @staticmethod
    def encode_string(field_num: int, value: str) -> bytes:
        """编码字符串字段"""
        value_bytes = value.encode('utf-8')
        length_bytes = ProtobufHelper.encode_varint(len(value_bytes))
        return ProtobufHelper.encode_field(field_num, 2, length_bytes + value_bytes)
    
    @staticmethod
    def encode_int64(field_num: int, value: int) -> bytes:
        """编码int64字段"""
        return ProtobufHelper.encode_field(field_num, 0, ProtobufHelper.encode_varint(value))
    
    @staticmethod
    def encode_int32(field_num: int, value: int) -> bytes:
        """编码int32字段"""
        return ProtobufHelper.encode_field(field_num, 0, ProtobufHelper.encode_varint(value))
    
    @staticmethod
    def encode_bytes(field_num: int, value: bytes) -> bytes:
        """编码bytes字段"""
        length_bytes = ProtobufHelper.encode_varint(len(value))
        return ProtobufHelper.encode_field(field_num, 2, length_bytes + value)
    
    @staticmethod
    def encode_gate_bind_req(uid: int, token: str, platform: str = "test", lang: str = "zh", app_version: str = "1.0.0") -> bytes:
        """编码GateBindReq"""
        req = b''
        req += ProtobufHelper.encode_int64(1, uid)  # uid
        req += ProtobufHelper.encode_string(2, token)  # token
        req += ProtobufHelper.encode_string(3, platform)  # platform
        req += ProtobufHelper.encode_string(4, lang)  # lang
        req += ProtobufHelper.encode_string(5, app_version)  # appVersion
        return req
    
    @staticmethod
    def encode_gate_body_req(bind_req: bytes) -> bytes:
        """编码GateBodyReq"""
        # field 2: bind
        return ProtobufHelper.encode_bytes(2, bind_req)
    
    @staticmethod
    def encode_hall_body_req(method_name: str, request_data: Dict) -> bytes:
        """编码HallBodyReq"""
        # 根据方法名和请求数据构造对应的请求消息
        # 这里简化处理，返回空body
        # 实际需要根据不同的方法构造不同的protobuf消息
        return b''
    
    @staticmethod
    def parse_response_body(body_bytes: bytes) -> Dict:
        """解析响应body（简化实现）"""
        # 这里需要根据实际的protobuf消息类型解析
        # 暂时返回原始数据
        return {
            'raw_bytes': body_bytes.hex() if body_bytes else '',
            'size': len(body_bytes) if body_bytes else 0
        }

