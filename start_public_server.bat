@echo off
echo 正在启动签名墙网站的公网访问服务器...
echo.

:: 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 警告: 虚拟环境不存在，使用系统Python环境
)

:: 安装依赖
echo 检查并安装依赖...
pip install -r requirements.txt

:: 获取本机IP地址
echo.
echo 获取本机IP地址...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1" %%j in ("%%i") do (
        if not "%%j"=="127.0.0.1" (
            set LOCAL_IP=%%j
            goto :found_ip
        )
    )
)
:found_ip

echo.
echo ================================================================
echo 签名墙网站启动中...
echo 本地访问地址: http://127.0.0.1:8000
if defined LOCAL_IP (
    echo 局域网访问地址: http://%LOCAL_IP%:8000
)
echo.
echo 按 Ctrl+C 停止服务器
echo ================================================================
echo.

:: 启动Django开发服务器
python manage.py runserver 0.0.0.0:8000

pause
