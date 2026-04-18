# ☁️ 云端部署完整指南

**更新时间**: 2026-04-18  
**状态**: ✅ 已测试可用

---

## 🎯 部署目标

将 BaziAI API 系统部署到云端，实现：
- ✅ 随时随地访问
- ✅ 无需本地运行
- ✅ 稳定可靠
- ✅ 支持多用户

---

## 📊 云平台对比

| 平台 | 免费额度 | 部署难度 | 推荐度 | 备注 |
|------|---------|---------|--------|------|
| **Render** | ✅ 免费套餐 | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ | **最推荐** |
| **Vercel** | ✅ 免费 | ⭐ 最简单 | ⭐⭐⭐⭐ | 适合静态+API |
| **Fly.io** | ✅ 免费额度 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐ | 性能好 |
| Railway | ⚠️ $5/月 | ⭐⭐ 简单 | ⭐⭐⭐ | 已测试，网络受限 |
| Heroku | ❌ 无免费 | ⭐⭐ 简单 | ⭐⭐ | 需付费 |

---

## 🚀 方案 1: Render（最推荐）

### 为什么选择 Render？
- ✅ 完全免费
- ✅ 支持 Python/Flask
- ✅ 自动 HTTPS
- ✅ 持续部署
- ✅ 无需信用卡

### 部署步骤

#### 1. 准备 GitHub 仓库

确保你的代码已推送到 GitHub：
```bash
git add .
git commit -m "准备云端部署"
git push origin main
```

#### 2. 注册 Render

