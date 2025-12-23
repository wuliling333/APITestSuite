#!/bin/bash
# 安装所有依赖脚本

echo "=========================================="
echo "正在安装所有依赖..."
echo "=========================================="

cd /Users/rourou/Desktop/APITestSuite
source .venv/bin/activate

# 安装所有依赖
echo "安装 pyyaml..."
python3 -m pip install --no-cache-dir pyyaml || echo "⚠ pyyaml 安装失败"

echo "安装 requests..."
python3 -m pip install --no-cache-dir requests || echo "⚠ requests 安装失败"

echo "安装 jinja2..."
python3 -m pip install --no-cache-dir jinja2 || echo "⚠ jinja2 安装失败"

echo "安装 pytest..."
python3 -m pip install --no-cache-dir pytest || echo "⚠ pytest 安装失败"

echo "安装 pytest-html..."
python3 -m pip install --no-cache-dir pytest-html || echo "⚠ pytest-html 安装失败"

echo "安装 openpyxl..."
python3 -m pip install --no-cache-dir openpyxl || echo "⚠ openpyxl 安装失败"

echo "安装 protobuf..."
python3 -m pip install --no-cache-dir protobuf || echo "⚠ protobuf 安装失败"

echo ""
echo "=========================================="
echo "验证安装..."
echo "=========================================="

python3 -c "import yaml; print('✓ yaml')" || echo "✗ yaml"
python3 -c "import requests; print('✓ requests')" || echo "✗ requests"
python3 -c "import jinja2; print('✓ jinja2')" || echo "✗ jinja2"
python3 -c "import pytest; print('✓ pytest')" || echo "✗ pytest"
python3 -c "import openpyxl; print('✓ openpyxl')" || echo "✗ openpyxl"
python3 -c "import google.protobuf; print('✓ protobuf')" || echo "✗ protobuf"

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="

