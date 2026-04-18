# 🚀 部署指南

**快速部署 BaziAI Cloud API 到云端**

---

## 📋 准备工作

### 需要的文件

- ✅ `cloud_api.py` - 主程序
- ✅ `requirements_cloud.txt` - 依赖
- ✅ `Procfile_cloud` - 进程配置
- ✅ `runtime.txt` - Python 版本
- ✅ `render_cloud.yaml` - Render 配置

### 需要的账号

- GitHub 账号（免费）
- Render 账号（免费）或 Heroku 账号（免费）

---

## 🎯 方法 1: 部署到 Render（推荐）

### 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库，例如 `bazi-cloud-api`
3. 不要初始化 README

### 步骤 2: 推送代码

```bash
# 初始化 git
git init

# 添加文件
git add cloud_api.py requirements_cloud.txt Procfile_cloud runtime.txt render_cloud.yaml CLOUD_API_README.md

# 提交
git commit -m "Initial commit: BaziAI Cloud API"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/your-username/bazi-cloud-api.git

# 推送
git branch -M main
git push -u origin main
```

### 步骤 3: 在 Render 上部署

1. 访问 https://render.com
2. 注册/登录账号
3. 点击 **"New +"** → **"Web Service"**
4. 点击 **"Connect a repository"**
5. 选择你的 GitHub 仓库 `bazi-cloud-api`
6. Render 会自动检测到 `render_cloud.yaml`
7. 点击 **"Apply"** 或 **"Create Web Service"**
8. 等待部署完成（约 2-3 分钟）

### 步骤 4: 获取 API 地址

部署完成后，Render 会提供一个公网地址：

```
https://bazi-cloud-api.onrender.com
```

### 步骤 5: 测试 API

```bash
# 健康检查
curl https://bazi-cloud-api.onrender.com/health

# 查看文档
curl https://bazi-cloud-api.onrender.com/docs
```

---

## 🎯 方法 2: 部署到 Heroku

### 步骤 1: 安装 Heroku CLI

访问 https://devcenter.heroku.com/articles/heroku-cli 下载安装

### 步骤 2: 登录 Heroku

```bash
heroku login
```

### 步骤 3: 创建应用

```bash
# 创建应用
heroku create bazi-cloud-api

# 或指定区域
heroku create bazi-cloud-api --region eu
```

### 步骤 4: 准备文件

```bash
# 重命名 Procfile
cp Procfile_cloud Procfile

# 初始化 git（如果还没有）
git init

# 添加文件
git add cloud_api.py requirements_cloud.txt Procfile runtime.txt

# 提交
git commit -m "Deploy to Heroku"
```

### 步骤 5: 部署

```bash
# 推送到 Heroku
git push heroku main

# 查看日志
heroku logs --tail

# 打开应用
heroku open
```

### 步骤 6: 获取 API 地址

```
https://bazi-cloud-api.herokuapp.com
```

---

## 🧪 本地测试

在部署到云端之前，建议先本地测试：

### 步骤 1: 安装依赖

```bash
pip install -r requirements_cloud.txt
```

### 步骤 2: 启动服务

```bash
python cloud_api.py
```

### 步骤 3: 测试 API

```bash
# 在另一个终端运行
python test_cloud_api.py
```

或使用 curl：

```bash
# 健康检查
curl http://localhost:8000/health

# 查看文档
curl http://localhost:8000/docs
```

---

## 📡 使用 API

### 获取 Cookie

1. 访问 https://www.bazi-ai.com
2. 登录你的账号
3. 按 F12 打开开发者工具
4. 切换到 Network 标签
5. 刷新页面
6. 找到任意请求，查看 Request Headers
7. 复制 Cookie 字段的值

### Python 示例

```python
import requests

# API 地址
api_url = "https://bazi-cloud-api.onrender.com"

# 你的 Cookie
cookie = "你的 BaziAI Cookie"

# 请求头
headers = {
    "X-Bazi-Cookie": cookie,
    "Content-Type": "application/json"
}

# 一键对话
response = requests.post(
    f"{api_url}/api/chat",
    headers=headers,
    json={"content": "今天运势如何？"}
)

result = response.json()
print(f"Session ID: {result['session_id']}")
print(f"官网链接: {result['chat_url']}")
```

### JavaScript 示例

```javascript
const apiUrl = "https://bazi-cloud-api.onrender.com";
const cookie = "你的 BaziAI Cookie";

fetch(`${apiUrl}/api/chat`, {
    method: 'POST',
    headers: {
        'X-Bazi-Cookie': cookie,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: "今天运势如何？" })
})
.then(res => res.json())
.then(data => {
    console.log('Session ID:', data.session_id);
    console.log('官网链接:', data.chat_url);
});
```

---

## 🔧 常见问题

### Q1: 部署失败怎么办？

**A**: 检查以下几点：
- Python 版本是否正确（3.12.0）
- 依赖是否完整
- Procfile 配置是否正确
- 查看部署日志找出错误

### Q2: API 返回 500 错误？

**A**: 可能的原因：
- Cookie 已过期，需要更新
- BaziAI 服务器不可用
- 网络连接问题

### Q3: 如何更新 Cookie？

**A**: 
1. 重新获取 Cookie
2. 在请求头中使用新的 Cookie
3. 或者设置环境变量

### Q4: 免费版有限制吗？

**A**: 
- Render 免费版：每月 750 小时
- Heroku 免费版：已取消（需要付费）
- 建议使用 Render

### Q5: 如何查看日志？

**A**:
- Render: 在 Dashboard 中查看 Logs
- Heroku: `heroku logs --tail`
- 本地: 直接在终端查看

---

## 📊 性能优化

### 1. 增加 Workers

在 `Procfile` 中：

```
web: gunicorn cloud_api:app --workers 4 --timeout 120
```

### 2. 使用缓存

添加 Redis 缓存 Cookie 和会话信息

### 3. 负载均衡

使用多个实例分担负载

---

## 🎯 下一步

部署完成后，你可以：

1. ✅ 在你的网页中集成 API
2. ✅ 实现自动同步消息
3. ✅ 添加用户认证
4. ✅ 监控 API 使用情况

---

## 📞 总结

### 推荐部署方式

**Render（免费 + 简单）**

优点：
- ✅ 完全免费
- ✅ 自动部署
- ✅ 支持 YAML 配置
- ✅ 稳定可靠

### 部署流程

```
创建 GitHub 仓库
    ↓
推送代码
    ↓
连接到 Render
    ↓
自动部署
    ↓
获取 API 地址
    ↓
开始使用
```

**5 分钟完成部署！** 🚀

---

**立即开始部署吧！**
