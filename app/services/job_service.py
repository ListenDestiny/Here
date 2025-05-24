from sqlalchemy.orm import Session
from ..models.job import Job
from ..scrapers.web3_career_scraper import Web3CareerScraper
from .translation_service import TranslationService
from typing import List, Dict, Any
from datetime import datetime, timedelta
import asyncio

class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.translation_service = TranslationService()
        self.scrapers = [
            Web3CareerScraper()
        ]
    
    def scrape_all_jobs(self, limit_per_site: int = 20) -> List[Dict[str, Any]]:
        """从所有网站抓取工作并保存到数据库"""
        all_jobs = []
        
        for scraper in self.scrapers:
            try:
                print(f"正在抓取 {scraper.name}...")
                jobs = scraper.scrape_jobs(limit_per_site)
                
                # 为每个工作获取详细信息
                for job in jobs:
                    if job.get('url'):
                        try:
                            details = scraper.parse_job_detail(job['url'])
                            job.update(details)
                        except Exception as e:
                            print(f"获取工作详情失败 {job['url']}: {e}")
                
                all_jobs.extend(jobs)
                print(f"从 {scraper.name} 抓取到 {len(jobs)} 个工作")
                
            except Exception as e:
                print(f"抓取 {scraper.name} 时出错: {e}")
        
        # 保存所有工作到数据库
        if all_jobs:
            saved_count = self.save_jobs_to_db(all_jobs)
            print(f"总共保存了 {saved_count} 个新工作到数据库")
        
        return all_jobs
    
    def save_jobs_to_db(self, jobs_data: List[Dict[str, Any]]) -> int:
        """保存工作到数据库"""
        saved_count = 0
        
        # 获取Job模型的有效字段
        valid_fields = {column.name for column in Job.__table__.columns}
        
        for job_data in jobs_data:
            try:
                # 检查是否已存在
                existing_job = self.db.query(Job).filter(Job.url == job_data['url']).first()
                
                if not existing_job:
                    # 翻译工作信息
                    translated_data = self.translation_service.translate_job_fields(job_data)
                    
                    # 过滤掉无效字段
                    filtered_data = {k: v for k, v in translated_data.items() if k in valid_fields}
                    
                    # 创建新工作记录
                    job = Job(**filtered_data)
                    self.db.add(job)
                    saved_count += 1
                else:
                    # 更新现有记录（如果需要翻译）
                    if not existing_job.is_translated:
                        translated_data = self.translation_service.translate_job_fields(job_data)
                        # 过滤掉无效字段
                        filtered_data = {k: v for k, v in translated_data.items() if k in valid_fields}
                        for key, value in filtered_data.items():
                            if hasattr(existing_job, key):
                                setattr(existing_job, key, value)
                
            except Exception as e:
                print(f"保存工作时出错: {e}")
                continue
        
        try:
            self.db.commit()
            print(f"成功保存 {saved_count} 个新工作到数据库")
        except Exception as e:
            self.db.rollback()
            print(f"提交数据库时出错: {e}")
            saved_count = 0
        
        return saved_count
    
    def get_recent_jobs(self, days: int = 7, limit: int = 50) -> List[Job]:
        """获取最近的工作"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return self.db.query(Job).filter(
            Job.scraped_date >= cutoff_date,
            Job.is_active == True
        ).order_by(Job.scraped_date.desc()).limit(limit).all()
    
    def get_jobs_by_keywords(self, keywords: List[str], limit: int = 50) -> List[Job]:
        """根据关键词搜索工作"""
        query = self.db.query(Job).filter(Job.is_active == True)
        
        for keyword in keywords:
            query = query.filter(
                Job.title.contains(keyword) |
                Job.title_zh.contains(keyword) |
                Job.description.contains(keyword) |
                Job.description_zh.contains(keyword) |
                Job.tags.contains(keyword)
            )
        
        return query.order_by(Job.scraped_date.desc()).limit(limit).all()
    
    def get_remote_jobs(self, limit: int = 50) -> List[Job]:
        """获取远程工作"""
        return self.db.query(Job).filter(
            Job.remote == True,
            Job.is_active == True
        ).order_by(Job.scraped_date.desc()).limit(limit).all()
    
    def get_jobs_by_salary_range(self, min_salary: float, max_salary: float = None, limit: int = 50) -> List[Job]:
        """根据薪资范围获取工作"""
        query = self.db.query(Job).filter(
            Job.is_active == True,
            Job.salary_min >= min_salary
        )
        
        if max_salary:
            query = query.filter(Job.salary_max <= max_salary)
        
        return query.order_by(Job.scraped_date.desc()).limit(limit).all()
    
    def update_job_translations(self, limit: int = 10):
        """更新未翻译的工作"""
        untranslated_jobs = self.db.query(Job).filter(
            Job.is_translated == False
        ).limit(limit).all()
        
        for job in untranslated_jobs:
            try:
                job_data = {
                    'title': job.title,
                    'description': job.description,
                    'requirements': job.requirements
                }
                
                translated_data = self.translation_service.translate_job_fields(job_data)
                
                job.title_zh = translated_data.get('title_zh')
                job.description_zh = translated_data.get('description_zh')
                job.requirements_zh = translated_data.get('requirements_zh')
                job.is_translated = True
                
            except Exception as e:
                print(f"翻译工作 {job.id} 时出错: {e}")
        
        try:
            self.db.commit()
            print(f"更新了 {len(untranslated_jobs)} 个工作的翻译")
        except Exception as e:
            self.db.rollback()
            print(f"更新翻译时出错: {e}")
    
    def get_job_statistics(self) -> Dict[str, Any]:
        """获取工作统计信息"""
        total_jobs = self.db.query(Job).filter(Job.is_active == True).count()
        recent_jobs = self.db.query(Job).filter(
            Job.scraped_date >= datetime.now() - timedelta(days=7),
            Job.is_active == True
        ).count()
        remote_jobs = self.db.query(Job).filter(
            Job.remote == True,
            Job.is_active == True
        ).count()
        translated_jobs = self.db.query(Job).filter(
            Job.is_translated == True,
            Job.is_active == True
        ).count()
        
        # 按来源网站统计
        source_stats = {}
        for scraper in self.scrapers:
            count = self.db.query(Job).filter(
                Job.source_website == scraper.name,
                Job.is_active == True
            ).count()
            source_stats[scraper.name] = count
        
        return {
            'total_jobs': total_jobs,
            'recent_jobs': recent_jobs,
            'remote_jobs': remote_jobs,
            'translated_jobs': translated_jobs,
            'source_stats': source_stats
        }