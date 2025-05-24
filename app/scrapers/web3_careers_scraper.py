from .base_scraper import BaseScraper
from typing import List, Dict, Any
from datetime import datetime
import json

class Web3CareersScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://web3.career", "Web3Career")
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """抓取Web3.career的工作信息"""
        jobs = []
        page = 1
        
        while len(jobs) < limit:
            try:
                url = f"{self.base_url}/jobs?page={page}"
                soup = self.get_page(url)
                
                # 查找工作列表
                job_items = soup.find_all('div', class_='job-item') or soup.find_all('tr', class_='job-row')
                
                if not job_items:
                    # 尝试查找其他可能的选择器
                    job_items = soup.find_all('a', href=lambda x: x and '/job/' in x)
                
                if not job_items:
                    break
                
                for item in job_items:
                    if len(jobs) >= limit:
                        break
                    
                    job_data = self.parse_job_item(item)
                    if job_data:
                        jobs.append(job_data)
                
                page += 1
                self.random_delay()
                
            except Exception as e:
                print(f"Error scraping Web3.career page {page}: {e}")
                break
        
        return jobs
    
    def parse_job_item(self, item) -> Dict[str, Any]:
        """解析工作项目"""
        try:
            # 提取标题
            title_elem = item.find('h3') or item.find('h2') or item.find('a')
            title = self.clean_text(title_elem.get_text()) if title_elem else "Unknown"
            
            # 获取工作链接
            link_elem = item.find('a') or item
            job_url = link_elem.get('href', '') if link_elem else ''
            if job_url and not job_url.startswith('http'):
                job_url = self.base_url + job_url
            
            # 提取公司名称
            company_elem = item.find('span', class_='company-name') or item.find('div', class_='company')
            company = self.clean_text(company_elem.get_text()) if company_elem else "Unknown"
            
            # 提取位置
            location_elem = item.find('span', class_='location') or item.find('div', class_='location')
            location = self.clean_text(location_elem.get_text()) if location_elem else ""
            
            # 检查远程工作
            remote = any(keyword in location.lower() for keyword in ['remote', 'anywhere', 'global'])
            
            # 提取薪资
            salary_elem = item.find('span', class_='salary') or item.find('div', class_='salary')
            salary_text = self.clean_text(salary_elem.get_text()) if salary_elem else ""
            salary_min, salary_max = self.extract_salary(salary_text)
            
            # 提取工作类型
            job_type_elem = item.find('span', class_='job-type') or item.find('div', class_='job-type')
            job_type = self.clean_text(job_type_elem.get_text()) if job_type_elem else "full-time"
            
            # 提取技能标签
            tags_elems = item.find_all('span', class_='skill-tag') or item.find_all('div', class_='tag')
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
                'job_type': job_type.lower(),
                'experience_level': 'mid'
            }
            
        except Exception as e:
            print(f"Error parsing Web3.career job item: {e}")
            return None
    
    def parse_job_detail(self, job_url: str) -> Dict[str, Any]:
        """解析工作详情页面"""
        try:
            soup = self.get_page(job_url)
            
            # 提取工作描述
            description_elem = soup.find('div', class_='job-description') or soup.find('section', class_='description')
            description = self.clean_text(description_elem.get_text()) if description_elem else ""
            
            # 提取工作要求
            requirements_elem = soup.find('div', class_='job-requirements') or soup.find('section', class_='requirements')
            requirements = self.clean_text(requirements_elem.get_text()) if requirements_elem else ""
            
            # 提取更多详细信息
            details = {}
            
            # 尝试提取经验要求
            experience_elem = soup.find('span', string=lambda x: x and 'experience' in x.lower())
            if experience_elem:
                details['experience_level'] = self.clean_text(experience_elem.get_text())
            
            return {
                'description': description,
                'requirements': requirements,
                **details
            }
            
        except Exception as e:
            print(f"Error parsing Web3.career job detail {job_url}: {e}")
            return {}