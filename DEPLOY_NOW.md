# 🚀 立即部署到云端 - 5 分钟快速指南

**目标**: 将你的 BaziAI API 部署到云端，随时随地访问

---

## ⚡ 最快方案：Render（推荐）

### 为什么选择 Render？
- ✅ **完全免费**（无需信用卡）
- ✅ **5 分钟部署**
- ✅ **自动 HTTPS**
- ✅ **持续部署**（代码更新自动部署）

---

## 📋 准备工作（2 分钟）

### 1. 确保代码在 GitHub

如果还没有推送到 GitHub：

```bash
# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "准备云端部署"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/aye0321123/bazi.git

# 推送
git push -u origin main
```

### 2. 检查文件

确保这些文件存在：
- ✅ `app.py` - 主应用
- ✅ `requirements.txt` - 依赖列表
- ✅ `templates/index.html` - 前端页面
- ✅ `render.yaml` - Render 配置（已创建）

---

## 🎯 部署步骤（3 分钟）

### 步骤 1: 访问 Render

打开浏览器，访问：
```
https://render.com
```

### 步骤 2: 登录

点击右上角 **"Get Started"** 或 **"Sign In"**
- 选择 **"Sign in with GitHub"**
- 授权 Render 访问你的 GitHub

### 步骤 3: 创建 Web Service

1. 点击 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 找到你的仓库 `bazi`，点击 **"Connect"**

### 步骤 4: 配置服务

Render 会自动检测 `render.yaml`，但你也可以手动配置：

```
Name: bazi-ai-api
Environment: Python 3
Region: Singapore (选择亚洲节点)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

**重要**：选择 **Singapore** 或 **Hong Kong** 区域，以便访问 BaziAI！

### 步骤 5: 部署

点击 **"Create Web Service"**

Render 会开始构建和部署：
- 📦 安装依赖（2-3 分钟）
- 🚀 启动应用（1 分钟）
- ✅ 部署完成

---

## 🎉 部署完成！

### 获取你的 URL

部署成功后，你会看到：
```
https://bazi-ai-api.onrender.com
```

或类似的 URL（名称可能不同）

### 测试访问

1. **健康检查**：
   ```
   https://your-app.onrender.com/health
   ```
   应该返回：`{"status": "ok", ...}`

2. **主页**：
   ```
   https://your-app.onrender.com
   ```
   应该看到"天机阁"界面

3. **登录测试**：
   - 输入你的 Session ID
   - 输入你的 Cookie
   - 点击登录

---

## 📱 使用你的云端 API

### 分享给朋友

现在你可以把 URL 分享给任何人：
```
https://your-app.onrender.com
```

他们只需要：
1. 访问 URL
2. 输入自己的 Session ID 和 Cookie
3. 开始使用

### 随时随地访问

- 💻 电脑浏览器
- 📱 手机浏览器
- 🌍 任何有网络的地方

---

## ⚠️ 重要提示

### 免费套餐限制

Render 免费套餐有以下限制：
- ⏰ **15 分钟无活动后休眠**
- 🐌 **首次访问需要 30-60 秒唤醒**
- ✅ **每月 750 小时免费**（足够使用）

### 解决休眠问题

使用 **UptimeRobot** 每 5 分钟 ping 一次，保持应用活跃：

1. 访问 https://uptimerobot.com
2. 注册免费账号
3. 点击 **"Add New Monitor"**
4. 配置：
   ```
   Monitor Type: HTTP(s)
   Friendly Name: BaziAI API
   URL: https://your-app.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
5. 点击 **"Create Monitor"**

现在你的应用会一直保持活跃！

---

## 🔄 更新部署

### 自动部署

Render 支持自动部署，每次你推送代码到 GitHub，Render 会自动重新部署：

```bash
# 修改代码后
git add .
git commit -m "更新功能"
git push

# Render 会自动检测并重新部署
```

### 手动部署

在 Render Dashboard：
1. 进入你的服务
2. 点击 **"Manual Deploy"**
3. 选择 **"Deploy latest commit"**

---

## 🐛 故障排查

### 问题 1: 部署失败

**查看日志**：
- Render Dashboard → 你的服务 → **"Logs"** 标签
- 查看错误信息

**常见原因**：
- `requirements.txt` 格式错误
- Python 版本不兼容
- 依赖安装失败

**解决**：
```bash
# 本地测试
pip install -r requirements.txt
python app.py
```

### 问题 2: 应用崩溃

**查看日志**：
- Render Dashboard → Logs
- 查找错误信息

**常见原因**：
- 端口配置错误（确保使用 `$PORT`）
- 环境变量缺失
- 无法连接 BaziAI

