import schedule
import time
import threading
from datetime import datetime
from .database import SessionLocal, create_tables
from .services.job_service import JobService
from .services.notification_service import NotificationService

class JobScheduler:
    def __init__(self):
        self.notification_service = NotificationService()
        self.running = False
        self.thread = None
    
    def scrape_and_notify(self):
        """抓取工作并发送通知"""
        print(f"开始定时抓取工作 - {datetime.now()}")
        
        db = SessionLocal()
        try:
            job_service = JobService(db)
            
            # 抓取所有工作
            all_jobs = job_service.scrape_all_jobs(limit_per_site=30)
            print(f"总共抓取到 {len(all_jobs)} 个工作")
            
            # 保存到数据库
            new_jobs_count = job_service.save_jobs_to_db(all_jobs)
            print(f"保存了 {new_jobs_count} 个新工作")
            
            # 获取今天的新工作
            recent_jobs = job_service.get_recent_jobs(days=1, limit=50)
            
            # 发送每日报告
            if recent_jobs:
                success = self.notification_service.send_daily_job_report(recent_jobs)
                if success:
                    print("每日工作报告发送成功")
                else:
                    print("每日工作报告发送失败")
            
            # 发送抓取摘要
            errors = []  # 这里可以收集抓取过程中的错误
            self.notification_service.send_scraping_summary(
                total_scraped=len(all_jobs),
                new_jobs=new_jobs_count,
                errors=errors
            )
            
        except Exception as e:
            print(f"定时任务执行出错: {e}")
            # 发送错误通知
            self.notification_service.send_email(
                "Web3工作抓取错误",
                f"定时任务执行时发生错误: {str(e)}"
            )
        finally:
            db.close()
    
    def update_translations(self):
        """更新翻译"""
        print(f"开始更新翻译 - {datetime.now()}")
        
        db = SessionLocal()
        try:
            job_service = JobService(db)
            job_service.update_job_translations(limit=20)
            print("翻译更新完成")
        except Exception as e:
            print(f"更新翻译时出错: {e}")
        finally:
            db.close()
    
    def setup_schedule(self):
        """设置定时任务"""
        # 每天早上9点抓取工作
        schedule.every().day.at("09:00").do(self.scrape_and_notify)
        
        # 每天晚上6点再抓取一次
        schedule.every().day.at("18:00").do(self.scrape_and_notify)
        
        # 每2小时更新一次翻译
        schedule.every(2).hours.do(self.update_translations)
        
        # 测试用：每5分钟执行一次（可以注释掉）
        # schedule.every(5).minutes.do(self.scrape_and_notify)
        
        print("定时任务已设置:")
        print("- 每天 09:00 和 18:00 抓取工作")
        print("- 每2小时更新翻译")
    
    def run_scheduler(self):
        """运行调度器"""
        self.setup_schedule()
        self.running = True
        
        print("调度器开始运行...")
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def start(self):
        """启动调度器线程"""
        if not self.running:
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            print("调度器线程已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("调度器已停止")
    
    def run_once(self):
        """立即执行一次抓取"""
        print("立即执行抓取任务...")
        self.scrape_and_notify()

# 全局调度器实例
scheduler = JobScheduler()