访问 [https://render.com](https://render.com)
- 使用 GitHub 账号登录
- 授权 Render 访问你的仓库

#### 3. 创建 Web Service

1. 点击 **"New +"** → **"Web Service"**
2. 选择你的 GitHub 仓库
3. 配置如下：

```
Name: bazi-ai-api
Environment: Python 3
Region: Singapore (或其他亚洲节点)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 4. 环境变量（可选）

在 "Environment" 标签添加：
```
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
```

#### 5. 部署

点击 **"Create Web Service"**
- Render 会自动构建和部署
- 等待 5-10 分钟
- 部署成功后会显示 URL

#### 6. 获取 URL

部署完成后，你会得到类似这样的 URL：
```
https://bazi-ai-api.onrender.com
```

### 注意事项

⚠️ **免费套餐限制**：
- 15 分钟无活动后会休眠
- 首次访问需要 30-60 秒唤醒
- 每月 750 小时免费（足够使用）

💡 **解决休眠问题**：
使用 UptimeRobot 每 5 分钟 ping 一次：
1. 访问 [https://uptimerobot.com](https://uptimerobot.com)
2. 添加监控：`https://your-app.onrender.com/health`
3. 间隔设置为 5 分钟

---

## 🌐 方案 2: Vercel（最简单）

### 为什么选择 Vercel？
- ✅ 完全免费
- ✅ 部署超快（< 1 分钟）
- ✅ 自动 HTTPS
- ✅ 全球 CDN

### 部署步骤

#### 1. 安装 Vercel CLI

```bash
npm install -g vercel
```

#### 2. 创建 vercel.json

项目已包含此文件，内容：
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### 3. 部署

```bash
vercel
```

按提示操作：
- 登录 Vercel 账号
- 选择项目设置
- 确认部署

#### 4. 获取 URL

部署成功后会显示：
```
https://bazi-ai-api.vercel.app
```

### 注意事项

⚠️ **Vercel 限制**：
- Selenium 可能无法运行（无头浏览器受限）
- 适合纯 API 模式
- 函数执行时间限制 10 秒（免费版）

---

## 🛫 方案 3: Fly.io（高性能）

### 为什么选择 Fly.io？
- ✅ 免费额度充足
- ✅ 支持 Docker
- ✅ 全球部署
- ✅ 性能优秀

### 部署步骤

#### 1. 安装 Fly CLI

**Windows**:
```bash
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Mac/Linux**:
```bash
curl -L https://fly.io/install.sh | sh
```

#### 2. 登录

```bash
fly auth login
```

#### 3. 初始化应用

```bash
fly launch
```

按提示操作：
- 选择应用名称
- 选择区域（Singapore 或 Hong Kong）
- 不需要 PostgreSQL
- 不需要 Redis

#### 4. 部署

```bash
fly deploy
```

#### 5. 获取 URL

```bash
fly status
```

URL 格式：
```
https://your-app-name.fly.dev
```

### 注意事项

💰 **免费额度**：
- 3 个共享 CPU 虚拟机
- 3GB 持久化存储
- 160GB 出站流量/月

---

## 🔧 方案 4: 自己的服务器（完全控制）

### 适用场景
- 你有自己的服务器（阿里云/腾讯云/AWS）
- 需要完全控制
- 需要运行 Selenium

### 部署步骤

#### 1. 连接服务器

```bash
ssh root@your-server-ip
```

#### 2. 安装依赖

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Python
apt install python3 python3-pip -y

# 安装 Chrome（用于 Selenium）
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb -y

# 安装 Git
apt install git -y
```

#### 3. 克隆项目

```bash
git clone https://github.com/aye0321123/bazi.git
cd bazi
```

#### 4. 安装 Python 依赖

```bash
pip3 install -r requirements.txt
```

#### 5. 运行应用

```bash
# 测试运行
python3 app.py

# 生产运行
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### 6. 配置 Nginx（推荐）

安装 Nginx：
```bash
apt install nginx -y
```

创建配置文件 `/etc/nginx/sites-available/bazi-ai`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
ln -s /etc/nginx/sites-available/bazi-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 7. 配置 Systemd 服务

创建 `/etc/systemd/system/bazi-ai.service`：
```ini
[Unit]
Description=BaziAI API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bazi
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
systemctl daemon-reload
systemctl start bazi-ai
systemctl enable bazi-ai
systemctl status bazi-ai
```

---

## 📝 部署后配置

### 1. 更新 Cookie

部署后，需要在云端应用中输入你的 Cookie：

1. 访问你的云端 URL
2. 输入 Session ID 和 Cookie
3. 点击登录

### 2. 测试功能

访问健康检查端点：
```
https://your-app-url.com/health
```

应该返回：
```json
{
  "status": "ok",
  "timestamp": "2026-04-18T..."
}
```

### 3. 测试连接

访问：
```
https://your-app-url.com/api/test-connection
```

检查与 BaziAI 的连接状态。

---

## 🔒 安全建议

### 1. 设置环境变量

不要在代码中硬编码敏感信息：

**Render**:
在 Dashboard → Environment 添加

**Vercel**:
```bash
vercel env add SECRET_KEY
```

**Fly.io**:
```bash
fly secrets set SECRET_KEY=your-secret-key
```

### 2. 使用 HTTPS

所有推荐的云平台都自动提供 HTTPS。

### 3. 限制访问（可选）

如果只给特定人使用，可以添加简单的访问控制：

在 `app.py` 中添加：
```python
ALLOWED_IPS = ['your-ip-address']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

---

## 📊 性能优化

### 1. 使用 CDN

Vercel 和 Render 自动提供 CDN。

### 2. 启用缓存

在 `app.py` 中添加：
```python
from flask import make_response

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response
```

### 3. 压缩响应

```python
from flask_compress import Compress
compress = Compress(app)
```

---

## 🐛 故障排查

### 问题 1: 部署失败

**检查**:
- requirements.txt 是否正确
- Python 版本是否兼容
- 查看构建日志

**解决**:
```bash
# 本地测试
pip install -r requirements.txt
python app.py
```

### 问题 2: 应用崩溃

**检查**:
- 查看应用日志
- 检查环境变量
- 测试 API 连接

**Render 查看日志**:
Dashboard → Logs

**Fly.io 查看日志**:
```bash
fly logs
```

### 问题 3: 无法访问 BaziAI

**原因**: 云服务器可能在国外，无法访问 BaziAI

**解决方案**:
1. 选择亚洲节点（Singapore, Hong Kong）
2. 使用自己的服务器
3. 配置代理（高级）

---

## 💰 成本估算

### 免费方案
- **Render**: 完全免费（有休眠）
- **Vercel**: 完全免费（有限制）
- **Fly.io**: 免费额度充足

### 付费方案（如需）
- **Render**: $7/月（无休眠）
- **Fly.io**: 按需付费（通常 $5-10/月）
- **自己服务器**: $5-20/月

---

## 🎯 推荐方案总结

### 场景 1: 个人使用，偶尔访问
**推荐**: Render 免费版
- 完全免费
- 自动休眠节省资源
- 首次访问等待 30 秒可接受

### 场景 2: 多人使用，频繁访问
**推荐**: Render 付费版 ($7/月)
- 无休眠
- 响应快速
- 稳定可靠

### 场景 3: 需要 Selenium 功能
**推荐**: 自己的服务器
- 完全控制
- 可运行 Chrome
- 性能最好

### 场景 4: 快速测试
**推荐**: Vercel
- 部署最快
- 适合纯 API
- 全球 CDN

---

## 📞 下一步

### 立即部署

1. **选择平台**: Render（推荐）
2. **推送代码**: 
   ```bash
   git add .
   git commit -m "准备部署"
   git push
   ```
3. **访问平台**: https://render.com
4. **创建服务**: 按照上面的步骤
5. **等待部署**: 5-10 分钟
6. **测试访问**: 访问你的 URL

### 配置监控

使用 UptimeRobot 防止休眠：
1. 注册 https://uptimerobot.com
2. 添加监控
3. 设置 5 分钟间隔

### 分享给朋友

部署成功后，分享你的 URL：
```
https://your-app.onrender.com
```

告诉他们：
1. 访问 URL
2. 输入 Session ID 和 Cookie
3. 开始使用

---

## 🎉 总结

### 最简单的方案
```
1. 推送代码到 GitHub
2. 访问 Render.com
3. 连接仓库
4. 点击部署
5. ✅ 完成！
```

### 预期时间
- 准备代码: 5 分钟
- 注册平台: 2 分钟
- 配置部署: 3 分钟
- 等待构建: 5-10 分钟
- **总计**: 15-20 分钟

### 成功标志
- ✅ 可以访问 URL
- ✅ 健康检查返回 OK
- ✅ 可以登录和使用
- ✅ API 功能正常

---

**准备好了吗？现在就开始部署吧！** 🚀

**推荐**: 从 Render 开始，5 分钟内完成部署！

---

**文档版本**: 1.0  
**最后更新**: 2026-04-18  
**维护者**: Kiro AI Assistant
