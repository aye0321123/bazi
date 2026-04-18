# 🌐 BaziAI Cloud API

**逆向工程的 BaziAI API 封装，部署到云端**

---

## 📋 项目说明

这是一个将 BaziAI 官方 API 逆向工程后封装的云端 API 服务。

### 功能特点

- ✅ 创建聊天会话
- ✅ 发送消息
- ✅ 获取消息列表
- ✅ 一键对话（创建+发送）
- ✅ RESTful API 设计
- ✅ 支持跨域请求（CORS）
- ✅ 完整的 API 文档

---

## 🚀 快速部署

### 方法 1: 部署到 Render（推荐）

1. **创建 GitHub 仓库**
   ```bash
   git init
   git add cloud_api.py requirements_cloud.txt Procfile_cloud runtime.txt render_cloud.yaml
   git commit -m "Add BaziAI Cloud API"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **在 Render 上部署**
   - 访问 https://render.com
   - 点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库
   - 选择 `render_cloud.yaml` 配置
   - 点击 "Create Web Service"

3. **等待部署完成**
   - Render 会自动安装依赖并启动服务
   - 部署完成后会提供一个公网 URL

---

### 方法 2: 部署到 Heroku

1. **安装 Heroku CLI**
   ```bash
   # 访问 https://devcenter.heroku.com/articles/heroku-cli 下载安装
   ```

2. **登录并创建应用**
   ```bash
   heroku login
   heroku create bazi-cloud-api
   ```

3. **部署**
   ```bash
   # 重命名 Procfile
   mv Procfile_cloud Procfile
   
   # 部署
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

4. **查看日志**
   ```bash
   heroku logs --tail
   ```

---

### 方法 3: 本地测试

```bash
# 安装依赖
pip install -r requirements_cloud.txt

# 运行服务
python cloud_api.py

# 访问
http://localhost:8000
```

---

## 📡 API 文档

### 基础信息

**Base URL**: `https://your-app.onrender.com` 或 `http://localhost:8000`

**认证方式**: 在请求头中添加 `X-Bazi-Cookie`

```
X-Bazi-Cookie: 你的 BaziAI Cookie
```

---

### 端点列表

#### 1. 获取 API 信息

```
GET /
```

**响应**:
```json
{
  "name": "BaziAI Cloud API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

---

#### 2. 查看文档

```
GET /docs
```

**响应**: 完整的 API 文档

---

#### 3. 健康检查

```
GET /health
```

**响应**:
```json
{
  "status": "ok",
  "timestamp": "2026-04-18T..."
}
```

---

#### 4. 创建会话

```
POST /api/session/create
```

**请求头**:
```
X-Bazi-Cookie: 你的 Cookie
```

**响应**:
```json
{
  "success": true,
  "session_id": "xxx-xxx-xxx",
  "data": {...}
}
```

---

#### 5. 发送消息

```
POST /api/session/<session_id>/send
```

**请求头**:
```
X-Bazi-Cookie: 你的 Cookie
Content-Type: application/json
```

**请求体**:
```json
{
  "content": "今天运势如何？"
}
```

**响应**:
```json
{
  "success": true,
  "data": {...}
}
```

---

#### 6. 获取消息列表

```
GET /api/session/<session_id>/messages
```

**请求头**:
```
X-Bazi-Cookie: 你的 Cookie
```

**响应**:
```json
{
  "success": true,
  "messages": [
    {
      "role": "user",
      "content": "今天运势如何？",
      "created_at": "2026-04-18T..."
    },
    {
      "role": "assistant",
      "content": "AI 的回复...",
      "created_at": "2026-04-18T..."
    }
  ]
}
```

---

#### 7. 一键对话

```
POST /api/chat
```

**请求头**:
```
X-Bazi-Cookie: 你的 Cookie
Content-Type: application/json
```

**请求体**:
```json
{
  "content": "今天运势如何？"
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "xxx-xxx-xxx",
  "user_message": {...},
  "chat_url": "https://www.bazi-ai.com/zh/chat/xxx",
  "note": "AI 回复需要在官网查看，或稍后调用获取消息接口"
}
```

---

## 💻 使用示例

### Python

```python
import requests

# 你的 Cookie
cookie = "你的 BaziAI Cookie"

# API 地址
base_url = "https://your-app.onrender.com"

# 请求头
headers = {
    "X-Bazi-Cookie": cookie,
    "Content-Type": "application/json"
}

# 1. 一键对话
response = requests.post(
    f"{base_url}/api/chat",
    headers=headers,
    json={"content": "今天运势如何？"}
)

