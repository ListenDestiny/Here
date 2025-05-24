import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from ..models.job import Job
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    def send_email(self, subject: str, body: str, is_html: bool = False) -> bool:
        """发送邮件"""
        if not all([self.email_user, self.email_password, self.recipient_email]):
            print("邮件配置不完整，跳过发送邮件")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html' if is_html else 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_user, self.recipient_email, text)
            server.quit()
            
            print(f"邮件发送成功: {subject}")
            return True
            
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False
    
    def format_job_email(self, jobs: List[Job]) -> str:
        """格式化工作邮件内容"""
        if not jobs:
            return "今天没有发现新的Web3工作机会。"
        
        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .job-item {{ border: 1px solid #ddd; margin: 20px 0; padding: 20px; border-radius: 5px; }}
                .job-title {{ color: #2196F3; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .job-company {{ color: #666; font-size: 16px; margin-bottom: 5px; }}
                .job-location {{ color: #888; margin-bottom: 10px; }}
                .job-salary {{ color: #4CAF50; font-weight: bold; margin-bottom: 10px; }}
                .job-description {{ margin: 15px 0; }}
                .job-tags {{ margin: 10px 0; }}
                .tag {{ background-color: #e1f5fe; color: #0277bd; padding: 3px 8px; margin: 2px; border-radius: 3px; font-size: 12px; }}
                .job-link {{ display: inline-block; background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }}
                .remote-badge {{ background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Web3工作日报</h1>
                <p>{datetime.now().strftime('%Y年%m月%d日')} - 发现 {len(jobs)} 个新工作机会</p>
            </div>
        """
        
        for job in jobs:
            # 处理薪资显示
            salary_info = ""
            if job.salary_min or job.salary_max:
                if job.salary_min and job.salary_max:
                    salary_info = f"💰 {job.salary_min:,.0f} - {job.salary_max:,.0f} {job.currency}"
                elif job.salary_min:
                    salary_info = f"💰 {job.salary_min:,.0f}+ {job.currency}"
                elif job.salary_max:
                    salary_info = f"💰 最高 {job.salary_max:,.0f} {job.currency}"
            
            # 处理标签
            tags_html = ""
            if job.tags:
                tags = job.tags.split(',')
                tags_html = "".join([f'<span class="tag">{tag.strip()}</span>' for tag in tags if tag.strip()])
            
            # 处理远程工作标识
            remote_badge = '<span class="remote-badge">🏠 远程工作</span>' if job.remote else ""
            
            # 使用中文标题和描述（如果有的话）
            title = job.title_zh if job.title_zh else job.title
            description = job.description_zh if job.description_zh else job.description
            
            # 截断描述
            if description and len(description) > 300:
                description = description[:300] + "..."
            
            html_content += f"""
            <div class="job-item">
                <div class="job-title">{title}</div>
                <div class="job-company">🏢 {job.company}</div>
                <div class="job-location">📍 {job.location} {remote_badge}</div>
                {f'<div class="job-salary">{salary_info}</div>' if salary_info else ''}
                <div class="job-description">{description}</div>
                {f'<div class="job-tags">{tags_html}</div>' if tags_html else ''}
                <div>
                    <a href="{job.url}" class="job-link" target="_blank">查看详情</a>
                    <small style="margin-left: 15px; color: #888;">来源: {job.source_website}</small>
                </div>
            </div>
            """
        
        html_content += """
            <div class="footer">
                <p>这是一个自动生成的Web3工作推送邮件</p>
                <p>如果您不想继续接收此邮件，请联系管理员</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_daily_job_report(self, jobs: List[Job]) -> bool:
        """发送每日工作报告"""
        subject = f"Web3工作日报 - {datetime.now().strftime('%Y年%m月%d日')} ({len(jobs)}个新机会)"
        body = self.format_job_email(jobs)
        
        return self.send_email(subject, body, is_html=True)
    
    def send_job_alert(self, job: Job, keywords: List[str]) -> bool:
        """发送工作提醒"""
        title = job.title_zh if job.title_zh else job.title
        subject = f"🔥 Web3工作提醒: {title} - {job.company}"
        
        body = self.format_job_email([job])
        
        return self.send_email(subject, body, is_html=True)
    
    def send_scraping_summary(self, total_scraped: int, new_jobs: int, errors: List[str]) -> bool:
        """发送抓取摘要"""
        subject = f"Web3工作抓取摘要 - {datetime.now().strftime('%Y-%m-%d')}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Web3工作抓取摘要</h2>
            <p><strong>抓取时间:</strong> {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p><strong>总共抓取:</strong> {total_scraped} 个工作</p>
            <p><strong>新增工作:</strong> {new_jobs} 个</p>
            
            {f'<h3>错误信息:</h3><ul>{"".join([f"<li>{error}</li>" for error in errors])}</ul>' if errors else '<p>✅ 抓取过程无错误</p>'}
        </body>
        </html>
        """
        
        return self.send_email(subject, body, is_html=True)