# RPC 方法格式说明

## 📋 标准 RPC 方法定义

### 格式

```protobuf
service ServiceName {
    rpc MethodName(RequestMessage) returns (ResponseMessage);
}
```

### 实际示例

#### 1. Hall Service (service/hall/hall.proto)

```protobuf
syntax = "proto3";
package hall;

service HallService {
    // 处理客户端请求
    rpc HandlerClientRequest(shared.ClientRequest) returns (shared.ClientResponse);

    // 获取玩家完整信息
    rpc FetchFullUserInfo(FetchFullUserInfoReq) returns (FetchFullUserInfoRsp);

    // 通知玩家进入游戏，从仓库扣除背包道具，并返回玩家完整信息
    rpc NotifyUserEnterGame(NotifyUserEnterGameReq) returns (NotifyUserEnterGameRsp);

    // 批量获取玩家简略信息
    rpc BatchFetchSimpleUserInfo(BatchFetchSimpleUserInfoReq) returns (BatchFetchSimpleUserInfoRsp);

    // 上报玩家从游戏中带出的战利品和道具。由 room 调用
    rpc ReportGameSpoils(ReportGameSpoilsReq) returns (ReportGameSpoilsRsp);

    // 玩家在战斗服购买道具。由 room 调用
    rpc BuyItemInGame(BuyItemInGameReq) returns (BuyItemInGameRsp);

    // 接收 center 发送的指令
    rpc HandlerCenterCommand(shared.CenterCommandReq) returns (shared.CenterCommandRsp);
}

// 请求消息定义
message FetchFullUserInfoReq {
    int64 uid = 1;
}

// 响应消息定义
message FetchFullUserInfoRsp {
    shared.FullUserInfo full_user_info = 1;
    bool exists = 2; // 玩家是否存在
}
```

#### 2. Room Service (service/room/room.proto)

```protobuf
syntax = "proto3";
package room;

service RoomService {
    rpc HandlerClientRequest(shared.ClientRequest) returns (shared.ClientResponse);
    
    // 获取房间成员列表（供聊天服调用）
    rpc GetTeamMembers(GetTeamMembersReq) returns (GetTeamMembersRsp);

    // 上报游戏结果（供战斗服调用）
    rpc ReportGameResult(ReportGameResultReq) returns (ReportGameResultRsp);

    // 上报游戏结束（供战斗服调用）
    rpc ReportGameOver(ReportGameOverReq) returns (ReportGameOverRsp);

    // 游戏内购买道具（供游戏服调用）
    rpc BuyItemInGame(BuyItemInGameReq) returns (BuyItemInGameRsp);

    // 匹配成功后创建游戏实例
    rpc CreateGameAfterMatch(CreateGameAfterMatchReq) returns (CreateGameAfterMatchRsp);

    // 通知team匹配结果
    rpc NotifyMatchResult(NotifyMatchResultReq) returns (NotifyMatchResultRsp);

    // 匹配服重启后向房间服获取所有匹配中的队伍信息恢复匹配
    rpc RecoverMatch(RecoverMatchReq) returns (RecoverMatchRsp);

    // 强制玩家离开队伍（跨节点调用）
    rpc ForceLeaveTeam(ForceLeaveTeamReq) returns (ForceLeaveTeamRsp);
}
```

## 🔄 两种 Proto 文件格式对比

### 格式1：标准 gRPC RPC 定义（服务间通信）

**位置**：`config/proto_jinn/service/*/`

**格式**：
```protobuf
service HallService {
    rpc FetchFullUserInfo(FetchFullUserInfoReq) returns (FetchFullUserInfoRsp);
}
```

**用途**：
- ✅ 服务间通信（gRPC）
- ✅ 服务器内部调用
- ✅ 使用 gRPC 框架

**示例文件**：
- `service/hall/hall.proto`
- `service/room/room.proto`
- `service/social/social.proto`

### 格式2：消息包装模式（客户端通信）

