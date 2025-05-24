# 🚀 Web3工作抓取器

一个自动化的Web3工作抓取和推送系统，每天从多个Web3工作网站抓取最新工作机会，并翻译成中文推送给您。

## ✨ 功能特性

- 🔄 **自动抓取**: 每天定时从多个Web3工作网站抓取最新工作
- 🌐 **多平台支持**: 支持CryptoJobsList、Web3.career、AngelCo等主流平台
- 🈯 **中文翻译**: 自动将工作描述翻译成中文，支持OpenAI和Google翻译
- 📧 **邮件推送**: 每日工作报告邮件推送
- 🔍 **智能搜索**: 支持关键词搜索、远程工作筛选等
- 📱 **响应式界面**: 现代化的Web界面，支持移动端
- 🗄️ **数据管理**: 自动去重，数据持久化存储
- ⚙️ **管理后台**: 完整的管理界面，支持手动抓取和配置

## 🛠️ 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Bootstrap 5 + Jinja2模板
- **抓取**: BeautifulSoup + Requests
- **翻译**: OpenAI API / Google Translate API
- **调度**: Schedule库
- **邮件**: SMTP

## 📦 安装部署

### 1. 克隆项目

```bash
git clone <repository-url>
cd Here
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下参数：

```env
# 翻译服务配置
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here

# 邮件配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com

# 应用配置
APP_HOST=0.0.0.0
APP_PORT=12000
DEBUG=True
```

### 4. 启动应用

```bash
python run.py
```

或者直接运行：

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 12000 --reload
```

### 5. 访问应用

打开浏览器访问: `http://localhost:12000`

## 🎯 使用说明

### 首页
- 查看最新工作统计
- 浏览最近抓取的工作机会
- 查看数据来源统计

### 工作列表
- 搜索和筛选工作
- 按来源、远程工作等条件过滤
- 分页浏览所有工作

### 工作详情
- 查看完整的工作描述（中英文对照）
- 查看工作要求和技能标签
- 直接跳转到原始工作页面

### 管理后台
- 手动触发工作抓取
- 测试邮件发送功能
- 查看系统统计和配置状态

## ⏰ 定时任务

系统默认配置了以下定时任务：

- **每天 09:00**: 自动抓取工作并发送日报
- **每天 18:00**: 再次抓取工作并发送日报
- **每2小时**: 更新未翻译工作的中文翻译

## 📧 邮件配置

### Gmail配置示例

1. 开启两步验证
2. 生成应用专用密码
3. 配置环境变量：

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com
```

### 其他邮箱服务

- **QQ邮箱**: `smtp.qq.com:587`
- **163邮箱**: `smtp.163.com:587`
- **Outlook**: `smtp-mail.outlook.com:587`

## 🔧 API接口

### 获取工作列表
```
GET /api/jobs?limit=20&search=blockchain&remote_only=true
```

### 获取统计信息
```
GET /api/stats
```

### 手动触发抓取
```
POST /api/scrape
```

## 🌐 支持的工作网站

1. **CryptoJobsList** - 专业的加密货币工作平台
2. **Web3.career** - Web3专业工作平台
3. **AngelCo** - 创业公司工作平台（Web3相关）

## 🔄 扩展新的工作网站

要添加新的工作网站，请：

1. 在 `app/scrapers/` 目录下创建新的爬虫类
2. 继承 `BaseScraper` 类
3. 实现 `scrape_jobs()` 和 `parse_job_detail()` 方法
4. 在 `JobService` 中添加新的爬虫实例

示例：

```python
from .base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://newsite.com", "NewSite")
    
    def scrape_jobs(self, limit: int = 50):
        # 实现抓取逻辑
        pass
    
    def parse_job_detail(self, job_url: str):
        # 实现详情解析逻辑
        pass
```

## 🐛 故障排除

### 常见问题

1. **抓取失败**
   - 检查网络连接
   - 确认目标网站是否可访问
   - 查看日志中的错误信息

2. **翻译失败**
   - 检查API密钥配置
   - 确认API额度是否充足
   - 尝试切换翻译服务

3. **邮件发送失败**
   - 检查SMTP配置
   - 确认邮箱密码或应用密码
   - 检查防火墙设置

### 日志查看

应用日志会输出到控制台，包含：
- 抓取进度和结果
- 翻译状态
- 邮件发送状态
- 错误信息

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

感谢以下开源项目：
- FastAPI
- BeautifulSoup
- SQLAlchemy
- Bootstrap
- 以及所有依赖的开源库

---

如有问题或建议，请提交Issue或联系开发者。

**祝您找到理想的Web3工作！** 🎉