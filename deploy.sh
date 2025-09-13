#!/bin/bash

# DanPlay Docker部署脚本
# 使用方法: ./deploy.sh [选项]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认值
ACTION="start"
PROFILE=""
BUILD_ONLY=false

# 显示帮助
show_help() {
    echo "DanPlay Docker部署脚本"
    echo ""
    echo "使用方法: ./deploy.sh [选项]"
    echo ""
    echo "选项:"
    echo "  start          启动服务（默认）"
    echo "  stop           停止服务"
    echo "  restart        重启服务"
    echo "  build          构建镜像"
    echo "  logs           查看日志"
    echo "  status         查看服务状态"
    echo "  clean          清理所有容器和镜像"
    echo ""
    echo "配置选项:"
    echo "  --with-nginx   包含Nginx反向代理"
    echo "  --with-redis   包含Redis缓存"
    echo "  --with-all     包含所有可选服务"
    echo ""
    echo "示例:"
    echo "  ./deploy.sh start                # 启动基础服务"
    echo "  ./deploy.sh start --with-nginx   # 启动服务和Nginx"
    echo "  ./deploy.sh start --with-all     # 启动所有服务"
    echo "  ./deploy.sh logs                 # 查看日志"
}

# 检查Docker和Docker Compose
check_requirements() {
    echo -e "${YELLOW}检查环境要求...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker未安装${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}错误: Docker Compose未安装${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Docker和Docker Compose已安装${NC}"
}

# 检查并创建.env文件
check_env_file() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}未找到.env文件，创建默认配置...${NC}"
        cp .env.docker .env
        echo -e "${GREEN}✓ 已创建.env文件，请修改其中的配置${NC}"
        echo -e "${YELLOW}特别注意: 请修改SECRET_KEY的值！${NC}"
        read -p "按Enter继续..." 
    fi
}

# 构建镜像
build_image() {
    echo -e "${YELLOW}构建Docker镜像...${NC}"
    docker-compose build
    echo -e "${GREEN}✓ 镜像构建完成${NC}"
}

# 启动服务
start_services() {
    echo -e "${YELLOW}启动服务...${NC}"
    
    if [ -n "$PROFILE" ]; then
        docker-compose --profile $PROFILE up -d
    else
        docker-compose up -d danplay
    fi
    
    echo -e "${GREEN}✓ 服务已启动${NC}"
    echo ""
    echo "访问地址:"
    echo "  - 应用: http://localhost:8000"
    
    if [[ "$PROFILE" == *"nginx"* ]]; then
        echo "  - Nginx: http://localhost"
    fi
    
    if [[ "$PROFILE" == *"redis"* ]]; then
        echo "  - Redis: localhost:6379"
    fi
}

# 停止服务
stop_services() {
    echo -e "${YELLOW}停止服务...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ 服务已停止${NC}"
}

# 重启服务
restart_services() {
    stop_services
    start_services
}

# 查看日志
show_logs() {
    docker-compose logs -f --tail=100
}

# 查看状态
show_status() {
    echo -e "${YELLOW}服务状态:${NC}"
    docker-compose ps
}

# 清理环境
clean_all() {
    echo -e "${RED}警告: 这将删除所有容器、镜像和数据卷！${NC}"
    read -p "确定要继续吗？(y/N): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo -e "${YELLOW}清理中...${NC}"
        docker-compose down -v --rmi all
        echo -e "${GREEN}✓ 清理完成${NC}"
    else
        echo "已取消"
    fi
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        start|stop|restart|build|logs|status|clean)
            ACTION=$1
            shift
            ;;
        --with-nginx)
            PROFILE="${PROFILE:+$PROFILE,}with-nginx"
            shift
            ;;
        --with-redis)
            PROFILE="${PROFILE:+$PROFILE,}with-redis"
            shift
            ;;
        --with-all)
            PROFILE="with-nginx,with-redis"
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 主流程
check_requirements
check_env_file

case $ACTION in
    start)
        build_image
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    build)
        build_image
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    *)
        echo -e "${RED}未知操作: $ACTION${NC}"
        show_help
        exit 1
        ;;
esac