#!/bin/bash
# 生成Python protobuf代码

set -e

PROTO_DIR="jinn_server/config/proto_jinn"
OUTPUT_DIR="generated_proto"

echo "生成Python protobuf代码..."
echo "Proto目录: $PROTO_DIR"
echo "输出目录: $OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR/shared"
mkdir -p "$OUTPUT_DIR/client"

# 检查protoc
if ! command -v protoc &> /dev/null; then
    echo "错误: protoc未安装，请先安装protobuf编译器"
    exit 1
fi

# 生成shared protobuf
echo "生成shared protobuf..."
protoc --proto_path="$PROTO_DIR" \
    --python_out="$OUTPUT_DIR" \
    "$PROTO_DIR/shared/shared.proto" \
    "$PROTO_DIR/shared/head.proto" \
    "$PROTO_DIR/shared/gate.proto" 2>&1 || echo "警告: shared proto生成失败"

# 生成client protobuf
echo "生成client protobuf..."
for proto_file in "$PROTO_DIR/client"/*.proto; do
    if [ -f "$proto_file" ]; then
        echo "  处理: $(basename $proto_file)"
        protoc --proto_path="$PROTO_DIR" \
            --python_out="$OUTPUT_DIR" \
            "$proto_file" 2>&1 || echo "警告: $(basename $proto_file) 生成失败"
    fi
done

echo "✓ Python protobuf代码生成完成"

