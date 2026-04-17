# 🔮 天机阁 - BaziAI Web 应用

基于 Flask 的 BaziAI API Web 界面，提供友好的用户体验。

## ✨ 功能特性

- 🆕 创建新对话
- 💬 发送和接收消息
- 🔄 实时刷新对话
- 📥 导出聊天记录
- 🎨 精美的中国风界面

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问
http://localhost:5000
```

### Docker 运行

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

## 📚 文档

- [快速开始](快速开始.md)
- [使用说明](天机阁使用说明.md)
- [API 文档](API_DOCUMENTATION.md)
- [部署指南](云端部署指南.md)

## 🌐 部署到云端

支持多种部署方式：

- **Railway** - 推荐，免费且简单
- **Render** - 免费，有休眠限制
- **Docker** - 适合有服务器的用户
- **阿里云/腾讯云** - 国内访问快

详见 [云端部署指南](云端部署指南.md)

## 📝 使用方法

1. 访问应用 URL
2. 粘贴你的 Cookie（从 BaziAI 官网获取）
3. 点击"✨ 新对话"创建对话
4. 开始使用

## 🔒 安全提示

- 不要分享你的 Cookie
- 不要将 `bazi_credentials.json` 上传到公共仓库
- 定期更新 Cookie

## 📄 许可证

MIT License

## 🙏 致谢

感谢 BaziAI 提供的 API 服务。