**位置**：`config/proto_jinn/client/`

**格式**：
```protobuf
enum HallOpType {
    HallOpTypeFetchSelfFullUserInfo = 2;
}

message HallBodyReq {
    HallFetchSelfFullUserInfoReq fetch_self_full_user_info = 2;
}

message HallFetchSelfFullUserInfoReq { }
message HallFetchSelfFullUserInfoRsp { ... }
```

**用途**：
- ✅ 客户端与服务器通信（TCP）
- ✅ 通过 Gate 服务器转发
- ✅ 使用自定义 TCP 协议

**示例文件**：
- `client/hall_reqrsp.proto`
- `client/room_reqrsp.proto`
- `client/social_reqrsp.proto`

## 📊 对比总结

| 特性 | gRPC RPC定义 | 消息包装模式 |
|------|-------------|-------------|
| **定义方式** | `service` + `rpc` | `enum` + `message` |
| **文件位置** | `service/*/` | `client/` |
| **通信方式** | gRPC | TCP |
| **使用场景** | 服务间调用 | 客户端调用 |
| **框架支持** | gRPC框架 | 自定义框架 |

## 🎯 框架当前支持的格式

**APITestSuite 框架当前支持的是：消息包装模式（client/*.proto）**

### 为什么？

1. **测试目标** - 框架用于测试客户端API接口
2. **通信协议** - 客户端通过TCP与Gate服务器通信
3. **消息格式** - 使用 `BodyReq`/`BodyRsp` 包装消息

### 框架如何解析？

```python
# 框架通过消息命名约定识别接口
pattern = rf'message\s+{service_cap}(\w+)Req\s*{{'

# 例如：
# message HallFetchSelfFullUserInfoReq { } → 识别为 FetchSelfFullUserInfo
# message HallUpdateNicknameReq { ... }   → 识别为 UpdateNickname
```

## 📝 RPC 方法语法详解

### 基本语法

```protobuf
rpc MethodName(RequestType) returns (ResponseType);
```

### 参数说明

- **MethodName** - 方法名（驼峰命名）
- **RequestType** - 请求消息类型
- **ResponseType** - 响应消息类型

### 完整示例

```protobuf
service UserService {
    // 简单RPC（请求-响应）
    rpc GetUser(GetUserReq) returns (GetUserRsp);
    
    // 服务器流式RPC
    rpc ListUsers(ListUsersReq) returns (stream User);
    
    // 客户端流式RPC
    rpc CreateUsers(stream CreateUserReq) returns (CreateUsersRsp);
    
    // 双向流式RPC
    rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}
```

### 注释

```protobuf
service HallService {
    // 这是单行注释
    rpc Method1(Req1) returns (Rsp1);
    
    /* 这是多行注释
       可以写多行 */
    rpc Method2(Req2) returns (Rsp2);
}
```

## 🔍 生成的代码示例

### Go 语言（gRPC）

**客户端接口**：
```go
type HallServiceClient interface {
    FetchFullUserInfo(ctx context.Context, in *FetchFullUserInfoReq, opts ...grpc.CallOption) (*FetchFullUserInfoRsp, error)
}
```

**服务器接口**：
```go
type HallServiceServer interface {
    FetchFullUserInfo(context.Context, *FetchFullUserInfoReq) (*FetchFullUserInfoRsp, error)
}
```

### Python 语言（gRPC）

```python
class HallServiceStub:
    def FetchFullUserInfo(self, request, timeout=None, metadata=None):
        # 调用RPC方法
        pass
```

## ✅ 总结

1. **标准RPC定义** - 使用 `service` 和 `rpc` 关键字
2. **消息包装模式** - 使用 `enum` 和 `message`（你们客户端使用的）
3. **框架支持** - 当前框架支持消息包装模式
4. **两种格式** - 服务间用gRPC，客户端用TCP

---

**文档版本**: v1.0  
**最后更新**: 2024-12-23
