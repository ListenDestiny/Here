from .base_scraper import BaseScraper
from typing import List, Dict, Any
from datetime import datetime
import json

class AngelCoScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://angel.co", "AngelCo")
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """抓取AngelCo的Web3相关工作"""
        jobs = []
        
        # AngelCo的搜索URL，搜索Web3相关工作
        search_terms = ['web3', 'blockchain', 'crypto', 'defi', 'nft']
        
        for term in search_terms:
            if len(jobs) >= limit:
                break
                
            try:
                # 构建搜索URL
                url = f"{self.base_url}/jobs?keywords={term}"
                soup = self.get_page(url)
                
                # 查找工作列表
                job_cards = soup.find_all('div', class_='job-card') or soup.find_all('div', class_='startup-job')
                
                for card in job_cards:
                    if len(jobs) >= limit:
                        break
                    
                    job_data = self.parse_job_card(card)
                    if job_data and not any(j['url'] == job_data['url'] for j in jobs):
                        jobs.append(job_data)
                
                self.random_delay()
                
            except Exception as e:
                print(f"Error scraping AngelCo for term '{term}': {e}")
                continue
        
        return jobs
    
    def parse_job_card(self, card) -> Dict[str, Any]:
        """解析AngelCo工作卡片"""
        try:
            # 提取标题
            title_elem = card.find('h4') or card.find('h3') or card.find('a', class_='job-title')
            title = self.clean_text(title_elem.get_text()) if title_elem else "Unknown"
            
            # 获取工作链接
            link_elem = card.find('a') or title_elem
            job_url = link_elem.get('href', '') if link_elem else ''
            if job_url and not job_url.startswith('http'):
                job_url = self.base_url + job_url
            
            # 提取公司名称
            company_elem = card.find('span', class_='company-name') or card.find('a', class_='startup-link')
            company = self.clean_text(company_elem.get_text()) if company_elem else "Unknown"
            
            # 提取位置
            location_elem = card.find('span', class_='location') or card.find('div', class_='location')
            location = self.clean_text(location_elem.get_text()) if location_elem else ""
            
            # 检查远程工作
            remote = 'remote' in location.lower() or 'anywhere' in location.lower()
            
            # 提取薪资范围
            salary_elem = card.find('span', class_='salary-range') or card.find('div', class_='compensation')
            salary_text = self.clean_text(salary_elem.get_text()) if salary_elem else ""
            salary_min, salary_max = self.extract_salary(salary_text)
            
            # 提取工作类型
            job_type_elem = card.find('span', class_='job-type')
            job_type = self.clean_text(job_type_elem.get_text()) if job_type_elem else "full-time"
            
            # 提取经验要求
            experience_elem = card.find('span', class_='experience-level')
            experience_level = self.clean_text(experience_elem.get_text()) if experience_elem else "mid"
            
            # 提取技能标签
            tags_elems = card.find_all('span', class_='tag') or card.find_all('div', class_='skill')
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
                'experience_level': experience_level.lower()
            }
            
        except Exception as e:
            print(f"Error parsing AngelCo job card: {e}")
            return None
    
    def parse_job_detail(self, job_url: str) -> Dict[str, Any]:
        """解析AngelCo工作详情页面"""
        try:
            soup = self.get_page(job_url)
            
            # 提取工作描述
            description_elem = soup.find('div', class_='job-description') or soup.find('section', class_='description')
            description = self.clean_text(description_elem.get_text()) if description_elem else ""
            
            # 提取工作要求
            requirements_elem = soup.find('div', class_='requirements') or soup.find('section', class_='qualifications')
            requirements = self.clean_text(requirements_elem.get_text()) if requirements_elem else ""
            
            # 提取公司信息
            company_info_elem = soup.find('div', class_='company-info')
            company_description = self.clean_text(company_info_elem.get_text()) if company_info_elem else ""
            
            return {
                'description': description,
                'requirements': requirements,
                'company_description': company_description
            }
            
        except Exception as e:
            print(f"Error parsing AngelCo job detail {job_url}: {e}")
            return {}