#!/bin/bash
# 安装依赖脚本

echo "正在安装依赖..."

# 激活虚拟环境
source .venv/bin/activate

# 如果虚拟环境的pip有问题，尝试使用python -m pip
if ! pip install pyyaml requests jinja2 pytest pytest-html openpyxl protobuf 2>/dev/null; then
    echo "使用 python -m pip 安装..."
    python3 -m pip install pyyaml requests jinja2 pytest pytest-html openpyxl protobuf
fi

echo "验证安装..."
python3 -c "import yaml; print('✓ yaml 模块安装成功')" || echo "✗ yaml 模块安装失败"

echo "完成！"

