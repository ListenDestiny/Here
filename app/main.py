from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from .database import get_db, create_tables
from .models.job import Job
from .services.job_service import JobService
from .services.notification_service import NotificationService
from .scheduler import scheduler

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Web3工作抓取器",
    description="每天从Web3工作网站抓取最新工作并翻译成中文",
    version="1.0.0"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 模板
templates = Jinja2Templates(directory="app/templates")

# 创建数据库表
create_tables()

@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    print("Web3工作抓取器启动中...")
    # 启动调度器
    scheduler.start()
    print("应用启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件"""
    print("正在关闭应用...")
    scheduler.stop()
    print("应用已关闭")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """首页"""
    job_service = JobService(db)
    
    # 获取最近的工作
    recent_jobs = job_service.get_recent_jobs(days=7, limit=20)
    
    # 获取统计信息
    stats = job_service.get_job_statistics()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "jobs": recent_jobs,
        "stats": stats
    })

@app.get("/jobs", response_class=HTMLResponse)
async def jobs_page(
    request: Request,
    page: int = 1,
    search: Optional[str] = None,
    remote_only: bool = False,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """工作列表页面"""
    job_service = JobService(db)
    
    # 构建查询
    query = db.query(Job).filter(Job.is_active == True)
    
    if search:
        query = query.filter(
            Job.title.contains(search) |
            Job.title_zh.contains(search) |
            Job.company.contains(search) |
            Job.tags.contains(search)
        )
    
    if remote_only:
        query = query.filter(Job.remote == True)
    
    if source:
        query = query.filter(Job.source_website == source)
    
    # 分页
    per_page = 20
    offset = (page - 1) * per_page
    jobs = query.order_by(Job.scraped_date.desc()).offset(offset).limit(per_page).all()
    
    total_jobs = query.count()
    total_pages = (total_jobs + per_page - 1) // per_page
    
    return templates.TemplateResponse("jobs.html", {
        "request": request,
        "jobs": jobs,
        "current_page": page,
        "total_pages": total_pages,
        "search": search,
        "remote_only": remote_only,
        "source": source
    })

@app.get("/job/{job_id}", response_class=HTMLResponse)
async def job_detail(request: Request, job_id: int, db: Session = Depends(get_db)):
    """工作详情页面"""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="工作不存在")
    
    return templates.TemplateResponse("job_detail.html", {
        "request": request,
        "job": job
    })

@app.get("/api/jobs")
async def api_get_jobs(
    limit: int = 20,
    search: Optional[str] = None,
    remote_only: bool = False,
    db: Session = Depends(get_db)
):
    """API: 获取工作列表"""
    job_service = JobService(db)
    
    if search:
        jobs = job_service.get_jobs_by_keywords([search], limit)
    elif remote_only:
        jobs = job_service.get_remote_jobs(limit)
    else:
        jobs = job_service.get_recent_jobs(days=30, limit=limit)
    
    return [job.to_dict() for job in jobs]

@app.get("/api/stats")
async def api_get_stats(db: Session = Depends(get_db)):
    """API: 获取统计信息"""
    job_service = JobService(db)
    return job_service.get_job_statistics()

@app.post("/api/scrape")
async def api_scrape_now(db: Session = Depends(get_db)):
    """API: 立即抓取工作"""
    try:
        scheduler.run_once()
        return {"message": "抓取任务已启动", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"抓取失败: {str(e)}")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    """管理页面"""
    job_service = JobService(db)
    stats = job_service.get_job_statistics()
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "stats": stats
    })

@app.post("/admin/scrape")
async def admin_scrape(request: Request, db: Session = Depends(get_db)):
    """管理员触发抓取"""
    try:
        scheduler.run_once()
        return RedirectResponse(url="/admin?message=抓取任务已启动", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin?error={str(e)}", status_code=303)

@app.post("/admin/test-email")
async def admin_test_email(request: Request):
    """测试邮件发送"""
    try:
        notification_service = NotificationService()
        success = notification_service.send_email(
            "Web3工作抓取器测试邮件",
            "这是一封测试邮件，如果您收到此邮件，说明邮件配置正确。"
        )
        
        if success:
            return RedirectResponse(url="/admin?message=测试邮件发送成功", status_code=303)
        else:
            return RedirectResponse(url="/admin?error=测试邮件发送失败", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin?error={str(e)}", status_code=303)

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "12000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        access_log=True
    )