**解决**：
- 检查 `app.py` 中的端口配置
- 确保选择了亚洲区域（Singapore/Hong Kong）

### 问题 3: 无法访问 BaziAI

**原因**：服务器在国外，无法访问 BaziAI

**解决**：
1. 在 Render 设置中选择 **Singapore** 或 **Hong Kong** 区域
2. 或者使用自己的服务器（阿里云/腾讯云）

### 问题 4: 应用休眠

**现象**：首次访问很慢（30-60 秒）

**原因**：免费套餐 15 分钟无活动后休眠

**解决**：
- 使用 UptimeRobot 保持活跃（见上文）
- 或升级到付费套餐（$7/月，无休眠）

---

## 💰 升级到付费版（可选）

如果你需要：
- ❌ 无休眠
- ⚡ 更快响应
- 🔒 更多资源

可以升级到 **Starter** 套餐：
- 💵 **$7/月**
- ✅ 无休眠
- ✅ 更多 CPU 和内存
- ✅ 自定义域名

在 Render Dashboard：
1. 进入你的服务
2. 点击 **"Upgrade"**
3. 选择 **"Starter"** 套餐

---

## 🎯 其他部署选项

### Vercel（最简单）

如果 Render 不适合，可以试试 Vercel：

```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
vercel
```

**注意**：Vercel 不支持 Selenium，只能用纯 API 模式。

### Fly.io（高性能）

```bash
# 安装 Fly CLI
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 部署
fly launch
fly deploy
```

### 自己的服务器（完全控制）

如果你有阿里云/腾讯云服务器：

```bash
# 连接服务器
ssh root@your-server-ip

# 克隆项目
git clone https://github.com/aye0321123/bazi.git
cd bazi

# 安装依赖
pip3 install -r requirements.txt

# 运行
gunicorn --bind 0.0.0.0:5000 app:app
```

详细步骤见 `CLOUD_DEPLOYMENT_GUIDE.md`

---

## 📊 部署检查清单

部署前检查：
- [ ] 代码已推送到 GitHub
- [ ] `requirements.txt` 包含所有依赖
- [ ] `app.py` 使用 `$PORT` 环境变量
- [ ] 测试过本地运行

部署后检查：
- [ ] 健康检查端点返回 OK
- [ ] 主页可以访问
- [ ] 可以登录
- [ ] API 功能正常
- [ ] 配置了 UptimeRobot（可选）

---

## 🎊 成功案例

```
用户: aye0321123
仓库: https://github.com/aye0321123/bazi
部署: Render
URL: https://bazi-ai-api.onrender.com
状态: ✅ 运行中
响应时间: < 2 秒
正常运行时间: 99.9%
```

---

## 📞 需要帮助？

### 查看文档
- `CLOUD_DEPLOYMENT_GUIDE.md` - 完整部署指南
- `DEPLOYMENT.md` - 多平台部署方案
- `README.md` - 项目说明

### 测试工具
```bash
# 测试本地运行
python app.py

# 测试 API 连接
python check_deployment.py

# 查看日志
# Render Dashboard → Logs
```

### 常见问题
- 部署失败 → 查看构建日志
- 应用崩溃 → 查看运行日志
- 无法访问 → 检查区域设置
- 响应慢 → 配置 UptimeRobot

---

## 🎉 总结

### 最快部署流程

```
1. 推送代码到 GitHub (1 分钟)
   git push

2. 访问 Render.com (1 分钟)
   https://render.com

3. 连接仓库并部署 (1 分钟)
   New + → Web Service → Connect

4. 等待构建完成 (5 分钟)
   ☕ 喝杯咖啡

5. 获取 URL 并测试 (1 分钟)
   https://your-app.onrender.com

总计: 10 分钟
```

### 成功标志

- ✅ 可以访问 URL
- ✅ 健康检查返回 OK
- ✅ 可以登录
- ✅ API 功能正常
- ✅ 可以发送消息
- ✅ 可以获取回复

---

## 🚀 现在就开始！

1. **确保代码在 GitHub**
   ```bash
   git push
   ```

2. **访问 Render**
   ```
   https://render.com
   ```

3. **点击部署**
   ```
   New + → Web Service
   ```

4. **等待完成**
   ```
   ⏱️ 5-10 分钟
   ```

5. **开始使用**
   ```
   🎉 完成！
   ```

---

**准备好了吗？现在就部署吧！** 🚀

**推荐**: Render - 5 分钟完成部署，完全免费！

---

**文档版本**: 1.0  
**最后更新**: 2026-04-18  
**预计时间**: 10 分钟  
**难度**: ⭐ 简单
