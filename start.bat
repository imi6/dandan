@echo off
echo ====================================
echo   DanDanPlay Python 启动脚本
echo ====================================
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 启动服务器
echo 正在启动服务器...
echo 访问地址: http://localhost:8888
echo API文档: http://localhost:8888/docs
echo.
echo 按 Ctrl+C 停止服务器
echo ====================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload

pause