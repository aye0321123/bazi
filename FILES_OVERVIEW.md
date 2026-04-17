# 📁 文件说明

本项目包含多个文件，每个文件都有特定用途。以下是详细说明：

## 🎯 核心文件

### `bazi_api.py` ⭐⭐⭐⭐⭐
**主要的 API 封装类**
- 包含完整的 BaziAI API 封装
- 提供发送消息、获取消息、保存消息等功能
- 适合作为库导入到其他脚本中使用
- **推荐用于**: 需要在自己的项目中集成 BaziAI API

```python
from bazi_api import BaziAI
client = BaziAI(session_id="...", cookie="...")
```

---

## 🚀 快速使用

### `bazi_simple.py` ⭐⭐⭐⭐⭐
**最简单的使用示例**
- 代码最少，最容易理解
- 直接修改文件中的配置即可使用
- 适合快速测试和学习
- **推荐用于**: 第一次使用，快速测试

### `bazi_interactive.py` ⭐⭐⭐⭐
**交互式命令行工具**
- 提供友好的命令行界面
- 无需修改代码，运行时输入配置
- 支持多种命令（发送、获取、保存等）
- **推荐用于**: 日常使用，不想写代码的用户

---

## 🧪 测试工具

### `test_connection.py` ⭐⭐⭐⭐
**连接测试脚本**
- 验证 Session ID 和 Cookie 是否有效
- 提供详细的错误诊断
- 在使用其他脚本前先运行此脚本
- **推荐用于**: 排查连接问题，验证配置

---

## 📖 文档文件

### `README.md` ⭐⭐⭐⭐⭐
**完整的使用文档**
- 详细的功能介绍
- API 说明和示例
- 常见问题解答
- **推荐阅读**: 了解完整功能

### `QUICKSTART.md` ⭐⭐⭐⭐⭐
**5分钟快速开始指南**
- 最快上手的教程
- 包含常用示例
- 问题排查指南
- **推荐阅读**: 第一次使用必读

### `FILES_OVERVIEW.md` ⭐⭐⭐
**本文件 - 文件说明**
- 列出所有文件的用途
- 帮助您选择合适的文件

---

## ⚙️ 配置文件

### `config_example.py` ⭐⭐⭐
**配置文件模板**
- 提供配置文件的示例
- 复制为 `config.py` 后填入实际信息
- 更安全地管理敏感信息
- **推荐用于**: 需要频繁使用，不想每次输入配置

### `.gitignore` ⭐⭐⭐
**Git 忽略文件**
- 防止敏感信息被提交到 Git
- 包含常见的 Python 忽略规则
- **重要**: 保护您的 Cookie 和配置文件

---

## 📊 使用场景推荐

### 场景1: 第一次使用
```
1. 阅读 QUICKSTART.md
2. 运行 test_connection.py 测试连接
3. 运行 bazi_simple.py 快速体验
```

### 场景2: 日常使用
```
运行 bazi_interactive.py
使用交互式命令操作
```

### 场景3: 集成到项目
```python
# 导入 bazi_api.py
from bazi_api import BaziAI

# 在您的代码中使用
client = BaziAI(session_id, cookie)
messages = client.get_messages()
```

### 场景4: 批量操作
```python
# 基于 bazi_api.py 编写自定义脚本
from bazi_api import BaziAI
import time

client = BaziAI(session_id, cookie)

for question in questions:
    client.send_message(question)
    time.sleep(3)
```

### 场景5: 遇到问题
```
1. 运行 test_connection.py 诊断问题
2. 查看 README.md 的常见问题部分
3. 检查 Cookie 是否过期
```

---

## 🎓 学习路径

### 初学者
1. ✅ 阅读 `QUICKSTART.md`
2. ✅ 运行 `test_connection.py`
3. ✅ 运行 `bazi_simple.py`
4. ✅ 尝试 `bazi_interactive.py`

### 进阶用户
1. ✅ 阅读 `README.md`
2. ✅ 学习 `bazi_api.py` 的代码
3. ✅ 基于 `bazi_api.py` 编写自定义脚本
4. ✅ 使用 `config.py` 管理配置

### 开发者
1. ✅ 研究 `bazi_api.py` 的实现
2. ✅ 了解 API 的请求和响应格式
3. ✅ 扩展功能或集成到自己的项目
4. ✅ 参考 `README.md` 的 API 说明

---

## 📝 文件依赖关系

```
bazi_api.py (核心库)
    ↓
    ├── bazi_simple.py (导入使用)
    ├── bazi_interactive.py (导入使用)
    └── 您的自定义脚本 (导入使用)

test_connection.py (独立工具)

config_example.py → config.py (配置文件)
```

---

## 🔄 更新日志

### v1.0 (2026-04-16)
- ✅ 初始版本
- ✅ 完整的 API 封装
- ✅ 交互式工具
- ✅ 测试工具
- ✅ 完整文档

---

## 💡 提示

- **新手**: 从 `bazi_simple.py` 开始
- **日常使用**: 使用 `bazi_interactive.py`
- **开发集成**: 导入 `bazi_api.py`
- **遇到问题**: 运行 `test_connection.py`

---

**选择适合您的文件，开始使用吧！** 🚀
