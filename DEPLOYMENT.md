# 🚀 部署指南

本文档介绍如何将 BaziAI Web 应用部署到云端，让您的伙伴们可以通过浏览器访问。

---

## 📋 目录

1. [本地测试](#本地测试)
2. [部署到 Heroku](#部署到-heroku)
3. [部署到 Railway](#部署到-railway)
4. [部署到 Render](#部署到-render)
5. [使用 Docker 部署](#使用-docker-部署)
6. [部署到阿里云/腾讯云](#部署到阿里云腾讯云)

---

## 🧪 本地测试

在部署到云端之前，先在本地测试：

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：`http://localhost:5000`

---

## ☁️ 部署到 Heroku

Heroku 是最简单的部署方式，免费套餐足够使用。

### 步骤：

#### 1. 注册 Heroku 账号
访问 [https://heroku.com](https://heroku.com) 注册账号

#### 2. 安装 Heroku CLI
- Windows: 下载安装包 [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
- Mac: `brew install heroku/brew/heroku`
- Linux: `curl https://cli-assets.heroku.com/install.sh | sh`

#### 3. 登录 Heroku
```bash
heroku login
```

#### 4. 创建应用
```bash
heroku create bazi-ai-app
```

#### 5. 部署
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

#### 6. 打开应用
```bash
heroku open
```

### 配置环境变量（可选）

```bash
heroku config:set SECRET_KEY=your-random-secret-key
```

---

## 🚂 部署到 Railway

Railway 提供免费额度，部署非常简单。

### 步骤：

#### 1. 注册 Railway
访问 [https://railway.app](https://railway.app) 使用 GitHub 登录

#### 2. 创建新项目
- 点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 选择您的仓库

#### 3. 配置
Railway 会自动检测 Python 项目并部署

#### 4. 设置环境变量
在 Railway 控制台中添加：
- `SECRET_KEY`: 随机字符串

#### 5. 获取 URL
部署完成后，Railway 会提供一个公开 URL

---

## 🎨 部署到 Render

Render 提供免费的 Web 服务。

### 步骤：

#### 1. 注册 Render
访问 [https://render.com](https://render.com) 注册账号

#### 2. 创建 Web Service
- 点击 "New +"
- 选择 "Web Service"
- 连接您的 GitHub 仓库

#### 3. 配置
- **Name**: bazi-ai-app
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

#### 4. 部署
点击 "Create Web Service"，Render 会自动部署

---

## 🐳 使用 Docker 部署

适合部署到任何支持 Docker 的平台。

### 本地 Docker 测试

#### 1. 构建镜像
```bash
docker build -t bazi-ai-app .
```

#### 2. 运行容器
```bash
docker run -p 5000:5000 bazi-ai-app
```

#### 3. 访问
打开浏览器访问：`http://localhost:5000`

### 使用 Docker Compose

```bash
docker-compose up -d
```

### 部署到云端

#### Docker Hub
```bash
# 登录
docker login

# 标记镜像
docker tag bazi-ai-app your-username/bazi-ai-app

# 推送
docker push your-username/bazi-ai-app
```

然后在云服务器上：
```bash
docker pull your-username/bazi-ai-app
docker run -d -p 80:5000 your-username/bazi-ai-app
```

---

## 🇨🇳 部署到阿里云/腾讯云

### 方式一：使用云服务器（ECS）

#### 1. 购买云服务器
- 选择最低配置即可（1核2G）
- 操作系统：Ubuntu 20.04 或 CentOS 7

#### 2. 连接服务器
```bash
ssh root@your-server-ip
```

#### 3. 安装依赖
```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Python 和 pip
apt install python3 python3-pip -y

# 安装 Git
apt install git -y
```

#### 4. 克隆项目
```bash
git clone https://github.com/your-username/bazi-ai-app.git
cd bazi-ai-app
```

#### 5. 安装 Python 依赖
```bash
pip3 install -r requirements.txt
```

#### 6. 使用 Gunicorn 运行
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### 7. 使用 Nginx 反向代理（推荐）

安装 Nginx：
```bash
apt install nginx -y
```

配置 Nginx（`/etc/nginx/sites-available/bazi-ai`）：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：
```bash
ln -s /etc/nginx/sites-available/bazi-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 8. 使用 Systemd 管理服务

创建服务文件（`/etc/systemd/system/bazi-ai.service`）：
```ini
[Unit]
Description=BaziAI Web Application
After=network.target

[Service]
User=root
WorkingDirectory=/root/bazi-ai-app
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
Restart=always

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

### 方式二：使用容器服务

阿里云和腾讯云都提供容器服务，可以直接部署 Docker 镜像。

---

## 🔒 安全建议

### 1. 设置强密钥
```bash
# 生成随机密钥
python -c "import secrets; print(secrets.token_hex(32))"
```

将生成的密钥设置为环境变量 `SECRET_KEY`

### 2. 使用 HTTPS
- 使用 Let's Encrypt 免费证书
- 或使用云服务商提供的 SSL 证书

### 3. 限制访问
- 设置防火墙规则
- 使用 IP 白名单（如果只给特定人使用）

### 4. 定期更新
```bash
git pull
pip install -r requirements.txt --upgrade
systemctl restart bazi-ai
```

---

## 📊 监控和日志

### 查看日志
```bash
# Systemd 服务日志
journalctl -u bazi-ai -f

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 性能监控
推荐使用：
- **Uptime Robot**: 免费的网站监控
- **New Relic**: 应用性能监控
- **Sentry**: 错误追踪

---

## 🌐 域名配置

### 1. 购买域名
在阿里云、腾讯云或 GoDaddy 购买域名

### 2. 配置 DNS
添加 A 记录指向您的服务器 IP：
```
类型: A
主机记录: @
记录值: your-server-ip
TTL: 600
```

### 3. 等待 DNS 生效
通常需要 10 分钟到 24 小时

---

## 💰 成本估算

### 免费方案
- **Heroku**: 免费套餐（有限制）
- **Railway**: $5 免费额度/月
- **Render**: 免费套餐（有限制）

### 付费方案
- **阿里云 ECS**: ¥50-100/月（学生优惠更便宜）
- **腾讯云 CVM**: ¥50-100/月
- **Heroku Hobby**: $7/月

---

## 🆘 常见问题

### Q: 部署后无法访问？
A: 检查防火墙设置，确保开放了 80 和 443 端口

### Q: 应用崩溃怎么办？
A: 查看日志文件，检查错误信息

### Q: 如何更新应用？
A: 
```bash
git pull
pip install -r requirements.txt --upgrade
systemctl restart bazi-ai
```

### Q: 如何备份数据？
A: 应用使用 session 存储，无需备份。如需持久化，可以添加数据库。

---

## 📞 获取帮助

如果遇到问题：
1. 查看日志文件
2. 检查防火墙和端口设置
3. 确认依赖已正确安装
4. 查看云服务商的文档

---

## 🎉 部署成功后

1. 分享 URL 给您的伙伴们
2. 告诉他们如何获取 Session ID 和 Cookie
3. 建议他们保存好自己的配置信息

**祝您部署顺利！** 🚀
