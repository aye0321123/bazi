# 🚀 ngrok 内网穿透设置指南

## 什么是 ngrok？

ngrok 可以让你的本地服务器（http://127.0.0.1:5000）通过一个公网 URL 被外网访问。

## 📝 设置步骤

### 步骤 1：注册 ngrok 账号

1. 访问：https://dashboard.ngrok.com/signup
2. 使用 Google/GitHub 账号或邮箱注册（免费）

### 步骤 2：获取 authtoken

1. 登录后访问：https://dashboard.ngrok.com/get-started/your-authtoken
2. 复制你的 authtoken（类似：`2abc...xyz`）

### 步骤 3：配置 authtoken

打开 `start_with_ngrok.py` 文件，找到这一行：

```python
# ngrok.set_auth_token("你的authtoken")
```

去掉注释并填入你的 token：

```python
ngrok.set_auth_token("2abc...xyz")  # 替换成你的真实 token
```

### 步骤 4：启动服务

运行：

```bash
python start_with_ngrok.py
```

你会看到类似这样的输出：

```
🎉 服务已启动！
============================================================

📍 本地地址: http://127.0.0.1:5000
🌐 公网地址: https://xxxx-xx-xx-xx-xx.ngrok-free.app

💡 提示:
   - 使用公网地址可以从任何地方访问你的 API
   - 按 Ctrl+C 停止服务
```

## 🌐 使用公网 URL

复制公网地址（例如：`https://xxxx-xx-xx-xx-xx.ngrok-free.app`），你可以：

1. 在任何地方访问你的 API
2. 分享给其他人使用
3. 在手机上测试

## ⚠️ 注意事项

1. **免费版限制**：
   - 每次启动 URL 会变化
   - 有连接数限制
   - 会显示 ngrok 警告页面（点击"Visit Site"继续）

2. **安全性**：
   - 不要分享你的 authtoken
   - 公网 URL 任何人都能访问
   - 建议只在测试时使用

## 🔄 替代方案

如果不想注册 ngrok，可以：

1. **只在本地使用**：
   ```bash
   python app.py
   ```
   访问：http://127.0.0.1:5000

2. **使用其他内网穿透工具**：
   - localtunnel
   - serveo
   - cloudflared

## 💡 快速测试

如果你已经配置好 authtoken，直接运行：

```bash
python start_with_ngrok.py
```

然后访问显示的公网 URL！
