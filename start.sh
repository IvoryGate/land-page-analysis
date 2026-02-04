#!/bin/bash

# =================================================================
# Landing Page Analyser 自动化启动脚本 (日志存放在 backend/logs/)
# =================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}       Landing Page Analyser 检查并启动程序          ${NC}"
echo -e "${BLUE}====================================================${NC}"

# --- 1. 配置文件检查 ---
echo -e "${YELLOW}[1/5] 检查配置文件...${NC}"
cd land-page-analysis-backend

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}已根据模板创建 .env，请确保数据库密码正确。${NC}"
    else
        echo -e "${RED}错误: 缺少 .env.example 文件。${NC}"
        exit 1
    fi
fi

# --- 2. 数据库验证 ---
echo -e "${YELLOW}[2/5] 验证数据库连接...${NC}"
DB_STATUS=$(python3 -c "
import os
from dotenv import load_dotenv
import pymysql
load_dotenv()
try:
    conn = pymysql.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USR'),
        password=os.getenv('PASSWORD').strip('\"'),
        database=os.getenv('DATABASE'),
        port=int(os.getenv('PORT', 3306)),
        connect_timeout=3
    )
    print('SUCCESS')
    conn.close()
except Exception as e:
    print(e)
" 2>/dev/null)

if [ "$DB_STATUS" != "SUCCESS" ]; then
    echo -e "${RED}数据库连接失败！错误: $DB_STATUS${NC}"
    exit 1
fi

# --- 3. 后端启动 (日志重定向至 ./logs/backend.log) ---
echo -e "${YELLOW}[3/5] 配置 Python 环境并启动后端...${NC}"

# 确保 logs 目录存在
if [ ! -d "logs" ]; then
    mkdir logs
fi

if [ ! -d ".myvenv" ]; then
    python3 -m venv .myvenv
fi

source .myvenv/bin/activate
pip install -r requirements.txt | grep -v "already satisfied"

# 核心修改：将日志放入当前目录下的 logs 文件夹
python app.py > ./logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# --- 4. 前端启动 ---
echo -e "${YELLOW}[4/5] 配置前端环境...${NC}"
cd land-page-analysis-frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

echo -e "${YELLOW}[5/5] 启动前端开发服务器...${NC}"
echo -e "${BLUE}----------------------------------------------------${NC}"
echo -e "${GREEN}服务已启动！${NC}"
echo -e "${BLUE}实时后端日志: tail -f land-page-analysis-backend/logs/backend.log${NC}"
echo -e "${BLUE}前端地址: http://localhost:5173${NC}"
echo -e "${BLUE}----------------------------------------------------${NC}"

# 信号捕获：退出时杀掉后端
trap "kill $BACKEND_PID; echo -e '\n${RED}服务已停止。${NC}'; exit" SIGINT SIGTERM

npm run dev