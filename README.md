# PyTestCoder

PyTestCoder 是一个基于 FastAPI 开发的技术交流平台，同时也是一个完整的测试开发实践项目。项目实现了用户注册登录、帖子管理和评论互动等核心功能，并构建了完善的测试体系。

## 技术栈

- **后端框架：** FastAPI
- **数据库：** SQLite + SQLAlchemy ORM
- **认证：** JWT Token
- **测试框架：** Pytest
- **其他工具：** Pydantic, Passlib, Python-Jose

## 项目特点

### 完整的测试体系
- 分层测试架构（单元测试、集成测试、性能测试、安全测试）
- 测试覆盖率达到 88%
- 自动化的测试数据管理
- 完善的测试报告生成

### 核心功能
- 用户认证系统（注册、登录、JWT认证）
- 帖子管理（CRUD操作）
- 评论系统
- 内容安全（XSS防护）

### 性能测试
- 接口响应时间监控
- 并发压力测试（支持100并发用户）
- 性能基准测试
- 数据库查询优化

## 安装部署

1. 克隆项目
```bash
git clone https://github.com/yourusername/PyTestCoder.git
cd PyTestCoder
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行项目
```bash
uvicorn app.main:app --reload
```

项目将运行在 http://localhost:8000

## 测试运行

### 运行所有测试
```bash
pytest
```

### 运行特定测试类型
```bash
# 单元测试
pytest tests/unit

# 集成测试
pytest tests/integration

# 性能测试
pytest tests/performance

# 带覆盖率的测试
pytest --cov=app tests/
```

### 查看测试报告
```bash
pytest --cov=app tests/ --cov-report=html
```
报告将生成在 htmlcov 目录下

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
PyTestCoder/
├── app/
│   ├── models/         # 数据模型
│   ├── routes/         # API路由
│   ├── schemas/        # Pydantic模型
│   ├── utils/          # 工具函数
│   └── main.py         # 主程序
├── tests/
│   ├── unit/          # 单元测试
│   ├── integration/   # 集成测试
│   ├── performance/   # 性能测试
│   └── conftest.py    # 测试配置
└── requirements.txt    # 项目依赖
```

## 测试特性

### 测试夹具 (Fixtures)
- test_db: 提供独立的测试数据库会话
- test_client: FastAPI测试客户端
- test_user: 测试用户数据
- test_token: JWT测试令牌

### 测试类型
1. **单元测试**
   - 模型验证
   - 工具函数测试
   - 数据库操作测试

2. **集成测试**
   - API端点测试
   - 用户认证流程测试
   - 完整业务流程测试

3. **性能测试**
   - 响应时间测试
   - 并发处理测试
   - 数据库性能测试

4. **安全测试**
   - JWT验证测试
   - XSS防护测试
   - 访问控制测试

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 开源协议

此项目使用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

项目作者 - [@Leen-075](https://github.com/Leen-075)

项目链接: [https://github.com/Leen-075/PyTestCoder](https://github.com/Leen-075/PyTestCoder)