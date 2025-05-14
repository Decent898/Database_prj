# 签名墙网站 (Signature Wall)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个基于Python Django的签名墙网站项目，支持MySQL或SQLite数据库。该项目旨在提供一个让用户可以分享个性化签名、发布博客文章并建立社区的平台。

## 功能特点

### 用户系统
- 用户注册与登录功能
- 基于Django认证系统的权限管理
- 个性化用户个人资料
- 头像上传和编辑
- 密码重置功能

### 签名墙功能
- 手写签名上传（支持多种图片格式）
- 签名展示墙（按时间/热度排序）
- 个人签名管理（编辑/删除）
- 签名点赞和评论功能
- 签名搜索与筛选

### 博客系统
- Markdown格式支持
- LaTeX数学公式渲染（使用KaTeX）
- 代码高亮显示
- 文章分类与标签（支持中文标签）
- 评论交互功能
- 草稿保存与发布控制

### 社交功能
- 用户之间的互动
- 用户个人主页访问
- 关注喜欢的签名和博主

### 系统特性
- 响应式设计，适配移动设备
- 多语言支持架构
- 完整的管理员后台

## 技术栈

### 后端技术
- **Python 3.9+**: 核心编程语言
- **Django 5.2+**: Web开发框架
- **django-crispy-forms**: 改进表单渲染
- **crispy-bootstrap5**: Bootstrap 5样式集成
- **Markdown**: 博客内容渲染
- **python-markdown-math**: LaTeX数学公式支持
- **pypinyin**: 中文拼音转换（用于中文slug生成）

### 数据库
- **MySQL/MariaDB**: 生产环境推荐数据库
- **SQLite3**: 快速开发和测试环境数据库

### 前端技术
- **Bootstrap 5**: 响应式UI框架
- **JavaScript/jQuery**: 前端交互
- **EasyMDE**: Markdown编辑器
- **KaTeX**: 数学公式渲染
- **Font Awesome**: 图标库

### 部署和服务
- **Gunicorn**: WSGI HTTP服务器
- **WhiteNoise**: 静态文件服务
- **Dotenv**: 环境变量管理

## 安装和设置

### 基础安装

1. **克隆项目**
```bash
git clone https://github.com/你的用户名/signature_wall.git
cd signature_wall
```

