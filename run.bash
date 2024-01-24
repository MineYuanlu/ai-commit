#!/bin/bash

# 获取run.bash所在的目录
wd=$(dirname "${BASH_SOURCE[0]}")

# 调用run.bash执行Python脚本
python3 "$wd/src/entry.py" "$1"
