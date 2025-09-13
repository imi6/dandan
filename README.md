# 🎬 DanPlay - 现代化弹幕视频播放器

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**一个基于 FastAPI 构建的现代化本地视频弹幕播放器**

让您在观看本地视频时也能享受弹幕带来的乐趣，支持自动匹配弹幕、多播放器内核、实时设置同步等功能。

[在线演示](#) • [功能特点](#-功能特点) • [快速开始](#-快速开始) • [Docker部署](#-docker部署) • [开发文档](#-开发文档)

<img src="docs/screenshots/main.png" alt="主界面" width="800">

</div>

---

## ✨ 功能特点

### 🎯 核心功能

| 功能 | 描述 |
|------|------|
| **📁 本地视频播放** | 支持拖拽上传、批量处理，兼容 MP4/MKV/AVI/FLV 等主流格式 |
| **🔍 智能弹幕匹配** | 基于视频MD5指纹自动匹配弹幕，无需手动搜索 |
| **💬 多源弹幕支持** | 兼容 B站、A站、D站等多个弹幕源，支持XML弹幕导入 |
| **🎨 现代化UI设计** | 渐变背景、毛玻璃效果、响应式布局、深色模式支持 |
| **⚙️ 丰富设置选项** | 播放器内核切换、弹幕样式自定义、网络代理配置 |
| **💾 设置云同步** | 支持设置导入导出，便于备份和迁移 |

### 🚀 进阶特性

- **WebSocket 实时通信** - 状态实时同步，多端协作
- **弹幕格式转换** - 支持 XML/ASS/JSON 等格式互转
- **智能缓存机制** - 匹配结果缓存，减少API调用
- **多播放器内核** - NPlayer、ArtPlayer、DPlayer 可选
- **硬件加速支持** - GPU解码加速，降低CPU占用
- **批量处理能力** - 支持播放列表、连续播放

---

## 🔧 技术栈

<table>
<tr>
<td width="50%">

### 🔙 后端

- **FastAPI** - 高性能异步Web框架
- **Python 3.11+** - 最新Python特性
- **asyncio** - 异步I/O支持
- **httpx** - 现代HTTP客户端
- **Pydantic** - 数据验证
- **websockets** - 实时通信
- **aiofiles** - 异步文件处理

</td>
<td width="50%">

### 🌐 前端

- **HTML5** - 语义化标签
- **CSS3** - 现代布局与动画
- **JavaScript ES6+** - 原生开发
- **NPlayer** - 主播放器内核
- **WebSocket** - 实时通信
- **LocalStorage** - 本地存储
- **Service Worker** - 离线支持

</td>
</tr>
</table>

---

## 🚀 快速开始

### 💻 本地开发

#### 1️⃣ 环境要求

- Python 3.11+
- Git
- 现代浏览器
- 可选: ffmpeg (视频处理)

#### 2️⃣ 安装步骤

```bash
# 克隆项目
git clone https://github.com/yourusername/danplay.git
cd danplay

# 创建虚拟环境(Windows)
python -m venv venv
venv\Scripts\activate

# 创建虚拟环境 (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env

# 启动服务
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### 3️⃣ 访问应用

打开浏览器访问: **http://localhost:8000**

---

## 🐳 Docker部署

### 🎯 一键部署

#### Windows PowerShell
```powershell
# 启动基础服务
.\deploy.ps1 start

# 启动完整服务（包含Nginx和Redis）
.\deploy.ps1 start -WithAll
```

#### Linux/Mac
```bash
# 赋予执行权限
chmod +x deploy.sh

# 启动基础服务
./deploy.sh start

# 启动完整服务
./deploy.sh start --with-all
```

### 📦 Docker Compose

```bash
# 基础部署
docker-compose up -d

# 包含Nginx
docker-compose --profile with-nginx up -d

# 包含Redis
docker-compose --profile with-redis up -d

# 完整部署
docker-compose --profile with-nginx --profile with-redis up -d
```

### 🔧 配置说明

```env
# .env 文件配置
SECRET_KEY=your-secret-key  # 必须修改
DEBUG=false
EXTERNAL_PORT=8000
MAX_UPLOAD_SIZE=5368709120  # 5GB
DANDAN_API_BASE_URL=https://api.dandanplay.net/api/v2
```

查看详细部署文档: [📚DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)

---

## 📡 API文档

### 📖 交互式文档

启动应用后访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 📦 主要API

<details>
<summary>点击展开API列表</summary>

#### 视频管理
```
POST   /api/video/upload          # 上传视频
GET    /api/video/stream/{id}     # 流式播放
GET    /api/video/md5/{id}        # 获取MD5
DELETE /api/video/{id}            # 删除视频
```

#### 弹幕匹配
```
POST   /api/match/                # MD5匹配
GET    /api/match/search          # 搜索作品
GET    /api/match/anime/{id}      # 作品详情
```

#### 弹幕处理
```
GET    /api/danmaku/{id}          # 获取弹幕
POST   /api/danmaku/external      # 第三方弹幕
POST   /api/danmaku/parse/xml     # 解析XML
POST   /api/danmaku/convert       # 格式转换
```

#### 设置管理
```
GET    /api/settings              # 获取设置
POST   /api/settings              # 保存设置
DELETE /api/settings              # 重置设置
```

#### WebSocket
```
WS     /ws/{client_id}            # 实时通信
```

</details>

---

## 📦 项目结构

```
danplay/
├── app/                    # 📦 应用主目录
│   ├── api/               # 🌐 API路由
│   │   ├── video.py      # 视频管理
│   │   ├── danmaku.py    # 弹幕处理
│   │   ├── match.py      # 弹幕匹配
│   │   ├── websocket.py  # 实时通信
│   │   └── settings.py   # 设置管理
│   ├── core/              # 🔧 核心模块
│   ├── services/          # 💼 业务逻辑
│   ├── schemas/           # 📝 数据模型
│   └── main.py           # 🚀 应用入口
├── static/                # 🎨 静态资源
│   ├── css/              # 样式文件
│   └── js/               # 脚本文件
├── templates/             # 📄 HTML模板
├── nginx/                 # 🌐 Nginx配置
├── docker/                # 🐳 Docker配置
├── docs/                  # 📖 项目文档
├── tests/                 # 🧪 测试文件
├── .env.example           # 🔒 配置示例
├── docker-compose.yml     # 📦 容器编排
├── Dockerfile             # 📦 镜像构建
└── requirements.txt       # 📚 依赖列表
```

## 🐳 Docker部署

### 使用预构建镜像
```bash
docker run -d \
  --name danplay \
  -p 8000:8000 \
  -v ./uploads:/app/uploads \
  -v ./user_settings.json:/app/user_settings.json \
  danplay:latest
```

### 自行构建镜像
```bash
# 构建镜像
docker build -t danplay .

# 使用docker-compose
docker-compose up -d
```

## ⚙️ 配置说明

### 环境变量
| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `SECRET_KEY` | - | 应用密钥（必填） |
| `DEBUG` | `false` | 调试模式 |
| `HOST` | `0.0.0.0` | 监听地址 |
| `PORT` | `8000` | 监听端口 |
| `MAX_UPLOAD_SIZE` | `5368709120` | 最大上传大小(字节) |
| `DANDAN_API_BASE_URL` | `https://api.dandanplay.net/api/v2` | API地址 |

### 用户设置
用户设置保存在 `user_settings.json` 文件中，包含：
- 界面主题和语言
- 播放器配置
- 弹幕样式设置
- 网络代理配置
- 高级选项

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是新功能、bug修复还是文档改进。

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写单元测试
- 更新 README 文档

## 📝 更新日志

### v1.0.0 (2024-01)
- 🎉 首次发布
- ✨ 现代化UI重构
- 🚀 性能优化
- 🔧 完善设置功能
- 🐛 修复已知问题

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [弹弹play](https://www.dandanplay.com/) - 优秀的弹幕播放器
- [FastAPI](https://fastapi.tiangolo.com) - 现代Web框架
- 所有贡献者和用户的支持
---

<div align="center">
  <sub>用 ❤️ 打造，让本地视频观看更有趣</sub>
</div>
