"""
CryptoRecruit.com 抓取器
专注于加密货币和区块链招聘
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base_scraper import BaseScraper


class CryptoRecruitScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://www.cryptorecruit.com", name="CryptoRecruit")
        
        # CryptoRecruit.com 风格的工作数据
        self.sample_jobs = [
            {
                "title": "Head of Blockchain Engineering",
                "company": "Binance",
                "location": "Singapore",
                "description": "Lead a team of blockchain engineers to build and maintain the world's largest cryptocurrency exchange infrastructure. Drive technical strategy and innovation.",
                "requirements": "10+ years engineering leadership experience, deep blockchain expertise, experience scaling high-throughput systems",
                "salary_min": 200000,
                "salary_max": 350000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/binance-head-engineering",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "executive",
                "tags": "Leadership,Blockchain,Exchange,Binance,Singapore"
            },
            {
                "title": "Smart Contract Developer",
                "company": "MakerDAO",
                "location": "Remote",
                "description": "Develop and maintain smart contracts for the Maker Protocol. Work on the DAI stablecoin system and governance mechanisms.",
                "requirements": "3+ years Solidity development, experience with DeFi protocols, understanding of stablecoin mechanisms",
                "salary_min": 100000,
                "salary_max": 160000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/makerdao-solidity",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Solidity,DeFi,Stablecoin,MakerDAO,DAI"
            },
            {
                "title": "Cryptocurrency Trading Analyst",
                "company": "Jump Trading",
                "location": "Chicago, IL",
                "description": "Analyze cryptocurrency markets and develop algorithmic trading strategies. Work with quantitative researchers to optimize trading performance.",
                "requirements": "Strong quantitative background, experience with financial markets, knowledge of cryptocurrency trading",
                "salary_min": 120000,
                "salary_max": 200000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/jump-trading-analyst",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Trading,Quantitative,Crypto Markets,Jump Trading"
            },
            {
                "title": "Blockchain Infrastructure Engineer",
                "company": "Coinbase",
                "location": "San Francisco, CA",
                "description": "Build and maintain blockchain infrastructure for one of the largest cryptocurrency platforms. Ensure high availability and security.",
                "requirements": "5+ years infrastructure engineering, experience with blockchain nodes, knowledge of cloud platforms",
                "salary_min": 140000,
                "salary_max": 220000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/coinbase-infrastructure",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Infrastructure,Blockchain Nodes,Coinbase,Cloud"
            },
            {
                "title": "DeFi Research Scientist",
                "company": "Compound Labs",
                "location": "Remote",
                "description": "Research and develop new DeFi protocols and mechanisms. Publish research papers and contribute to the academic blockchain community.",
                "requirements": "PhD in Computer Science or related field, research experience in cryptography or distributed systems",
                "salary_min": 150000,
                "salary_max": 250000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/compound-research",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Research,DeFi,PhD,Compound,Academic"
            },
            {
                "title": "Crypto Marketing Manager",
                "company": "FTX",
                "location": "Miami, FL",
                "description": "Lead marketing campaigns for cryptocurrency exchange and trading platform. Develop brand strategy and community engagement initiatives.",
                "requirements": "5+ years marketing experience, knowledge of cryptocurrency industry, experience with digital marketing",
                "salary_min": 90000,
                "salary_max": 140000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/ftx-marketing",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Marketing,Crypto Exchange,FTX,Brand Strategy"
            },
            {
                "title": "Blockchain Legal Counsel",
                "company": "Ripple",
                "location": "New York, NY",
                "description": "Provide legal guidance on blockchain and cryptocurrency matters. Work with regulatory bodies and ensure compliance with evolving regulations.",
                "requirements": "JD from accredited law school, experience with financial regulations, knowledge of blockchain technology",
                "salary_min": 160000,
                "salary_max": 250000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/ripple-legal",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Legal,Compliance,Ripple,Regulation,JD"
            },
            {
                "title": "NFT Platform Developer",
                "company": "SuperRare",
                "location": "Remote",
                "description": "Develop features for digital art NFT marketplace. Work on creator tools, marketplace functionality, and blockchain integration.",
                "requirements": "4+ years web development, experience with NFT standards, knowledge of digital art and creator economy",
                "salary_min": 110000,
                "salary_max": 170000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/superrare-nft",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "NFT,Digital Art,SuperRare,Creator Economy"
            },
            {
                "title": "Crypto Custody Engineer",
                "company": "BitGo",
                "location": "Palo Alto, CA",
                "description": "Build secure cryptocurrency custody solutions for institutional clients. Implement multi-signature wallets and security protocols.",
                "requirements": "Strong security background, experience with cryptographic systems, knowledge of cryptocurrency custody",
                "salary_min": 130000,
                "salary_max": 190000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/bitgo-custody",
                "remote": False,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Custody,Security,Multi-sig,BitGo,Institutional"
            },
            {
                "title": "Web3 UX Designer",
                "company": "MetaMask",
                "location": "Remote",
                "description": "Design user experiences for the leading Web3 wallet. Create intuitive interfaces for complex blockchain interactions.",
                "requirements": "5+ years UX design experience, understanding of Web3 user flows, experience with design systems",
                "salary_min": 100000,
                "salary_max": 150000,
                "currency": "USD",
                "url": "https://www.cryptorecruit.com/job/metamask-ux",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "UX Design,Web3,MetaMask,Wallet,User Experience"
            }
        ]
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        模拟从CryptoRecruit.com抓取工作数据
        """
        try:
            # 随机选择一些工作进行返回
            num_jobs = min(random.randint(3, 6), len(self.sample_jobs))
            selected_jobs = random.sample(self.sample_jobs, num_jobs)
            
            # 为每个工作添加时间戳和来源
            jobs = []
            for job in selected_jobs:
                job_data = job.copy()
                job_data.update({
                    "source_website": self.name,
                    "posted_date": datetime.now() - timedelta(days=random.randint(0, 10)),
                    "scraped_date": datetime.now(),
                    "is_active": True,
                    "is_translated": False
                })
                jobs.append(job_data)
            
            print(f"从 {self.name} 模拟抓取到 {len(jobs)} 个加密货币工作")
            return jobs
            
        except Exception as e:
            print(f"从 {self.name} 抓取工作时出错: {str(e)}")
            return []
    
    def parse_job_detail(self, job_url: str) -> Dict[str, Any]:
        """
        解析工作详情页面
        """
        # 模拟解析工作详情
        return {
            "detailed_description": "详细的工作描述...",
            "benefits": ["竞争性薪资", "股权期权", "健康保险", "401k匹配"],
            "team_size": random.randint(20, 500),
            "company_stage": random.choice(["Startup", "Growth", "Established", "Public"])
        }