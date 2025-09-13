# 🐳 DanPlay Docker部署指南

## 📋 目录

- [快速开始](#快速开始)
- [部署方式](#部署方式)
- [配置说明](#配置说明)
- [高级配置](#高级配置)
- [故障排除](#故障排除)
- [生产部署建议](#生产部署建议)

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

### 一键部署

#### Linux/Mac
```bash
# 赋予执行权限
chmod +x deploy.sh

# 启动服务
./deploy.sh start

# 启动服务（包含Nginx）
./deploy.sh start --with-nginx

# 启动所有服务
./deploy.sh start --with-all
```

#### Windows PowerShell
```powershell
# 启动服务
.\deploy.ps1 start

# 启动服务（包含Nginx）
.\deploy.ps1 start -WithNginx

# 启动所有服务
.\deploy.ps1 start -WithAll
```

访问 http://localhost:8000 即可使用！

## 📦 部署方式

### 1. 基础部署（仅应用）

最简单的部署方式，只启动核心应用：

```bash
# 构建并启动
docker-compose up -d danplay

# 或使用部署脚本
./deploy.sh start
```

**适用场景：**
- 个人使用
- 开发测试
- 小规模部署

### 2. 带Nginx反向代理

包含Nginx提供更好的性能和安全性：

```bash
# 使用docker-compose
docker-compose --profile with-nginx up -d

# 或使用部署脚本
./deploy.sh start --with-nginx
```

**优势：**
- 静态文件缓存
- Gzip压缩
- SSL支持
- 负载均衡准备

### 3. 带Redis缓存

添加Redis提升性能：

```bash
# 使用docker-compose
docker-compose --profile with-redis up -d

# 或使用部署脚本
./deploy.sh start --with-redis
```

**优势：**
- API响应缓存
- 会话存储
- 匹配结果缓存

### 4. 完整部署

包含所有组件的生产级部署：

```bash
# 使用docker-compose
docker-compose --profile with-nginx --profile with-redis up -d

# 或使用部署脚本
./deploy.sh start --with-all
```

## ⚙️ 配置说明

### 环境变量配置

1. **复制配置文件**
```bash
cp .env.docker .env
```

2. **编辑 `.env` 文件**

```env
# 必须修改
SECRET_KEY=your-unique-secret-key-here

# 基础配置
DEBUG=false
EXTERNAL_PORT=8000

# 上传限制（5GB）
MAX_UPLOAD_SIZE=5368709120

# API配置
DANDAN_API_BASE_URL=https://api.dandanplay.net/api/v2
DANDAN_PROXY_URL=  # 可选代理

# 性能配置
WORKERS=4
```

### 数据卷说明

| 本地路径 | 容器路径 | 说明 |
|---------|---------|------|
| `./uploads` | `/app/uploads` | 上传的视频文件 |
| `./user_settings.json` | `/app/user_settings.json` | 用户设置 |
| `./logs` | `/app/logs` | 应用日志 |
| `./nginx/ssl` | `/etc/nginx/ssl` | SSL证书（可选） |

## 🔧 高级配置

### 启用HTTPS

1. **准备SSL证书**
```bash
mkdir -p nginx/ssl
# 将证书文件放入 nginx/ssl/
# - cert.pem (证书)
# - key.pem (私钥)
```

2. **修改nginx配置**

编辑 `nginx/nginx.conf`，取消HTTPS部分的注释：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... 其他配置
}
```

3. **重启服务**
```bash
./deploy.sh restart --with-nginx
```

### 自定义构建

修改 `Dockerfile` 添加额外依赖：

```dockerfile
# 添加系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# 添加Python包
RUN pip install \
    redis \
    celery \
    pillow
```

### 性能优化

1. **增加Worker数量**
```env
WORKERS=8  # 根据CPU核心数调整
```

2. **调整上传限制**
```env
MAX_UPLOAD_SIZE=10737418240  # 10GB
```

3. **启用Redis缓存**
```bash
./deploy.sh start --with-redis
```

## 🔍 常用命令

### 服务管理

```bash
# 查看服务状态
./deploy.sh status
docker-compose ps

# 查看日志
./deploy.sh logs
docker-compose logs -f --tail=100

# 停止服务
./deploy.sh stop
docker-compose down

# 重启服务
./deploy.sh restart
docker-compose restart

# 清理所有（危险！）
./deploy.sh clean
docker-compose down -v --rmi all
```

### 进入容器

```bash
# 进入应用容器
docker exec -it danplay_app bash

# 进入Python shell
docker exec -it danplay_app python

# 查看容器内文件
docker exec danplay_app ls -la /app
```

### 备份与恢复

```bash
# 备份数据
docker run --rm -v danplay_uploads:/data -v $(pwd):/backup \
    alpine tar czf /backup/uploads_backup.tar.gz -C /data .

# 备份设置
cp user_settings.json user_settings.backup.json

# 恢复数据
docker run --rm -v danplay_uploads:/data -v $(pwd):/backup \
    alpine tar xzf /backup/uploads_backup.tar.gz -C /data
```

## ❗ 故障排除

### 1. 端口被占用

**错误信息：**
```
Error: bind: address already in use
```

**解决方案：**
```bash
# 修改 .env 中的端口
EXTERNAL_PORT=8001
NGINX_PORT=8080
```

### 2. 权限问题

**错误信息：**
```
Permission denied
```

**解决方案：**
```bash
# Linux/Mac
chmod 755 uploads
chmod 644 user_settings.json

# 或重新构建
docker-compose build --no-cache
```

### 3. 内存不足

**错误信息：**
```
Container killed due to memory limit
```

**解决方案：**
```yaml
# 在 docker-compose.yml 中添加资源限制
services:
  danplay:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### 4. 上传失败

**解决方案：**
```bash
# 检查磁盘空间
df -h

# 检查权限
ls -la uploads/

# 查看错误日志
docker-compose logs danplay | grep ERROR
```

## 🚀 生产部署建议

### 1. 安全配置

- ✅ **修改SECRET_KEY**：使用强随机密钥
- ✅ **启用HTTPS**：配置SSL证书
- ✅ **限制访问**：配置防火墙规则
- ✅ **定期更新**：保持Docker镜像最新

### 2. 性能优化

- ✅ **使用Nginx**：处理静态文件和反向代理
- ✅ **启用Redis**：缓存API响应
- ✅ **调整Worker**：根据服务器配置优化
- ✅ **监控资源**：使用Prometheus/Grafana

### 3. 备份策略

- ✅ **定期备份**：每日备份用户数据
- ✅ **异地存储**：备份到云存储
- ✅ **测试恢复**：定期验证备份可用性

### 4. 监控告警

```bash
# 健康检查
curl http://localhost:8000/health

# 查看资源使用
docker stats danplay_app

# 设置告警
# 可以集成 Prometheus + Grafana
```

### 5. 日志管理

```bash
# 配置日志轮转
docker-compose logs --tail=1000 > logs/app_$(date +%Y%m%d).log

# 使用ELK栈进行日志分析
# Elasticsearch + Logstash + Kibana
```

## 📞 获取帮助

遇到问题？

1. 查看日志：`./deploy.sh logs`
2. 查看[常见问题](FAQ.md)
3. 提交[Issue](https://github.com/yourusername/danplay/issues)
4. 联系支持：your-email@example.com

---

祝您部署顺利！🎉