2. **创建并激活虚拟环境**
```bash
# 在macOS/Linux系统上:
python3 -m venv venv
source venv/bin/activate

# 在Windows系统上:
python -m venv venv
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

### 数据库配置

4. **配置SQLite (开发环境)**
   - 默认情况下项目使用SQLite，无需额外配置

   **或者配置MySQL (推荐用于生产环境)**
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE signature_wall_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON signature_wall_db.* TO 'your_database_user'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

5. **环境变量配置**
   - 创建.env文件在项目根目录下

```
# 开发环境配置
DEBUG=True
SECRET_KEY=请更改为一个安全的随机字符串
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置 (SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# 数据库配置 (MySQL) - 取消注释以启用MySQL
# DATABASE_URL=mysql://your_database_user:your_password@localhost:3306/signature_wall_db

# 邮件配置 (使用控制台后端进行开发)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# 生产环境邮件配置
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.example.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your_email@example.com
# EMAIL_HOST_PASSWORD=your_email_password
```

### 初始化应用

6. **运行数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **创建超级用户 (管理员账户)**
```bash
python manage.py createsuperuser
```

8. **收集静态文件**
```bash
python manage.py collectstatic
```

9. **设置初始数据和媒体文件** (可选)
```bash
# 初始化数据
bash setup_initial_data.sh

# 设置媒体文件
bash setup_media.sh
```

## 运行和部署

### 开发环境运行

1. **启动开发服务器**
```bash
# 默认本地访问
python manage.py runserver

# 指定IP和端口（局域网内访问）
python manage.py runserver 0.0.0.0:8000
```

2. **访问网站**
   - 在浏览器中访问: http://127.0.0.1:8000
   - 访问管理后台: http://127.0.0.1:8000/admin/

### 生产环境部署

#### 方法一: 使用提供的脚本部署

```bash
# 局域网访问
bash start_public_server.sh

# 生产模式（使用Gunicorn）
bash start_production_server.sh

# 使用ngrok实现公网临时访问
bash start_public_with_ngrok.sh
```

#### 方法二: 使用Docker部署 (需自行创建Dockerfile)

```bash
# 构建Docker镜像
docker build -t signature-wall .

# 运行Docker容器
docker run -d -p 8000:8000 --name signature-wall-app signature-wall
```

#### 方法三: 使用Nginx + Gunicorn部署

1. **安装并配置Gunicorn**
```bash
# 启动Gunicorn
gunicorn --bind 0.0.0.0:8000 signature_wall.wsgi:application
```

2. **Nginx配置示例**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        root /path/to/your/project;
    }

    location /media/ {
        root /path/to/your/project;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

有关如何在公网上安全部署的详细说明，请参阅 [PUBLIC_ACCESS.md](PUBLIC_ACCESS.md) 文件。

## 项目结构

```
signature_wall/
├── accounts/           # 用户认证和个人资料管理
│   ├── migrations/     # 数据库迁移文件
│   ├── templates/      # 用户相关模板
│   ├── forms.py        # 表单定义
│   ├── models.py       # 用户模型
│   └── views.py        # 视图函数
├── blog/               # 博客系统
│   ├── migrations/     # 数据库迁移文件
│   ├── templates/      # 博客相关模板
│   ├── forms.py        # 表单定义
│   ├── models.py       # 博客模型
│   └── views.py        # 视图函数
├── signatures/         # 签名墙功能
│   ├── migrations/     # 数据库迁移文件
│   ├── templates/      # 签名相关模板
│   ├── forms.py        # 表单定义
│   ├── models.py       # 签名模型
│   └── views.py        # 视图函数
├── signature_wall/     # 项目配置
│   ├── settings.py     # 项目设置
│   ├── urls.py         # URL路由配置
│   └── wsgi.py         # WSGI配置
├── static/             # 静态文件
│   ├── css/            # CSS样式
│   ├── js/             # JavaScript脚本
│   └── img/            # 图片资源
├── media/              # 用户上传文件
│   ├── profile_pics/   # 头像图片
│   └── signatures/     # 签名图片
├── templates/          # 全局模板文件
│   ├── base.html       # 基础模板
│   └── home.html       # 首页模板
├── manage.py           # Django管理脚本
├── requirements.txt    # 项目依赖
└── .env                # 环境变量配置
```

## 功能使用指南

### 管理员功能
1. 通过`/admin/`路径访问管理后台
2. 使用超级用户账号登录
3. 可管理用户、签名、文章和评论等所有内容

### 用户注册与登录
1. 点击导航栏的"注册"按钮创建新账户
2. 使用邮箱和密码登录
3. 可选择"记住我"功能保持登录状态

### 签名墙使用
1. 登录后可在"签名墙"页面上传个人签名
2. 支持上传PNG、JPG、WEBP等格式图片
3. 可编辑或删除自己的签名
4. 可浏览和点赞其他用户的签名

### 博客功能
1. 在"博客"页面浏览所有文章
2. 登录后可创建新文章
3. 支持Markdown格式和数学公式
4. 可为文章添加标签和分类
5. 支持保存草稿或直接发布

### 个人资料管理
1. 点击用户名下拉菜单中的"个人资料"
2. 可上传头像、修改个人信息
3. 查看个人发布的签名和文章

## 开源贡献指南

### 贡献方式
1. **提交Issue**: 报告Bug或提出功能建议
   - 使用清晰的标题和详细描述
   - 提供复现步骤和预期行为

2. **提交Pull Request**:
   - Fork本仓库并克隆到本地
   - 创建新分支进行修改 `git checkout -b feature/your-feature-name`
   - 提交变更 `git commit -m "Add: 功能描述"`
   - 推送到你的Fork `git push origin feature/your-feature-name`
   - 创建Pull Request并详细描述变更内容

### 开发规范
- 遵循PEP 8 Python编码规范
- 为所有新功能编写测试
- 保持代码注释清晰完整
- 提交前运行测试确保通过

### 分支管理
- `main`: 主分支，保持稳定
- `develop`: 开发分支，功能合并到此
- `feature/*`: 新功能分支
- `bugfix/*`: Bug修复分支
- `release/*`: 版本发布分支

## 版本历史

- **v1.0.0** (2025-05-14): 初始版本发布
  - 基础用户系统
  - 签名墙功能
  - 博客系统

- **v1.1.0** (2025-05-14): 功能增强
  - 添加数学公式支持
  - 修复中文标签问题
  - 改进博客编辑器
  - 优化登录登出流程

## 许可证

本项目采用MIT许可证。详情请参阅 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2025 签名墙项目团队

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
