#!/usr/bin/env pwsh
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "   DanDanPlay Python 启动脚本" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 激活虚拟环境
& .\venv\Scripts\Activate.ps1

# 启动服务器
Write-Host "正在启动服务器..." -ForegroundColor Green
Write-Host "访问地址: " -NoNewline
Write-Host "http://localhost:8888" -ForegroundColor Yellow
Write-Host "API文档: " -NoNewline
Write-Host "http://localhost:8888/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Red
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 运行服务器
python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload