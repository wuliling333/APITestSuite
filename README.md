# APITestSuite

自动化的API测试框架，专门用于测试基于Go语言protobuf定义的微服务API接口。

## 🚀 快速开始 - 一键生成新项目

如果你需要为新的服务器代码仓库创建测试项目，可以使用项目生成器：

```bash
python3 create_project.py <项目名称> <Git仓库地址> [分支名]
```

**示例**:
```bash
python3 create_project.py MyAPITest https://git.17zjh.com/wegame/jinn_server.git v0.1.0
```

这将自动创建完整的项目结构，包括配置文件、框架文件、测试用例目录等。详细说明请查看 [快速开始.md](./快速开始.md)

## 功能特性

- **自动解析**: 从Go protobuf生成文件自动解析API接口定义
- **代码生成**: 自动生成对应的Python测试代码
- **多服务支持**: 支持Hall、Room、Social三大核心服务
- **易于使用**: 提供简洁的命令行工具和配置文件
- **灵活扩展**: 支持自定义测试场景和断言，使用YAML管理测试用例

## 安装

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.yaml` 文件配置服务器地址和路径。

## 使用方法

### 1. 更新Git仓库并生成测试代码

```bash
python3 main.py
```

### 2. 运行测试并生成报告

```bash
python3 main.py --run
```

### 3. 跳过Git检查直接运行测试

```bash
python3 main.py --run --skip-git-check
```

## 项目结构

```
APITestSuite/
├── config.yaml              # 配置文件
├── main.py                  # 主入口
├── framework/               # 框架核心模块
│   ├── config.py           # 配置管理
│   ├── git_updater.py      # Git更新器
│   ├── connection_tester.py # 连接测试器
│   ├── protobuf_parser.py  # Protobuf解析器
│   ├── client.py           # API客户端
│   ├── test_generator.py   # 测试代码生成器
│   ├── test_runner.py      # 测试运行器
│   └── report_generator.py # 报告生成器
├── test_cases/             # YAML测试用例
│   ├── hall/
│   ├── room/
│   └── social/
├── generated_tests/        # 生成的测试代码
├── reports/                # HTML测试报告
└── jinn_server/            # jinn_server仓库（只读）
```

## 测试用例格式

测试用例使用YAML格式，示例：

```yaml
test_cases:
  MethodName:
    description: "接口描述"
    request:
      param1: value1
      param2: value2
```

## 报告

测试报告以HTML格式生成在 `reports/` 目录下，包含：
- 总接口数、通过数、失败数统计
- 按服务分页展示
- 每个接口的输入输出
- 失败原因详情

