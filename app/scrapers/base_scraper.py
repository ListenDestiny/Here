from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_page(self, url: str, retries: int = 3) -> BeautifulSoup:
        """获取页面内容"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                print(f"Error fetching {url} (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))
                else:
                    raise
    
    def random_delay(self, min_seconds: float = 1, max_seconds: float = 3):
        """随机延迟，避免被反爬虫"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    @abstractmethod
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """抓取工作信息"""
        pass
    
    @abstractmethod
    def parse_job_detail(self, job_url: str) -> Dict[str, Any]:
        """解析工作详情"""
        pass
    
    def clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        return text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    def extract_salary(self, salary_text: str) -> tuple:
        """提取薪资范围"""
        if not salary_text:
            return None, None
        
        # 简单的薪资提取逻辑，可以根据需要扩展
        import re
        numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', salary_text.replace(',', ''))
        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])
        elif len(numbers) == 1:
            return float(numbers[0]), None
        return None, None