# DanPlay Docker部署脚本 (Windows PowerShell版本)
# 使用方法: .\deploy.ps1 [选项]

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "restart", "build", "logs", "status", "clean")]
    [string]$Action = "start",
    
    [switch]$WithNginx,
    [switch]$WithRedis,
    [switch]$WithAll,
    [switch]$Help
)

# 颜色输出函数
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# 显示帮助
function Show-Help {
    Write-Host "DanPlay Docker部署脚本" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "使用方法: .\deploy.ps1 [选项]"
    Write-Host ""
    Write-Host "选项:" -ForegroundColor Yellow
    Write-Host "  start          启动服务（默认）"
    Write-Host "  stop           停止服务"
    Write-Host "  restart        重启服务"
    Write-Host "  build          构建镜像"
    Write-Host "  logs           查看日志"
    Write-Host "  status         查看服务状态"
    Write-Host "  clean          清理所有容器和镜像"
    Write-Host ""
    Write-Host "配置选项:" -ForegroundColor Yellow
    Write-Host "  -WithNginx     包含Nginx反向代理"
    Write-Host "  -WithRedis     包含Redis缓存"
    Write-Host "  -WithAll       包含所有可选服务"
    Write-Host ""
    Write-Host "示例:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1 start                 # 启动基础服务"
    Write-Host "  .\deploy.ps1 start -WithNginx      # 启动服务和Nginx"
    Write-Host "  .\deploy.ps1 start -WithAll        # 启动所有服务"
    Write-Host "  .\deploy.ps1 logs                  # 查看日志"
}

# 检查Docker和Docker Compose
function Check-Requirements {
    Write-Host "检查环境要求..." -ForegroundColor Yellow
    
    $dockerExists = Get-Command docker -ErrorAction SilentlyContinue
    if (-not $dockerExists) {
        Write-Host "错误: Docker未安装" -ForegroundColor Red
        Write-Host "请访问 https://www.docker.com/get-started 下载安装Docker Desktop" -ForegroundColor Yellow
        exit 1
    }
    
    $dockerComposeExists = Get-Command docker-compose -ErrorAction SilentlyContinue
    if (-not $dockerComposeExists) {
        Write-Host "错误: Docker Compose未安装" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Docker和Docker Compose已安装" -ForegroundColor Green
}

# 检查并创建.env文件
function Check-EnvFile {
    if (-not (Test-Path .env)) {
        Write-Host "未找到.env文件，创建默认配置..." -ForegroundColor Yellow
        Copy-Item .env.docker .env
        Write-Host "✓ 已创建.env文件，请修改其中的配置" -ForegroundColor Green
        Write-Host "特别注意: 请修改SECRET_KEY的值！" -ForegroundColor Yellow
        Read-Host "按Enter继续..."
    }
}

# 构建镜像
function Build-Image {
    Write-Host "构建Docker镜像..." -ForegroundColor Yellow
    docker-compose build
    Write-Host "✓ 镜像构建完成" -ForegroundColor Green
}

# 启动服务
function Start-Services {
    Write-Host "启动服务..." -ForegroundColor Yellow
    
    $profile = @()
    if ($WithNginx -or $WithAll) { $profile += "with-nginx" }
    if ($WithRedis -or $WithAll) { $profile += "with-redis" }
    
    if ($profile.Count -gt 0) {
        $profileStr = $profile -join ","
        docker-compose --profile $profileStr up -d
    } else {
        docker-compose up -d danplay
    }
    
    Write-Host "✓ 服务已启动" -ForegroundColor Green
    Write-Host ""
    Write-Host "访问地址:" -ForegroundColor Cyan
    Write-Host "  - 应用: http://localhost:8000"
    
    if ($WithNginx -or $WithAll) {
        Write-Host "  - Nginx: http://localhost"
    }
    
    if ($WithRedis -or $WithAll) {
        Write-Host "  - Redis: localhost:6379"
    }
}

# 停止服务
function Stop-Services {
    Write-Host "停止服务..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "✓ 服务已停止" -ForegroundColor Green
}

# 重启服务
function Restart-Services {
    Stop-Services
    Start-Services
}

# 查看日志
function Show-Logs {
    docker-compose logs -f --tail=100
}

# 查看状态
function Show-Status {
    Write-Host "服务状态:" -ForegroundColor Yellow
    docker-compose ps
}

# 清理环境
function Clean-All {
    Write-Host "警告: 这将删除所有容器、镜像和数据卷！" -ForegroundColor Red
    $confirm = Read-Host "确定要继续吗？(y/N)"
    
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "清理中..." -ForegroundColor Yellow
        docker-compose down -v --rmi all
        Write-Host "✓ 清理完成" -ForegroundColor Green
    } else {
        Write-Host "已取消"
    }
}

# 主程序
if ($Help) {
    Show-Help
    exit 0
}

Check-Requirements
Check-EnvFile

switch ($Action) {
    "start" {
        Build-Image
        Start-Services
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Restart-Services
    }
    "build" {
        Build-Image
    }
    "logs" {
        Show-Logs
    }
    "status" {
        Show-Status
    }
    "clean" {
        Clean-All
    }
    default {
        Write-Host "未知操作: $Action" -ForegroundColor Red
        Show-Help
        exit 1
    }
}