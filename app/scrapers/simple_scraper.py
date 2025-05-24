"""
简化的Web3工作爬虫 - 使用模拟数据进行演示
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

class SimpleWeb3Scraper:
    """简化的Web3工作爬虫，用于演示功能"""
    
    def __init__(self):
        self.name = "SimpleWeb3Scraper"
        
        # 模拟的Web3工作数据
        self.sample_jobs = [
            {
                "title": "Senior Blockchain Developer",
                "company": "DeFi Protocol",
                "location": "Remote",
                "description": "We are looking for an experienced blockchain developer to join our DeFi protocol team. You will be responsible for developing smart contracts, implementing security measures, and optimizing gas efficiency.",
                "requirements": "5+ years of Solidity experience, knowledge of DeFi protocols, experience with testing frameworks",
                "salary_min": 120000,
                "salary_max": 180000,
                "currency": "USD",
                "url": "https://remote3.co/jobs/blockchain-developer-001",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Solidity,DeFi,Smart Contracts,Ethereum"
            },
            {
                "title": "Web3 Frontend Engineer",
                "company": "NFT Marketplace",
                "location": "San Francisco, CA",
                "description": "Join our team to build the next generation NFT marketplace. You'll work with React, Web3.js, and modern frontend technologies to create amazing user experiences.",
                "requirements": "React, TypeScript, Web3.js, experience with wallet integration",
                "salary_min": 100000,
                "salary_max": 150000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/jobs/frontend-engineer-002",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "React,Web3.js,NFT,Frontend"
            },
            {
                "title": "Crypto Product Manager",
                "company": "Blockchain Startup",
                "location": "Remote",
                "description": "Lead product development for our cryptocurrency exchange platform. Define product roadmap, work with engineering teams, and drive user adoption.",
                "requirements": "Product management experience, understanding of crypto markets, data-driven approach",
                "salary_min": 130000,
                "salary_max": 200000,
                "currency": "USD",
                "url": "https://web3.career/jobs",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Product Management,Crypto,Exchange,Strategy"
            },
            {
                "title": "Smart Contract Auditor",
                "company": "Security Firm",
                "location": "New York, NY",
                "description": "Conduct security audits of smart contracts for various DeFi protocols. Identify vulnerabilities and provide recommendations for improvements.",
                "requirements": "Deep understanding of Solidity, security best practices, audit experience",
                "salary_min": 140000,
                "salary_max": 220000,
                "currency": "USD",
                "url": "https://cryptocurrencyjobs.co/jobs",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Security,Audit,Solidity,DeFi"
            },
            {
                "title": "DevOps Engineer - Blockchain Infrastructure",
                "company": "Layer 2 Solution",
                "location": "Remote",
                "description": "Build and maintain blockchain infrastructure for our Layer 2 scaling solution. Work with Kubernetes, Docker, and blockchain nodes.",
                "requirements": "DevOps experience, Kubernetes, Docker, blockchain node management",
                "salary_min": 110000,
                "salary_max": 160000,
                "currency": "USD",
                "url": "https://angel.co/jobs",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "DevOps,Kubernetes,Blockchain,Infrastructure"
            },
            {
                "title": "Web3 UX Designer",
                "company": "DApp Studio",
                "location": "Berlin, Germany",
                "description": "Design intuitive user experiences for decentralized applications. Create user flows, wireframes, and prototypes for Web3 products.",
                "requirements": "UX design experience, understanding of Web3 concepts, Figma proficiency",
                "salary_min": 70000,
                "salary_max": 100000,
                "currency": "EUR",
                "url": "https://jobs.lever.co/jobs",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "UX Design,DApp,Figma,Web3"
            },
            {
                "title": "Blockchain Data Analyst",
                "company": "Analytics Platform",
                "location": "Remote",
                "description": "Analyze on-chain data to provide insights for DeFi protocols and crypto projects. Build dashboards and reports for stakeholders.",
                "requirements": "Data analysis skills, SQL, Python, understanding of blockchain data",
                "salary_min": 90000,
                "salary_max": 130000,
                "currency": "USD",
                "url": "https://remote3.co/jobs/data-analyst-007",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Data Analysis,SQL,Python,On-chain Data"
            },
            {
                "title": "Tokenomics Specialist",
                "company": "GameFi Project",
                "location": "Remote",
                "description": "Design and implement tokenomics models for our play-to-earn gaming platform. Balance game economy and token utility.",
                "requirements": "Economics background, game design experience, understanding of token mechanics",
                "salary_min": 100000,
                "salary_max": 150000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/jobs/tokenomics-specialist-008",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Tokenomics,GameFi,Economics,Game Design"
            }
        ]
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        模拟抓取工作数据
        """
        try:
            # 随机选择一些工作进行返回，模拟实际抓取
            num_jobs = min(random.randint(3, 6), len(self.sample_jobs))
            selected_jobs = random.sample(self.sample_jobs, num_jobs)
            
            # 为每个工作添加时间戳和来源
            jobs = []
            for job in selected_jobs:
                job_data = job.copy()
                job_data.update({
                    "source_website": self.name,
                    "posted_date": datetime.now() - timedelta(days=random.randint(0, 7)),
                    "scraped_date": datetime.now(),
                    "is_active": True,
                    "is_translated": False
                })
                jobs.append(job_data)
            
            print(f"从 {self.name} 模拟抓取到 {len(jobs)} 个工作")
            return jobs
            
        except Exception as e:
            print(f"抓取过程中出现错误: {str(e)}")
            return []
    
    def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """
        获取工作详情（模拟）
        """
        return {
            "full_description": "这是一个详细的工作描述...",
            "benefits": ["健康保险", "远程工作", "股票期权", "学习津贴"],
            "application_process": "请发送简历到 jobs@example.com"
        }