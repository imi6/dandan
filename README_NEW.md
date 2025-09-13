# 🎬 DanPlay - 现代化弹幕视频播放器

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

一个基于 FastAPI 构建的现代化本地视频弹幕播放器，让您在观看本地视频时也能享受弹幕的乐趣。

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [技术架构](#-技术架构) • [API文档](#-api文档) • [贡献指南](#-贡献指南)

</div>

---

## ✨ 功能特点

### 🎯 核心功能
- **📁 本地视频播放** - 支持拖拽上传，批量处理，支持 MP4/MKV/AVI 等主流格式
- **🔍 智能弹幕匹配** - 基于视频指纹自动匹配弹幕，无需手动搜索
- **💬 多源弹幕支持** - 兼容 B站、A站等多个弹幕源
- **🎨 现代化UI设计** - 响应式布局，支持深色模式，流畅的动画效果

### 🚀 进阶特性
- **⚙️ 丰富的设置选项** - 播放器内核切换、弹幕样式自定义、网络代理配置
- **📊 实时通信** - WebSocket 支持，实时状态同步
- **🔄 格式转换** - 支持多种弹幕格式互转（XML/ASS/JSON）
- **💾 智能缓存** - 匹配结果缓存，提升二次加载速度
- **📱 响应式设计** - 完美适配桌面和移动设备

## 🖼️ 界面预览

<details>
<summary>点击查看界面截图</summary>

### 主界面
- 现代化设计风格
- 渐变背景动效
- 直观的拖拽上传区域

### 设置页面
- 分类清晰的设置项
- 实时预览效果
- 导入/导出配置

### 播放界面
- 多种播放器内核可选
- 弹幕实时渲染
- 播放控制栏

</details>

## 🚀 快速开始

### 环境要求

- Python 3.11 或更高版本
- 现代浏览器（Chrome/Firefox/Edge/Safari）
- 可选：ffmpeg（用于视频处理）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/danplay.git
cd danplay
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，配置必要的参数
# 主要配置项：
# - SECRET_KEY: 应用密钥
# - DANDAN_API_BASE_URL: 弹弹play API地址
# - MAX_UPLOAD_SIZE: 最大上传文件大小
```

5. **运行应用**
```bash
# 开发模式
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 生产模式
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

6. **访问应用**

打开浏览器访问 http://localhost:8000

## 🏗️ 技术架构

### 后端技术栈
- **框架**: FastAPI - 高性能异步Web框架
- **异步**: asyncio + aiofiles - 异步I/O操作
- **HTTP客户端**: httpx - 现代HTTP客户端
- **WebSocket**: websockets - 实时双向通信
- **验证**: Pydantic - 数据验证和设置管理

### 前端技术栈
- **核心**: 原生 HTML5 + CSS3 + JavaScript ES6+
- **样式**: 现代CSS（Grid/Flexbox/CSS变量）
- **动画**: CSS动画 + JavaScript动效
- **播放器**: 支持多种播放器内核（NPlayer/ArtPlayer/DPlayer）

### 项目结构
```
danplay/
├── app/                    # 应用主目录
│   ├── api/               # API路由端点
│   │   ├── video.py      # 视频相关API
│   │   ├── danmaku.py    # 弹幕相关API
│   │   ├── match.py      # 匹配相关API
│   │   ├── websocket.py  # WebSocket处理
│   │   └── settings.py   # 设置相关API
│   ├── core/              # 核心功能模块
│   │   ├── exceptions.py # 异常处理
│   │   └── websocket.py  # WebSocket管理
│   ├── services/          # 业务逻辑层
│   │   ├── danmaku_service.py  # 弹幕处理服务
│   │   ├── dandan_service.py   # 弹弹play API服务
│   │   └── video_service.py    # 视频处理服务
│   ├── schemas/           # 数据模型定义
│   ├── config.py         # 配置管理
│   └── main.py           # 应用入口
├── static/                # 静态资源
│   ├── css/              # 样式文件
│   │   └── modern.css    # 现代化样式
│   └── js/               # JavaScript文件
│       ├── app.js        # 主应用逻辑
│       ├── playlist.js   # 播放列表管理
│       └── settings-manager.js # 设置管理器
├── templates/             # HTML模板
│   ├── index.html        # 主页
│   ├── settings.html     # 设置页
│   └── splash.html       # 启动页
├── uploads/              # 上传文件目录
├── docs/                 # 文档目录
├── tests/                # 测试文件
├── .env.example          # 环境变量示例
├── requirements.txt      # Python依赖
├── Dockerfile           # Docker镜像构建
└── docker-compose.yml   # Docker编排配置
```

## 📡 API文档

### 自动生成文档
启动应用后，访问以下地址查看交互式API文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要API端点

#### 视频管理
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/video/upload` | 上传视频文件 |
| GET | `/api/video/stream/{video_id}` | 流式播放视频 |
| GET | `/api/video/md5/{video_id}` | 获取视频MD5指纹 |
| DELETE | `/api/video/{video_id}` | 删除视频 |

#### 弹幕匹配
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/match/` | 根据MD5匹配视频 |
| GET | `/api/match/search` | 搜索动画作品 |
| GET | `/api/match/anime/{anime_id}` | 获取动画详情 |

#### 弹幕处理
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/danmaku/{episode_id}` | 获取弹幕数据 |
| POST | `/api/danmaku/external` | 获取第三方弹幕 |
| POST | `/api/danmaku/parse/xml` | 解析XML弹幕 |
| POST | `/api/danmaku/convert` | 转换弹幕格式 |

#### 设置管理
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/settings` | 获取用户设置 |
| POST | `/api/settings` | 保存用户设置 |
| DELETE | `/api/settings` | 重置为默认设置 |

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

### Docker Compose配置
```yaml
version: '3.8'
services:
  danplay:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./user_settings.json:/app/user_settings.json
    environment:
      - SECRET_KEY=your-secret-key-here
    restart: unless-stopped
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
| `DANDAN_PROXY_URL` | - | 代理地址（可选） |

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

### 报告问题
如果您发现了bug或有功能建议，请[创建Issue](https://github.com/yourusername/danplay/issues)

## 📝 更新日志

### v1.0.0 (2024-01)
- 🎉 首次发布
- ✨ 现代化UI重构
- 🚀 性能优化
- 🔧 完善设置功能
- 🐛 修复已知问题

查看[完整更新日志](CHANGELOG.md)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [弹弹play](https://www.dandanplay.com/) - 优秀的弹幕播放器
- [弹弹play开放平台](https://api.dandanplay.net) - 提供API支持
- [FastAPI](https://fastapi.tiangolo.com) - 现代Web框架
- 所有贡献者和用户的支持

## 📮 联系方式

- 项目主页: [https://github.com/yourusername/danplay](https://github.com/yourusername/danplay)
- Issue反馈: [https://github.com/yourusername/danplay/issues](https://github.com/yourusername/danplay/issues)
- Email: your-email@example.com

---

<div align="center">
  <sub>用 ❤️ 打造，让本地视频观看更有趣</sub>
</div>