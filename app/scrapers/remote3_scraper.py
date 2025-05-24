"""
Remote3.co 抓取器
专注于远程Web3工作机会
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base_scraper import BaseScraper


class Remote3Scraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://remote3.co", name="Remote3")
        
        # Remote3.co 风格的工作数据
        self.sample_jobs = [
            {
                "title": "Senior DeFi Protocol Engineer",
                "company": "Aave Protocol",
                "location": "Remote",
                "description": "Lead the development of next-generation DeFi lending protocols. Work with cutting-edge blockchain technology to build secure and scalable financial infrastructure.",
                "requirements": "7+ years of software engineering experience, 3+ years in DeFi/blockchain, expertise in Solidity and smart contract security",
                "salary_min": 150000,
                "salary_max": 250000,
                "currency": "USD",
                "url": "https://remote3.co/job/aave-defi-engineer",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "DeFi,Solidity,Smart Contracts,Aave,Protocol Development"
            },
            {
                "title": "Web3 Frontend Developer",
                "company": "Uniswap Labs",
                "location": "Remote",
                "description": "Build beautiful and intuitive user interfaces for decentralized applications. Create seamless user experiences for DeFi protocols.",
                "requirements": "5+ years React/TypeScript experience, Web3.js/Ethers.js knowledge, understanding of DeFi protocols",
                "salary_min": 120000,
                "salary_max": 180000,
                "currency": "USD",
                "url": "https://remote3.co/job/uniswap-frontend",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "React,TypeScript,Web3.js,DeFi,Frontend"
            },
            {
                "title": "Blockchain Security Researcher",
                "company": "ConsenSys Diligence",
                "location": "Remote",
                "description": "Conduct security audits of smart contracts and blockchain protocols. Identify vulnerabilities and provide recommendations for secure development practices.",
                "requirements": "Strong background in cryptography and security, experience with smart contract auditing, knowledge of common attack vectors",
                "salary_min": 130000,
                "salary_max": 200000,
                "currency": "USD",
                "url": "https://remote3.co/job/consensys-security",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Security,Smart Contract Audit,Cryptography,ConsenSys"
            },
            {
                "title": "NFT Marketplace Developer",
                "company": "OpenSea",
                "location": "Remote",
                "description": "Develop and maintain the world's largest NFT marketplace. Work on scaling solutions and new features for digital asset trading.",
                "requirements": "4+ years full-stack development, experience with NFT standards (ERC-721, ERC-1155), knowledge of IPFS and metadata standards",
                "salary_min": 140000,
                "salary_max": 220000,
                "currency": "USD",
                "url": "https://remote3.co/job/opensea-nft-dev",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "NFT,ERC-721,IPFS,Marketplace,OpenSea"
            },
            {
                "title": "Layer 2 Protocol Engineer",
                "company": "Polygon Technology",
                "location": "Remote",
                "description": "Build and optimize Layer 2 scaling solutions for Ethereum. Work on state-of-the-art blockchain infrastructure and consensus mechanisms.",
                "requirements": "Deep understanding of blockchain consensus, experience with Layer 2 solutions, proficiency in Go or Rust",
                "salary_min": 160000,
                "salary_max": 280000,
                "currency": "USD",
                "url": "https://remote3.co/job/polygon-l2-engineer",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Layer 2,Polygon,Scaling,Consensus,Go,Rust"
            },
            {
                "title": "Web3 Product Manager",
                "company": "Chainlink Labs",
                "location": "Remote",
                "description": "Drive product strategy for decentralized oracle networks. Work with cross-functional teams to deliver innovative blockchain solutions.",
                "requirements": "5+ years product management experience, deep understanding of blockchain ecosystems, experience with developer tools",
                "salary_min": 130000,
                "salary_max": 190000,
                "currency": "USD",
                "url": "https://remote3.co/job/chainlink-pm",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "senior",
                "tags": "Product Management,Oracles,Chainlink,Strategy"
            },
            {
                "title": "DeFi Quantitative Analyst",
                "company": "1inch Network",
                "location": "Remote",
                "description": "Analyze DeFi markets and develop trading strategies. Build models for liquidity optimization and yield farming protocols.",
                "requirements": "Strong background in quantitative finance, experience with DeFi protocols, proficiency in Python and data analysis",
                "salary_min": 110000,
                "salary_max": 170000,
                "currency": "USD",
                "url": "https://remote3.co/job/1inch-quant",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Quantitative Analysis,DeFi,Trading,Python,1inch"
            },
            {
                "title": "Crypto Compliance Officer",
                "company": "Circle",
                "location": "Remote",
                "description": "Ensure regulatory compliance for digital asset operations. Work with legal teams to navigate evolving cryptocurrency regulations.",
                "requirements": "Law degree or compliance certification, experience with financial regulations, knowledge of cryptocurrency compliance frameworks",
                "salary_min": 100000,
                "salary_max": 150000,
                "currency": "USD",
                "url": "https://remote3.co/job/circle-compliance",
                "remote": True,
                "job_type": "full-time",
                "experience_level": "mid",
                "tags": "Compliance,Regulation,Legal,USDC,Circle"
            }
        ]
    
    def scrape_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        模拟从Remote3.co抓取工作数据
        """
        try:
            # 随机选择一些工作进行返回
            num_jobs = min(random.randint(4, 7), len(self.sample_jobs))
            selected_jobs = random.sample(self.sample_jobs, num_jobs)
            
            # 为每个工作添加时间戳和来源
            jobs = []
            for job in selected_jobs:
                job_data = job.copy()
                job_data.update({
                    "source_website": self.name,
                    "posted_date": datetime.now() - timedelta(days=random.randint(0, 14)),
                    "scraped_date": datetime.now(),
                    "is_active": True,
                    "is_translated": False
                })
                jobs.append(job_data)
            
            print(f"从 {self.name} 模拟抓取到 {len(jobs)} 个远程Web3工作")
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
            "benefits": ["远程工作", "股权激励", "健康保险", "学习津贴"],
            "team_size": random.randint(10, 100),
            "company_stage": random.choice(["Series A", "Series B", "Series C", "Public"])
        }