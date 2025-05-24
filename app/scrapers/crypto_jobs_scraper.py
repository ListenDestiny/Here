from .base_scraper import BaseScraper
from typing import List, Dict, Any
from datetime import datetime
import re

class CryptoJobsScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://cryptojobslist.com", "CryptoJobsList")
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """抓取CryptoJobsList的工作信息"""
        jobs = []
        page = 1
        
        while len(jobs) < limit:
            try:
                url = f"{self.base_url}/jobs?page={page}"
                soup = self.get_page(url)
                
                job_cards = soup.find_all('div', class_='job-card') or soup.find_all('a', class_='job-link')
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    if len(jobs) >= limit:
                        break
                    
                    job_data = self.parse_job_card(card)
                    if job_data:
                        jobs.append(job_data)
                
                page += 1
                self.random_delay()
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
        
        return jobs
    
    def parse_job_card(self, card) -> Dict[str, Any]:
        """解析工作卡片"""
        try:
            # 提取基本信息
            title_elem = card.find('h3') or card.find('h2') or card.find('a')
            title = self.clean_text(title_elem.get_text()) if title_elem else "Unknown"
            
            # 获取工作链接
            link_elem = card.find('a') or card
            job_url = link_elem.get('href', '') if link_elem else ''
            if job_url and not job_url.startswith('http'):
                job_url = self.base_url + job_url
            
            # 提取公司名称
            company_elem = card.find('span', class_='company') or card.find('div', class_='company')
            company = self.clean_text(company_elem.get_text()) if company_elem else "Unknown"
            
            # 提取位置信息
            location_elem = card.find('span', class_='location') or card.find('div', class_='location')
            location = self.clean_text(location_elem.get_text()) if location_elem else ""
            
            # 检查是否远程工作
            remote = 'remote' in location.lower() or 'anywhere' in location.lower()
            
            # 提取薪资信息
            salary_elem = card.find('span', class_='salary') or card.find('div', class_='salary')
            salary_text = self.clean_text(salary_elem.get_text()) if salary_elem else ""
            salary_min, salary_max = self.extract_salary(salary_text)
            
            # 提取标签
            tags_elems = card.find_all('span', class_='tag') or card.find_all('div', class_='tag')
            tags = [self.clean_text(tag.get_text()) for tag in tags_elems]
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'remote': remote,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'currency': 'USD',
                'url': job_url,
                'source_website': self.name,
                'tags': ','.join(tags),
                'posted_date': datetime.now(),
                'job_type': 'full-time',
                'experience_level': 'mid'
            }
            
        except Exception as e:
            print(f"Error parsing job card: {e}")
            return None
    
    def parse_job_detail(self, job_url: str) -> Dict[str, Any]:
        """解析工作详情页面"""
        try:
            soup = self.get_page(job_url)
            
            # 提取描述
            description_elem = soup.find('div', class_='job-description') or soup.find('div', class_='description')
            description = self.clean_text(description_elem.get_text()) if description_elem else ""
            
            # 提取要求
            requirements_elem = soup.find('div', class_='requirements') or soup.find('div', class_='job-requirements')
            requirements = self.clean_text(requirements_elem.get_text()) if requirements_elem else ""
            
            return {
                'description': description,
                'requirements': requirements
            }
            
        except Exception as e:
            print(f"Error parsing job detail {job_url}: {e}")
            return {}