# APITestSuite

🚀 **自动化API测试框架** - 专为基于 Protobuf 的微服务API设计的全功能测试解决方案

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 简介

APITestSuite 是一个功能完整的API测试框架，专门用于测试基于 Go 语言和 Protobuf 定义的微服务API接口。框架提供了从接口发现、测试用例生成、测试执行到报告生成的全流程自动化能力。

### 核心特性

- 🔍 **自动接口发现** - 从 Protobuf 文件自动解析API接口定义
- 🤖 **智能代码生成** - 自动生成 Python 测试代码（支持 unittest 和 pytest）
- 📝 **五维度测试用例** - 自动生成正常/参数异常/业务异常/权限安全/性能边界测试用例
- 🎯 **真实API调用** - 直接连接服务器进行真实API调用，非模拟数据
- 📊 **多格式报告** - 生成 HTML 和 Excel 格式的详细测试报告
- 📋 **YAML管理** - 使用 YAML 格式管理测试用例，易于维护和版本控制
- 🔄 **自动同步** - 自动检测 Git 仓库变更，同步最新接口定义
- 🎨 **可视化结果** - Excel 报告中带颜色标识的通过/不通过状态

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器
- Git（用于拉取服务器代码）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd APITestSuite
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置服务器地址**

编辑 `config.yaml` 文件：

```yaml
servers:
  gate:
    address: "your-gate-server:port"
  login:
    url: "http://your-login-server:port"

jinn_server:
  repo_url: "https://your-git-repo.git"
  branch: "your-branch"
  local_path: "jinn_server"
  read_only: true

services:
  hall:
    proto_path: "jinn_server/config/proto_jinn/client"
  room:
    proto_path: "jinn_server/config/proto_jinn/client"
  social:
    proto_path: "jinn_server/config/proto_jinn/client"
```

4. **运行测试**

```bash
# 完整流程：更新代码 → 生成测试 → 运行测试 → 生成报告
python3 main.py --run
```

## 📚 使用指南

### 基础命令

#### 1. 更新代码并生成测试代码

```bash
python3 main.py
```

**执行流程**：
- ✅ 自动拉取/更新 Git 仓库代码
- ✅ 测试服务器连接
- ✅ 解析 Protobuf 接口定义
- ✅ 生成 Python 测试代码

#### 2. 运行测试并生成报告

```bash
python3 main.py --run
```

**执行流程**：
- ✅ 更新 Git 代码（如有更新）
- ✅ 测试服务器连接
- ✅ 解析接口定义
- ✅ 生成测试代码
- ✅ 执行所有测试（真实API调用）
- ✅ 生成 HTML 和 Excel 报告

#### 3. 跳过 Git 更新

```bash
# 使用本地已有代码，不更新 Git
python3 main.py --run --skip-git-check
```

### 测试用例生成

#### 生成 Excel 格式测试用例

```bash
python3 main.py --generate-cases
```

**功能说明**：
- ✅ 自动拉取最新 Git 代码（除非使用 `--skip-git-check`）
- ✅ 从 YAML 文件读取测试用例
- ✅ 实际运行所有接口，获取真实返回数据
- ✅ 生成包含实际测试结果的 Excel 文件

**输出文件**：`reports/test_cases_complete.xlsx`

**包含内容**：
- 用例编号、标题、优先级、前置条件
- 维度分类（正常/参数异常/业务异常/权限安全/性能边界）
- 请求参数（带类型信息）
- 预期状态码、服务器返回
- **实际服务器返回**（真实API调用结果）
- **状态标记**（通过✅/不通过❌，带颜色标识）
- JSONPath断言、数据库校验、备注

#### 生成 YAML 格式测试用例

```bash
python3 main.py --generate-yaml
```

**功能说明**：
- ✅ 自动拉取最新 Git 代码（除非使用 `--skip-git-check`）
- ✅ 基于最新接口定义生成五维度测试用例
- ✅ 按服务分类保存到 `test_cases/` 目录

**生成的文件**：
- `test_cases/hall/test_hall.yaml`
- `test_cases/room/test_room.yaml`
- `test_cases/social/test_social.yaml`

### 使用 pytest 框架