result = response.json()
print(f"Session ID: {result['session_id']}")
print(f"官网链接: {result['chat_url']}")

# 2. 获取消息
session_id = result['session_id']
response = requests.get(
    f"{base_url}/api/session/{session_id}/messages",
    headers=headers
)

messages = response.json()['messages']
for msg in messages:
    role = "用户" if msg['role'] == 'user' else "AI"
    print(f"{role}: {msg['content']}")
```

---

### JavaScript

```javascript
// 你的 Cookie
const cookie = "你的 BaziAI Cookie";

// API 地址
const baseUrl = "https://your-app.onrender.com";

// 1. 一键对话
async function chat(question) {
    const response = await fetch(`${baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
            'X-Bazi-Cookie': cookie,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: question })
    });
    
    const result = await response.json();
    console.log('Session ID:', result.session_id);
    console.log('官网链接:', result.chat_url);
    
    return result.session_id;
}

// 2. 获取消息
async function getMessages(sessionId) {
    const response = await fetch(
        `${baseUrl}/api/session/${sessionId}/messages`,
        {
            headers: {
                'X-Bazi-Cookie': cookie
            }
        }
    );
    
    const result = await response.json();
    return result.messages;
}

// 使用
chat("今天运势如何？").then(sessionId => {
    setTimeout(() => {
        getMessages(sessionId).then(messages => {
            messages.forEach(msg => {
                const role = msg.role === 'user' ? '用户' : 'AI';
                console.log(`${role}: ${msg.content}`);
            });
        });
    }, 5000);
});
```

---

### cURL

```bash
# 你的 Cookie
COOKIE="你的 BaziAI Cookie"

# API 地址
BASE_URL="https://your-app.onrender.com"

# 1. 一键对话
curl -X POST "$BASE_URL/api/chat" \
  -H "X-Bazi-Cookie: $COOKIE" \
  -H "Content-Type: application/json" \
  -d '{"content":"今天运势如何？"}'

# 2. 获取消息
SESSION_ID="xxx-xxx-xxx"
curl -X GET "$BASE_URL/api/session/$SESSION_ID/messages" \
  -H "X-Bazi-Cookie: $COOKIE"
```

---

## 🔧 配置说明

### 环境变量

- `PORT`: 服务端口（默认 8000）

### 依赖项

- Flask: Web 框架
- flask-cors: 跨域支持
- urllib3: HTTP 客户端
- gunicorn: WSGI 服务器

---

## ⚠️ 重要提示

### Cookie 获取

1. 访问 https://www.bazi-ai.com
2. 登录你的账号
3. 按 F12 打开开发者工具
4. 切换到 Network 标签
5. 刷新页面
6. 找到任意请求，查看 Request Headers
7. 复制 Cookie 字段的值

### Cookie 有效期

- Cookie 会过期，需要定期更新
- 建议使用环境变量存储 Cookie
- 或者实现自动刷新机制

### AI 回复机制

- 纯 API 调用，AI 不会自动回复
- 需要用户访问官网才能触发 AI
- 建议使用轮询机制定期获取消息

---

## 📊 工作流程

```
你的应用
    ↓
调用 Cloud API
    ↓
Cloud API 转发到 BaziAI
    ↓
返回结果给你的应用
```

### 推荐使用方式

1. **发送消息**: 调用 `/api/chat`
2. **打开官网**: 使用返回的 `chat_url`
3. **轮询消息**: 定期调用 `/api/session/<id>/messages`
4. **显示回复**: 在你的应用中展示

---

## 🎯 优势

### 相比直接调用 BaziAI API

- ✅ 统一的 RESTful 接口
- ✅ 更好的错误处理
- ✅ 支持跨域请求
- ✅ 完整的 API 文档
- ✅ 易于集成

### 相比使用 Selenium

- ✅ 更快的响应速度
- ✅ 更低的资源消耗
- ✅ 更容易部署
- ✅ 更稳定可靠

---

## 📞 总结

这个 Cloud API 提供了：

1. **简单易用的 RESTful API**
2. **完整的文档和示例**
3. **支持多种部署方式**
4. **跨域支持，易于集成**

**立即部署到云端，开始使用！** 🚀

---

## 📁 文件清单

- `cloud_api.py` - 主程序
- `requirements_cloud.txt` - Python 依赖
- `Procfile_cloud` - Heroku 配置
- `runtime.txt` - Python 版本
- `render_cloud.yaml` - Render 配置
- `CLOUD_API_README.md` - 本文档

---

**版本**: 1.0.0  
**更新日期**: 2026-04-18  
**作者**: BaziAI API Team
