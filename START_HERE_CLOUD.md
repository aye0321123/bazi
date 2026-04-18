# 🚀 从这里开始 - BaziAI Cloud API

**恭喜！代码已上传到 GitHub** ✅

---

## 📦 已完成

✅ 逆向工程 BaziAI API  
✅ 封装为 RESTful API  
✅ 创建完整文档  
✅ 推送到 GitHub  

**GitHub 仓库**: https://github.com/aye0321123/bazi

---

## 🎯 下一步：部署到云端

### 方法 1: 部署到 Render（推荐，5分钟完成）

#### 步骤 1: 访问 Render

打开浏览器，访问：https://render.com

#### 步骤 2: 注册/登录

- 可以使用 GitHub 账号直接登录
- 或者注册新账号（免费）

#### 步骤 3: 创建 Web Service

1. 点击 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 点击 **"Connect a repository"**
4. 授权 Render 访问你的 GitHub
5. 选择仓库 **"aye0321123/bazi"**

#### 步骤 4: 配置服务

Render 会自动检测到 `render_cloud.yaml` 配置文件：

- **Name**: bazi-cloud-api（或自定义）
- **Region**: Singapore（新加坡）
- **Branch**: main
- **Build Command**: 自动检测
- **Start Command**: 自动检测

#### 步骤 5: 部署

1. 点击 **"Create Web Service"** 或 **"Apply"**
2. 等待部署（约 2-3 分钟）
3. 部署完成后会显示 URL

#### 步骤 6: 获取 API 地址

部署成功后，你会得到一个公网地址：

```
https://bazi-cloud-api.onrender.com
```

或类似的地址。

---

## 🧪 测试 API

### 1. 健康检查

在浏览器中访问：

```
https://your-app.onrender.com/health
```

应该看到：

```json
{
  "status": "ok",
  "timestamp": "2026-04-18T...",
  "service": "BaziAI Cloud API"
}
```

### 2. 查看文档

访问：

```
https://your-app.onrender.com/docs
```

会显示完整的 API 文档。

### 3. 测试 API 调用

使用 Python：

```python
import requests

# 替换为你的 Render URL
api_url = "https://your-app.onrender.com"

# 你的 BaziAI Cookie
cookie = "从 bazi_credentials.json 复制"

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
print(f"✅ 成功！")
print(f"Session ID: {result['session_id']}")
print(f"官网链接: {result['chat_url']}")
```

---

## 📡 API 端点

部署完成后，你可以使用以下端点：

### 基础端点

- `GET /` - API 信息
- `GET /docs` - API 文档
- `GET /health` - 健康检查

### 功能端点

- `POST /api/session/create` - 创建会话
- `POST /api/session/<id>/send` - 发送消息
- `GET /api/session/<id>/messages` - 获取消息
- `POST /api/chat` - 一键对话

---

## 💻 在你的网页中使用

### JavaScript 示例

```javascript
const apiUrl = "https://your-app.onrender.com";
const cookie = "你的 Cookie";

// 发送问题
async function askBazi(question) {
    const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
            'X-Bazi-Cookie': cookie,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: question })
    });
    
    const result = await response.json();
    
    if (result.success) {
        console.log('Session ID:', result.session_id);
        console.log('官网链接:', result.chat_url);
        
        // 打开官网（触发 AI）
        window.open(result.chat_url, '_blank');
        
        // 5秒后开始同步消息
        setTimeout(() => {
            syncMessages(result.session_id);
        }, 5000);
    }
}

// 同步消息
async function syncMessages(sessionId) {
    const response = await fetch(
        `${apiUrl}/api/session/${sessionId}/messages`,
        {
            headers: {
                'X-Bazi-Cookie': cookie
            }
        }
    );
    
    const result = await response.json();
    
    if (result.success) {
        const messages = result.messages;
        
        // 显示消息
        messages.forEach(msg => {
            const role = msg.role === 'user' ? '用户' : 'AI';
            console.log(`${role}: ${msg.content}`);
        });
    }
}

// 使用
askBazi("今天运势如何？");
```

---

## 🔄 自动同步方案

### 完整工作流程

```
1. 用户在你的网页输入问题
    ↓
2. 调用 Cloud API 发送消息
    ↓
3. 打开官网新标签页（触发 AI）
    ↓
4. 你的网页每 5 秒调用 API 同步消息
    ↓
5. AI 回复自动显示在你的网页上
```

### 实现代码

```javascript
let syncInterval = null;

// 开始同步
function startSync(sessionId) {
    // 每 5 秒同步一次
    syncInterval = setInterval(async () => {
        const response = await fetch(
            `${apiUrl}/api/session/${sessionId}/messages`,
            { headers: { 'X-Bazi-Cookie': cookie } }
        );
        
        const result = await response.json();
        
        if (result.success) {
            updateUI(result.messages);
            
            // 如果收到 AI 回复，可以停止同步
            const hasAI = result.messages.some(m => m.role === 'assistant');
            if (hasAI) {
                stopSync();
            }
        }
    }, 5000);
}

// 停止同步
function stopSync() {
    if (syncInterval) {
        clearInterval(syncInterval);
        syncInterval = null;
    }
}
```

---

## 📚 完整文档

- **API 文档**: `CLOUD_API_README.md`
- **部署指南**: `DEPLOY_GUIDE.md`
- **项目总结**: `CLOUD_API_SUMMARY.md`

---

## 🎉 成功！

你现在拥有：

✅ 完整的 BaziAI Cloud API  
✅ 部署到云端的能力  
✅ 在你的网页中集成的方案  
✅ 自动同步消息的方法  

---

## 🚀 立即行动

### 1. 部署到 Render

访问：https://render.com

### 2. 连接 GitHub 仓库

选择：aye0321123/bazi

### 3. 点击部署

等待 2-3 分钟

### 4. 获取 API 地址

复制 Render 提供的 URL

### 5. 开始使用

在你的网页中集成 API

---

**5 分钟完成部署，立即开始使用！** 🎊

---

**需要帮助？**

- 查看 `DEPLOY_GUIDE.md` 详细步骤
- 查看 `CLOUD_API_README.md` API 文档
- 运行 `python test_cloud_api.py` 测试