```bash
# 使用 pytest 框架和 PO 模式生成测试代码
python3 main.py --use-pytest --run
```

**说明**：
- 默认使用 `unittest` 框架
- 使用 `--use-pytest` 参数可以生成基于 `pytest` 和 Page Object 模式的测试代码

## 📁 项目结构

```
APITestSuite/
├── config.yaml                      # 配置文件
├── main.py                          # 主入口
├── requirements.txt                 # Python依赖
├── README.md                        # 项目说明（本文件）
├── REFACTORING.md                   # 重构建议文档
├── framework/                       # 框架核心模块
│   ├── config.py                   # 配置管理
│   ├── git_updater.py              # Git更新器
│   ├── connection_tester.py        # 连接测试器
│   ├── protobuf_parser.py          # Protobuf解析器
│   ├── proto_request_formatter.py  # 请求参数格式化
│   ├── client.py                   # API客户端（TCP通信）
│   ├── tcp_client.py               # TCP客户端
│   ├── protobuf_helper.py          # Protobuf辅助工具
│   ├── request_data_converter.py   # 请求数据转换器
│   ├── test_generator.py           # unittest测试代码生成器
│   ├── pytest_test_generator.py    # pytest测试代码生成器
│   ├── test_runner.py              # 测试运行器
│   ├── report_generator.py         # 报告生成器（HTML+Excel）
│   ├── test_case_generator.py      # Excel测试用例生成器
│   ├── yaml_test_case_generator.py # YAML测试用例生成器
│   └── pages/                      # Page Object模式页面对象
│       ├── base_page.py
│       ├── hall_page.py
│       ├── room_page.py
│       └── social_page.py
├── test_cases/                      # YAML测试用例
│   ├── hall/
│   │   └── test_hall.yaml
│   ├── room/
│   │   └── test_room.yaml
│   └── social/
│       └── test_social.yaml
├── generated_tests/                 # 生成的测试代码
│   ├── test_hall.py
│   ├── test_room.py
│   └── test_social.py
├── generated_proto/                 # 生成的protobuf代码
│   ├── client/
│   └── shared/
├── reports/                         # 测试报告
│   ├── test_report_*.html          # HTML报告
│   ├── test_report_*.xlsx          # Excel报告
│   └── test_cases_complete.xlsx    # 测试用例Excel
└── jinn_server/                     # jinn_server仓库（只读）
```

## 📝 测试用例格式

### YAML 格式示例

```yaml
test_cases:
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
            nickname: TestName_123
      error_code: 200
      error_message: ''
    jsonpath_assertion: $.success == true && $.error_code == 200
    remark: 正常业务流程验证
  
  UpdateNickname_正常:
    description: UpdateNickname_正常调用
    priority: P0
    preconditions: 已登录
    dimension: 正常
    request:
      nickname:
        value: "NewNickname"
        type: string
    expected_status: '200'
    expected_response:
      success: true
      response:
        updatenickname:
          nickname: "NewNickname"
      error_code: 200
    jsonpath_assertion: $.success == true && $.error_code == 200
    remark: 正常业务流程验证
```

### 请求参数格式

YAML 中的请求参数支持两种格式：

1. **简单格式**（直接值）：
```yaml
request:
  nickname: "TestNickname"
  game_mode: 1
```

2. **详细格式**（带类型信息）：
```yaml
request:
  nickname:
    value: "TestNickname"
    type: string
  game_mode:
    value: 1
    type: int32
```

## 📊 测试报告

### HTML 报告

**位置**：`reports/test_report_*.html`

**包含内容**：
- 📈 总接口数、通过数、失败数统计
- 📑 按服务分页展示
- 🔍 每个接口的详细信息：
  - 接口字段（从proto定义提取）
  - 请求参数（带类型信息）
  - 实际输出（服务器返回的完整数据）
  - 响应码
  - 错误原因（如有）
  - 前置条件
  - 问题分析

### Excel 报告

**位置**：`reports/test_report_*.xlsx`

**包含内容**：
- 测试结果汇总表
- 各服务详细测试结果
- 包含所有 HTML 报告中的信息
- 支持筛选和排序

### 测试用例 Excel

**位置**：`reports/test_cases_complete.xlsx`

