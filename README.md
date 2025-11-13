# Django Web 项目

这是一个功能丰富的 Django Web 应用程序，包含用户认证、论坛系统、主题管理等功能。

## 项目结构

```
pyWeb/
├── manage.py                     # Django 管理脚本
├── requirements.txt              # 项目依赖
├── .env.example                  # 环境变量示例
├── Procfile                      # Heroku 部署配置
├── runtime.txt                   # Python 运行时版本
├── db.sqlite3                    # SQLite 数据库文件
├── check_tables.py               # 数据库检查脚本
├── myproject/                    # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py                   # ASGI 配置
│   ├── settings.py               # 项目设置
│   ├── urls.py                   # 主 URL 配置
│   └── wsgi.py                   # WSGI 配置
├── myapp/                        # 应用目录
│   ├── __init__.py
│   ├── admin.py                  # 管理界面配置
│   ├── apps.py                   # 应用配置
│   ├── context_processors.py     # 上下文处理器
│   ├── forms.py                  # 表单定义
│   ├── models.py                 # 数据模型
│   ├── tests.py                  # 测试
│   ├── urls.py                   # 应用 URL 配置
│   ├── views.py                  # 视图函数
│   ├── management/               # 管理命令
│   │   └── commands/
│   ├── migrations/               # 数据库迁移文件
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   └── templates/                # 应用模板
│       └── myapp/
├── templates/                    # 全局模板目录
│   ├── base.html                 # 基础模板
│   ├── myapp/                    # 应用模板
│   │   ├── index.html            # 首页
│   │   ├── forum_index.html      # 论坛首页
│   │   ├── forum_detail.html     # 论坛详情
│   │   ├── post_create.html      # 创建帖子
│   │   ├── post_detail.html      # 帖子详情
│   │   ├── post_edit.html        # 编辑帖子
│   │   ├── theme_list.html       # 主题列表
│   │   ├── user_profile.html     # 用户资料
│   │   ├── user_profile_edit.html # 编辑用户资料
│   │   ├── user_profile_settings.html # 用户设置
│   │   └── notifications.html    # 通知中心
│   └── registration/             # 认证模板
│       ├── login.html            # 登录页面
│       └── signup.html           # 注册页面
└── static/                       # 静态文件目录
    ├── css/                      # 样式文件
    │   ├── style.css             # 基础样式
    │   ├── theme-variables.css   # 主题变量
    │   └── theme.css              # 主题样式
    └── js/                       # JavaScript 文件
        └── theme-manager.js       # 主题管理器
```

## 主要功能

### 用户系统
- 用户注册、登录、注销
- 用户资料管理
- 用户设置和偏好
- 头像上传和管理

### 论坛系统
- 多板块论坛
- 帖子发布、编辑、删除
- 帖子回复和互动
- 帖子置顶和精华功能
- 论坛搜索和排序

### 通知系统
- 实时通知
- 通知中心
- 已读/未读状态管理

### 主题系统
- 多主题支持（浅色、暗色、蓝色、绿色）
- 主题切换和管理
- 自定义主题创建
- 主题预览和应用

### 响应式设计
- 移动端友好界面
- Bootstrap 5 框架
- 自适应布局

## 安装和运行

1. 克隆项目：
   ```
   git clone <repository-url>
   cd pyWeb
   ```

2. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 环境变量配置：
   ```
   cp .env.example .env
   # 编辑 .env 文件，设置必要的环境变量
   ```

5. 数据库迁移：
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 创建管理员用户：
   ```
   python manage.py createsuperuser
   ```

7. 运行开发服务器：
   ```
   python manage.py runserver
   ```

8. 在浏览器中访问 http://127.0.0.1:8000/

## 开发指南

### 添加新功能
- 在 `myapp/views.py` 中添加视图函数
- 在 `myapp/urls.py` 中配置 URL 路由
- 在 `myapp/models.py` 中定义数据模型
- 在 `templates/myapp/` 中添加新模板
- 在 `static/` 中添加静态资源

### 主题开发
- 在 `static/css/theme-variables.css` 中定义主题变量
- 在 `static/css/theme.css` 中添加主题特定样式
- 使用 `theme-manager.js` 管理主题切换

### 数据库操作
- 使用 Django ORM 进行数据库操作
- 创建迁移文件：`python manage.py makemigrations`
- 应用迁移：`python manage.py migrate`

## 部署

### 本地部署
1. 设置环境变量
2. 收集静态文件：`python manage.py collectstatic`
3. 使用 Gunicorn 运行：`gunicorn myproject.wsgi:application`

### Heroku 部署
1. 安装 Heroku CLI
2. 登录 Heroku：`heroku login`
3. 创建应用：`heroku create`
4. 推送代码：`git push heroku main`
5. 迁移数据库：`heroku run python manage.py migrate`

### 生产环境注意事项
1. 更改 `settings.py` 中的 `SECRET_KEY`
2. 设置 `DEBUG = False`
3. 配置适当的 `ALLOWED_HOSTS`
4. 配置生产数据库（如 PostgreSQL）
5. 配置静态文件服务
6. 设置安全头和 HTTPS

## 技术栈

- **后端框架**：Django 4.x
- **前端框架**：Bootstrap 5
- **数据库**：SQLite（开发）/ PostgreSQL（生产）
- **部署平台**：Heroku（支持）
- **其他技术**：
  - Django REST Framework（API）
  - Pillow（图像处理）
  - Gunicorn（WSGI 服务器）
  - WhiteNoise（静态文件服务）

## 贡献指南

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。
