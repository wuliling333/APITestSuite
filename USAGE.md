# APITestSuite 使用说明

本文档提供 APITestSuite 框架的详细使用指南。

## 📋 目录

1. [快速开始](#快速开始)
2. [配置说明](#配置说明)
3. [命令详解](#命令详解)
4. [测试用例编写](#测试用例编写)
5. [报告解读](#报告解读)
6. [高级功能](#高级功能)
7. [故障排查](#故障排查)

## 🚀 快速开始

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置服务器

编辑 `config.yaml`：

```yaml
servers:
  gate:
    address: "your-gate-server:port"
  login:
    url: "http://your-login-server:port"
```

### 第三步：运行测试

```bash
python3 main.py --run
```

## ⚙️ 配置说明

### config.yaml 完整配置

```yaml
# 服务器配置
servers:
  gate:
    address: "47.84.190.150:29205"  # Gate服务器TCP地址
  login:
    url: "http://47.84.190.150:29002"  # Login服务器HTTP地址

# Git仓库配置
jinn_server:
  repo_url: "https://git.17zjh.com/wegame/jinn_server.git"  # 仓库地址
  branch: "v0.1.0"  # 分支名
  local_path: "jinn_server"  # 本地路径
  read_only: true  # 是否只读模式

# 服务配置
services:
  hall:
    proto_path: "jinn_server/config/proto_jinn/client"  # Protobuf文件路径
  room:
    proto_path: "jinn_server/config/proto_jinn/client"
  social:
    proto_path: "jinn_server/config/proto_jinn/client"

# 测试配置
test:
  output_dir: "generated_tests"  # 测试代码输出目录
  report_dir: "reports"  # 报告输出目录
  timeout: 30  # 请求超时时间（秒）
```

### 配置项说明

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `servers.gate.address` | Gate服务器TCP地址 | ✅ |
| `servers.login.url` | Login服务器HTTP地址 | ✅ |
| `jinn_server.repo_url` | Git仓库地址 | ✅ |
| `jinn_server.branch` | Git分支名 | ✅ |
| `jinn_server.local_path` | 本地仓库路径 | ✅ |
| `services.*.proto_path` | Protobuf文件路径 | ✅ |
| `test.timeout` | 请求超时时间 | ❌ |

## 📖 命令详解

### 基础命令

#### `python3 main.py`

**功能**：更新代码并生成测试代码（不运行测试）

**执行流程**：
1. 检查并更新 Git 仓库
2. 测试服务器连接
3. 解析 Protobuf 接口定义
4. 生成 Python 测试代码

**使用场景**：
- 首次使用框架
- 更新接口定义后重新生成测试代码
- 不需要运行测试时

#### `python3 main.py --run`

**功能**：完整流程（更新代码 → 生成测试 → 运行测试 → 生成报告）

**执行流程**：
1. 检查并更新 Git 仓库
2. 测试服务器连接
3. 解析 Protobuf 接口定义
4. 生成 Python 测试代码
5. 执行所有测试（真实API调用）
6. 生成 HTML 和 Excel 报告

**使用场景**：
- 完整测试流程
- 需要查看测试报告

#### `python3 main.py --skip-git-check`

**功能**：跳过 Git 更新检查

**使用场景**：
- 本地代码已是最新
- 网络问题无法访问 Git
- 快速测试（节省时间）

### 测试用例生成命令

#### `python3 main.py --generate-yaml`

**功能**：生成五维度测试用例 YAML 文件

**执行流程**：
1. 检查并更新 Git 仓库（除非使用 `--skip-git-check`）
2. 解析 Protobuf 接口定义
3. 为每个接口生成五维度测试用例
4. 保存到 `test_cases/` 目录

**生成的文件**：
- `test_cases/hall/test_hall.yaml`
- `test_cases/room/test_room.yaml`
- `test_cases/social/test_social.yaml`

**使用场景**：
- 首次生成测试用例
- 接口更新后重新生成测试用例
- 需要手动编辑测试用例

#### `python3 main.py --generate-cases`

**功能**：生成测试用例 Excel（从 YAML 文件，并实际运行接口）

**执行流程**：
1. 检查并更新 Git 仓库（除非使用 `--skip-git-check`）
2. 读取 YAML 测试用例文件
3. **实际运行所有接口**，获取真实返回数据
4. 生成包含实际测试结果的 Excel 文件

**输出文件**：`reports/test_cases_complete.xlsx`

**使用场景**：
- 需要查看所有测试用例的完整信息
- 需要查看实际API返回数据
- 需要验证测试用例的正确性

### 框架选择命令

#### `python3 main.py --use-pytest`

**功能**：使用 pytest 框架和 PO 模式生成测试代码

**说明**：
- 默认使用 `unittest` 框架
- 使用 `--use-pytest` 可以生成基于 `pytest` 和 Page Object 模式的测试代码
- 需要配合 `--run` 使用

**使用场景**：
- 偏好使用 pytest 框架
- 需要 Page Object 模式
- 团队使用 pytest 作为标准

### 命令组合示例

```bash
# 生成测试用例，不更新Git
python3 main.py --generate-cases --skip-git-check

# 运行测试，不更新Git
python3 main.py --run --skip-git-check

# 使用pytest框架运行测试
python3 main.py --use-pytest --run

# 生成YAML测试用例，不更新Git
python3 main.py --generate-yaml --skip-git-check
```

## 📝 测试用例编写

### YAML 格式说明

测试用例使用 YAML 格式，基本结构如下：

```yaml
test_cases:
  用例名称:
    description: 用例描述
    priority: 优先级（P0/P1/P2）
    preconditions: 前置条件
    dimension: 维度（正常/参数异常/业务异常/权限安全/性能边界）
    request: 请求参数
    expected_status: 预期状态码
    expected_response: 预期响应
    jsonpath_assertion: JSONPath断言
    remark: 备注
```

### 请求参数格式

#### 简单格式

```yaml
request:
  nickname: "TestNickname"
  game_mode: 1
```

#### 详细格式（推荐）

```yaml
request:
  nickname:
    value: "TestNickname"
    type: string
  game_mode:
    value: 1
    type: int32
```

### 五维度测试用例

#### 1. 正常用例

```yaml
FetchSelfFullUserInfo_正常:
  description: FetchSelfFullUserInfo_正常调用
  priority: P0
  preconditions: 已登录
  dimension: 正常
  request: {}
  expected_status: '200'
  expected_response:
    success: true
    response:
      fetchselffulluserinfo:
        full_user_info:
          uid: 10000263
    error_code: 200
  jsonpath_assertion: $.success == true && $.error_code == 200
  remark: 正常业务流程验证
```

#### 2. 参数异常用例

```yaml
UpdateNickname_参数异常_必填参数缺失:
  description: UpdateNickname_参数异常_必填参数缺失
  priority: P1
  preconditions: 已登录
  dimension: 参数异常
  request:
    nickname:
      value: null
      type: string
  expected_status: 400/500
  expected_response:
    success: false
    response: {}
    error_code: 400
    error_message: invalid request
  jsonpath_assertion: $.error_code != 200
  remark: 必填参数缺失场景验证
```

#### 3. 业务异常用例

```yaml
JoinTeam_业务异常_队伍不存在:
  description: JoinTeam_业务异常_队伍不存在
  priority: P1
  preconditions: 已登录
  dimension: 业务异常
  request:
    team_id:
      value: 999999999
      type: int64
  expected_status: 400
  expected_response:
    success: false
    response: {}
    error_code: 400
    error_message: team not exist
  jsonpath_assertion: $.error_code != 200
  remark: 操作不存在的队伍
```

#### 4. 权限安全用例

```yaml
FetchSimpleUserInfo_权限安全_越权访问:
  description: FetchSimpleUserInfo_权限安全_越权访问
  priority: P0
  preconditions: 已登录
  dimension: 权限安全
  request:
    target_uid:
      value: 999999999
      type: int64
  expected_status: 403
  expected_response:
    success: false
    response: {}
    error_code: 403
  jsonpath_assertion: $.error_code == 403
  remark: 越权访问场景验证
```

#### 5. 性能边界用例

```yaml
SendMessage_性能边界_并发请求:
  description: SendMessage_性能边界_并发请求
  priority: P2
  preconditions: 已登录
  dimension: 性能边界
  request:
    scene:
      value: 4
      type: int32
    content:
      value: null
      type: ChatMsgContent
  expected_status: '200'
  expected_response:
    success: true
    response: {}
    error_code: 200
  jsonpath_assertion: $.success == true
  remark: 并发请求场景验证
```

### 前置条件说明

常见的前置条件：

- `已登录` - 用户已登录并获取token
- `已登录，已调用 CreateTeam 获取 team_id` - 需要先创建队伍
- `已登录（使用世界聊天场景 scene=4，可直接发送消息）` - 特定场景的前置条件

## 📊 报告解读

### HTML 报告

#### 报告结构

1. **汇总信息**
   - 总接口数
   - 通过数
   - 失败数
   - 错误数

2. **服务分页**
   - 按服务分类展示
   - 每个服务一个标签页

3. **接口详情**
   - 接口名称
   - 接口字段（从proto定义提取）
   - 请求参数
   - 实际输出
   - 响应码
   - 错误信息
   - 前置条件
   - 问题分析

#### 如何查看

1. 打开 `reports/test_report_*.html`
2. 查看汇总信息了解整体情况
3. 切换到对应服务标签页
4. 查看具体接口的详细信息

### Excel 报告

#### 报告结构

1. **汇总表**
   - 服务名称
   - 接口数
   - 通过数
   - 失败数

2. **详细表**（每个服务一个工作表）
   - 接口名称
   - 测试结果
   - 请求参数
   - 实际输出
   - 响应码
   - 错误信息

#### 如何使用

1. 打开 `reports/test_report_*.xlsx`
2. 查看汇总表了解整体情况
3. 切换到对应服务工作表
4. 使用筛选和排序功能查找特定接口

### 测试用例 Excel

#### 报告结构

- 用例编号
- 用例名称
- 优先级
- 前置条件
- 维度
- 方法+URL
- 请求头
- 请求体
- 预期服务器返回
- **实际服务器返回**（真实API调用结果）
- **状态**（通过/不通过，带颜色）
- JSONPath断言
- 备注

#### 状态说明

- ✅ **通过**（绿色）- 测试用例通过
- ❌ **不通过**（红色）- 测试用例失败
- ⚠️ **未测试**（灰色）- 测试用例未执行

## 🔧 高级功能

### 自定义测试用例

1. 编辑 `test_cases/{service}/test_{service}.yaml`
2. 添加或修改测试用例
3. 运行 `python3 main.py --generate-cases` 生成Excel

### 添加新服务

1. 在 `config.yaml` 中添加服务配置：
```yaml
services:
  new_service:
    proto_path: "jinn_server/config/proto_jinn/client"
```

2. 在 `framework/client.py` 中添加服务方法映射

3. 运行 `python3 main.py --generate-yaml` 生成测试用例

### 使用 Page Object 模式

1. 运行 `python3 main.py --use-pytest --run`
2. 框架会自动生成 Page Object 模式的测试代码
3. 页面对象位于 `framework/pages/` 目录

## 🔍 故障排查

### 问题：Git 更新失败

**可能原因**：
- 网络问题
- Git 仓库地址错误
- 分支不存在

**解决方法**：
1. 检查网络连接
2. 验证 Git 仓库地址和分支名
3. 使用 `--skip-git-check` 跳过 Git 更新

### 问题：服务器连接失败

**可能原因**：
- 服务器地址错误
- 服务器不可用
- 防火墙阻止

**解决方法**：
1. 检查 `config.yaml` 中的服务器地址
2. 使用 `ping` 或 `telnet` 测试服务器连接
3. 检查防火墙设置

### 问题：Protobuf 解析失败

**可能原因**：
- Protobuf 文件路径错误
- Protobuf 文件格式错误
- 缺少依赖

**解决方法**：
1. 检查 `config.yaml` 中的 `proto_path` 配置
2. 验证 Protobuf 文件是否存在
3. 重新安装依赖：`pip install -r requirements.txt`

### 问题：测试用例生成失败

**可能原因**：
- YAML 文件格式错误
- 测试用例定义不完整
- 接口定义变更

**解决方法**：
1. 检查 YAML 文件语法
2. 验证测试用例定义是否完整
3. 重新生成测试用例：`python3 main.py --generate-yaml`

### 问题：请求编码失败

**可能原因**：
- 请求参数类型不匹配
- 缺少必需字段
- Protobuf 模块未正确导入

**解决方法**：
1. 检查请求参数类型是否正确
2. 验证所有必需字段是否提供
3. 查看错误日志了解详细信息

## 📚 相关文档

- [README.md](./README.md) - 项目说明
- [REFACTORING.md](./REFACTORING.md) - 重构建议

## 💬 获取帮助

如果遇到问题，请：

1. 查看本文档的故障排查部分
2. 检查错误日志
3. 提交 Issue 到项目仓库

---

**祝使用愉快！** 🎉