**包含内容**：
- 五维度测试用例（正常/参数异常/业务异常/权限安全/性能边界）
- 每个用例的完整信息
- **实际服务器返回**（真实API调用结果）
- **状态标记**（通过/不通过，带颜色）

## 🔧 命令行参数

```bash
python3 main.py [选项]

选项:
  --run              运行测试并生成报告
  --skip-git-check   跳过Git更新检查（适用于所有命令）
  --generate-cases   生成五维度测试用例Excel（从YAML文件，并实际运行接口）
  --generate-yaml    生成五维度测试用例YAML（基于最新接口定义）
  --use-pytest       使用pytest框架和PO模式生成测试代码（默认使用unittest）
```

### 命令组合示例

```bash
# 生成测试用例，不更新Git
python3 main.py --generate-cases --skip-git-check

# 运行测试，不更新Git
python3 main.py --run --skip-git-check

# 仅更新代码和生成测试代码，不运行测试
python3 main.py

# 使用pytest框架运行测试
python3 main.py --use-pytest --run
```

## 🎯 工作流程

```
1. 配置服务器地址和Git仓库
   ↓
2. 运行 python3 main.py --run
   ↓
3. 自动拉取Git代码（如有更新）
   ↓
4. 测试服务器连接
   ↓
5. 解析protobuf接口定义
   ↓
6. 生成Python测试代码
   ↓
7. 执行测试（真实API调用）
   ↓
8. 生成HTML和Excel报告
```

## 💡 使用提示

### 首次使用

1. **配置服务器地址**：编辑 `config.yaml`，设置正确的服务器地址
2. **运行测试**：`python3 main.py --run`，会自动拉取代码
3. **查看报告**：在 `reports/` 目录查看 HTML 和 Excel 报告

### 日常使用

- **快速测试**：`python3 main.py --run --skip-git-check`（跳过Git更新，更快）
- **更新接口**：`python3 main.py`（只更新代码和生成测试代码）
- **生成用例**：`python3 main.py --generate-cases`（生成完整的测试用例Excel）

### 注意事项

- ✅ 首次运行会自动拉取Git仓库代码
- ✅ 测试用例可以手动编写YAML文件，也可以使用生成器自动生成
- ✅ 报告会自动保存在 `reports/` 目录，只保留最新的3个报告
- ✅ 所有API调用都是真实连接服务器，确保测试环境可用
- ⚠️ 生成测试用例时会自动更新Git代码，确保基于最新接口定义
- ⚠️ 如果服务器不可用，测试会失败，但会生成详细的错误报告

## ❓ 常见问题

### Q: 测试用例生成会拉取新代码吗？

**A**: 是的。`--generate-cases` 和 `--generate-yaml` 默认会先更新Git代码，确保基于最新接口定义。如果不想更新，可以使用 `--skip-git-check`。

### Q: 如何只更新代码不运行测试？

**A**: 运行 `python3 main.py`（不带 `--run` 参数）即可。

### Q: 报告保存在哪里？

**A**: 
- HTML报告：`reports/test_report_*.html`
- Excel报告：`reports/test_report_*.xlsx`
- 测试用例Excel：`reports/test_cases_complete.xlsx`

### Q: 如何查看测试用例？

**A**: 
- Excel格式：运行 `python3 main.py --generate-cases`，查看 `reports/test_cases_complete.xlsx`
- YAML格式：运行 `python3 main.py --generate-yaml`，查看 `test_cases/` 目录下的YAML文件

### Q: 测试失败怎么办？

**A**: 
1. 查看HTML报告中的"问题分析"部分
2. 检查服务器是否可用
3. 检查测试用例参数是否正确
4. 查看错误信息和响应码

### Q: 如何添加新的服务？

**A**: 
1. 在 `config.yaml` 的 `services` 部分添加新服务配置
2. 在 `framework/client.py` 中添加服务的方法映射
3. 运行 `python3 main.py --generate-yaml` 生成测试用例

## 🔄 代码重构

框架代码重构建议请参考 [REFACTORING.md](./REFACTORING.md) 文档。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[根据项目实际情况填写]

---

**Made with ❤️ for API Testing**
