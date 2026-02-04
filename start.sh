#!/bin/bash

# =================================================================
# Landing Page Analyser 自动化启动脚本 (针对 Python 3.14 优化版)
# =================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}       Landing Page Analyser 检查并启动程序          ${NC}"
echo -e "${BLUE}====================================================${NC}"

# --- 1. 配置文件检查 ---
echo -e "${YELLOW}[1/5] 检查配置文件...${NC}"
if [ ! -d "land-page-analysis-backend" ]; then
    echo -e "${RED}错误: 找不到 backend 目录。请在项目根目录下运行。${NC}"
    exit 1
fi

cd land-page-analysis-backend

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}已创建 .env，请确保其中的数据库密码正确。${NC}"
    else
        echo -e "${RED}错误: 缺少 .env.example 文件。${NC}"
        exit 1
    fi
fi

# --- 2. 准备 Python 虚拟环境 ---
echo -e "${YELLOW}[2/5] 配置 Python 虚拟环境...${NC}"
if [ ! -d ".myvenv" ]; then
    echo -e "${BLUE}正在创建虚拟环境 (Python 3.14)...${NC}"
    python3 -m venv .myvenv
fi

# 激活虚拟环境
source .myvenv/bin/activate

# 同步依赖
echo -e "${BLUE}正在同步依赖库...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt | grep -v "already satisfied"
pip install pymysql python-dotenv -q

# --- 3. 数据库验证 (修复 Python 3.14 兼容性) ---
echo -e "${YELLOW}[3/5] 验证数据库连接...${NC}"

DB_CHECK_RESULT=$(python3 <<EOF
import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path

# 针对 Python 3.14 的核心修复：显式指定路径，避免 find_dotenv() 报错
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

try:
    host = os.getenv('HOST', '127.0.0.1')
    user = os.getenv('USR')
    raw_pass = os.getenv('PASSWORD') or ''
    # 移除引号
    password = raw_pass.strip('\"').strip("'")
    db = os.getenv('DATABASE')
    port = int(os.getenv('PORT', 3306))

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port,
        connect_timeout=5
    )
    conn.close()
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
EOF
)

if [[ "$DB_CHECK_RESULT" != "SUCCESS" ]]; then
    echo -e "${RED}数据库连接失败！${NC}"
    echo -e "${RED}错误详情: $DB_CHECK_RESULT${NC}"
    echo -e "${YELLOW}提示: 如果 Navicat 能连，请核对 .env 中的 HOST 是否为 127.0.0.1。${NC}"
    exit 1
else
    echo -e "${GREEN}数据库连接验证通过！${NC}"
fi

# --- 4. 后端启动 ---
echo -e "${YELLOW}[4/5] 启动后端服务...${NC}"

if [ ! -d "logs" ]; then
    mkdir logs
fi

# 启动并将日志输出到 logs/backend.log
python app.py > ./logs/backend.log 2>&1 &
BACKEND_PID=$!

# --- 5. 前端启动 ---
echo -e "${YELLOW}[5/5] 准备前端环境...${NC}"
cd ../land-page-analysis-frontend

if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}正在安装前端依赖 (npm install)...${NC}"
    npm install
fi

echo -e "${BLUE}----------------------------------------------------${NC}"
echo -e "${GREEN}所有服务已就绪！${NC}"
echo -e "${BLUE}后端日志位置: land-page-analysis-backend/logs/backend.log${NC}"
echo -e "${BLUE}前端地址: http://localhost:5173${NC}"
echo -e "${BLUE}按 Ctrl+C 停止所有服务${NC}"
echo -e "${BLUE}----------------------------------------------------${NC}"

# 信号捕获：退出时杀死后端进程
trap "kill $BACKEND_PID; echo -e '\n${RED}服务已停止。${NC}'; exit" SIGINT SIGTERM

npm run dev