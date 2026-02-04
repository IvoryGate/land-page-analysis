#!/bin/bash

echo "正在启动后端服务..."
cd land-page-analysis-backend
if [ -d ".myvenv" ]; then
    source .myvenv/bin/activate
    echo "已进入 myvenv 虚拟环境"
else
    echo "警告: 未找到 myvenv 目录"
fi
BACKEND_PID=$!
cd ..

echo "正在启动前端服务..."
cd land-page-analysis-frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "---------------------------------------"
echo "项目已启动！"
echo "按 Ctrl+C 停止所有进程"
echo "---------------------------------------"

trap "kill $BACKEND_PID $FRONTEND_PID; echo '已停止所有进程'; exit" SIGINT SIGTERM

wait