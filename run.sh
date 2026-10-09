#!/bin/bash
cd "$(dirname "$0")"

# 首次运行时自动创建虚拟环境并安装依赖
if [ ! -f venv/bin/activate ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi
source venv/bin/activate

for i in ./*.pdf
do
    python3 ./crop.py "${i}"
done
