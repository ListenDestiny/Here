from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_zh = Column(String(255))  # 中文标题
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    remote = Column(Boolean, default=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    currency = Column(String(10), default="USD")
    description = Column(Text)
    description_zh = Column(Text)  # 中文描述
    requirements = Column(Text)
    requirements_zh = Column(Text)  # 中文要求
    url = Column(String(500), unique=True, nullable=False)
    source_website = Column(String(100), nullable=False)
    job_type = Column(String(50))  # full-time, part-time, contract
    experience_level = Column(String(50))  # junior, mid, senior
    tags = Column(String(500))  # 技能标签，逗号分隔
    posted_date = Column(DateTime)
    scraped_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    is_translated = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'title_zh': self.title_zh,
            'company': self.company,
            'location': self.location,
            'remote': self.remote,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'currency': self.currency,
            'description': self.description,
            'description_zh': self.description_zh,
            'requirements': self.requirements,
            'requirements_zh': self.requirements_zh,
            'url': self.url,
            'source_website': self.source_website,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'tags': self.tags.split(',') if self.tags else [],
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None,
            'is_active': self.is_active,
            'is_translated': self.is_translated
        }