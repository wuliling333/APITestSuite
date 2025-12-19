"""
TCP客户端 - 处理与Gate服务器的TCP通信
"""
import socket
import struct
import threading
import queue
import time
from typing import Dict, Any, Optional
from framework.config import Config


class TCPClient:
    """TCP客户端"""
    
    def __init__(self, config: Config):
        self.config = config
        self.socket = None
        self.seq = 0
        self.pending_requests = {}  # seq -> (response_queue, timestamp)
        self.read_thread = None
        self.running = False
        self.lock = threading.Lock()
    
    def connect(self, host: str, port: int) -> bool:
        """连接服务器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.config.get_timeout())
            self.socket.connect((host, port))
            
            # 启动读取线程
            self.running = True
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
            
            return True
        except Exception as e:
            print(f"✗ TCP连接失败: {e}")
            return False
    
    def _read_loop(self):
        """读取循环"""
        buffer = b''
        
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                buffer += data
                
                # 解析数据包
                while len(buffer) >= 4:
                    # 读取总长度
                    total_len = struct.unpack('<I', buffer[:4])[0]
                    
                    # 检查是否有完整数据包
                    packet_size = 4 + total_len
                    if len(buffer) < packet_size:
                        break
                    
                    # 提取完整数据包
                    packet = buffer[:packet_size]
                    buffer = buffer[packet_size:]
                    
                    # 解析响应
                    self._parse_response(packet)
            
            except socket.timeout:
                continue
            except Exception as e:
                print(f"✗ 读取数据失败: {e}")
                break
    
    def _parse_response(self, packet: bytes):
        """解析响应数据包"""
        try:
            offset = 4  # 跳过总长度
            
            # 读取头部长度
            head_len = struct.unpack('<I', packet[offset:offset+4])[0]
            offset += 4
            
            # 读取头部数据（protobuf）
            head_bytes = packet[offset:offset+head_len]
            offset += head_len
            
            # 读取body长度
            body_len = struct.unpack('<I', packet[offset:offset+4])[0]
            offset += 4
            
            # 读取body数据
            body_bytes = packet[offset:offset+body_len] if body_len > 0 else b''
            
            # 解析protobuf头部（简化处理，直接提取关键字段）
            # 这里需要protobuf库来解析，暂时用简单方式
            seq = self._extract_seq_from_head(head_bytes)
            
            # 查找对应的请求
            with self.lock:
                if seq in self.pending_requests:
                    response_queue, _ = self.pending_requests[seq]
                    response_queue.put({
                        'seq': seq,
                        'head_bytes': head_bytes,
                        'body_bytes': body_bytes,
                        'head_len': head_len,
                        'body_len': body_len
                    })
                    del self.pending_requests[seq]
        
        except Exception as e:
            print(f"✗ 解析响应失败: {e}")
    
    def _extract_seq_from_head(self, head_bytes: bytes) -> int:
        """从protobuf头部提取seq"""
        try:
            # 尝试使用protobuf库解析
            import sys
            import os
            generated_proto_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_proto')
            sys.path.insert(0, generated_proto_path)
            sys.path.insert(0, os.path.join(generated_proto_path, 'shared'))
            
            from shared import head_pb2
            rsp_head = head_pb2.RspHead()
            rsp_head.ParseFromString(head_bytes)
            return rsp_head.seq
        except:
            # 回退到简单解析
            try:
                idx = 0
                while idx < len(head_bytes):
                    if idx < len(head_bytes):
                        tag = head_bytes[idx]
                        field_num = tag >> 3
                        wire_type = tag & 0x7
                        
                        if field_num == 2 and wire_type == 0:  # seq字段，varint类型
                            # 读取varint值
                            value = 0
                            shift = 0
                            idx += 1
                            while idx < len(head_bytes):
                                byte = head_bytes[idx]
                                value |= (byte & 0x7F) << shift
                                idx += 1
                                if (byte & 0x80) == 0:
                                    break
                                shift += 7
                            return value
                        else:
                            # 跳过当前字段
                            idx += 1
                            if wire_type == 0:  # varint
                                while idx < len(head_bytes) and (head_bytes[idx] & 0x80):
                                    idx += 1
                                idx += 1
                            elif wire_type == 2:  # length-delimited
                                if idx < len(head_bytes):
                                    length = head_bytes[idx]
                                    idx += 1 + length
                            else:
                                idx += 1
            except:
                pass
        return 0
    
    def send_request(self, command: int, op_type: int, body_bytes: bytes) -> Optional[Dict]:
        """发送请求并等待响应"""
        with self.lock:
            self.seq += 1
            seq = self.seq
        
        # 构造请求头（protobuf格式）
        # ReqHead: command=1, seq=2, type=3
        head_bytes = self._encode_req_head(command, seq, op_type)
        
        # 编码数据包
        packet = self._encode_packet(head_bytes, body_bytes)
        
        # 发送请求
        try:
            self.socket.sendall(packet)
        except Exception as e:
            print(f"✗ 发送请求失败: {e}")
            return None
        
        # 等待响应
        response_queue = queue.Queue()
        with self.lock:
            self.pending_requests[seq] = (response_queue, time.time())
        
        try:
            response = response_queue.get(timeout=self.config.get_timeout())
            return response
        except queue.Empty:
            with self.lock:
                if seq in self.pending_requests:
                    del self.pending_requests[seq]
            print(f"✗ 请求超时: seq={seq}")
            return None
    
    def _encode_req_head(self, command: int, seq: int, op_type: int) -> bytes:
        """编码请求头（protobuf格式）"""
        # 简化实现：手动编码protobuf
        # field 1 (command): varint
        # field 2 (seq): varint
        # field 3 (type): varint
        
        def encode_varint(value):
            result = []
            while value >= 0x80:
                result.append((value & 0x7F) | 0x80)
                value >>= 7
            result.append(value & 0x7F)
            return bytes(result)
        
        head = b''
        # field 1: command
        head += bytes([(1 << 3) | 0])  # wire type 0 (varint)
        head += encode_varint(command)
        
        # field 2: seq
        head += bytes([(2 << 3) | 0])
        head += encode_varint(seq)
        
        # field 3: type
        head += bytes([(3 << 3) | 0])
        head += encode_varint(op_type)
        
        return head
    
    def _encode_packet(self, head_bytes: bytes, body_bytes: bytes) -> bytes:
        """编码数据包"""
        # 4 bytes total length + 4 bytes head length + headBytes + 4 bytes body length + bodyBytes
        total_len = 4 + len(head_bytes) + 4 + len(body_bytes)
        
        packet = struct.pack('<I', total_len)  # total length
        packet += struct.pack('<I', len(head_bytes))  # head length
        packet += head_bytes
        packet += struct.pack('<I', len(body_bytes))  # body length
        packet += body_bytes
        
        return packet
    
    def close(self):
        """关闭连接"""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None

