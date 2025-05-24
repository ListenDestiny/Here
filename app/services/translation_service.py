import os
from typing import Optional
import openai
import time
import random
import requests
import json

class TranslationService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def translate_with_openai(self, text: str, target_language: str = "Chinese") -> Optional[str]:
        """使用OpenAI API进行翻译"""
        if not self.openai_api_key or not text.strip():
            return None
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {target_language}. Keep the technical terms and maintain the professional tone. Only return the translated text without any additional comments."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI translation error: {e}")
            return None
    
    def translate_with_google_free(self, text: str, target_language: str = "zh") -> Optional[str]:
        """使用免费的Google翻译API进行翻译"""
        if not text.strip():
            return None
        
        try:
            # 添加随机延迟避免频率限制
            time.sleep(random.uniform(0.5, 1.5))
            
            # 使用免费的Google翻译API
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',
                'tl': target_language,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0 and len(result[0]) > 0:
                translated_text = ''.join([item[0] for item in result[0] if item[0]])
                return translated_text
            
            return None
            
        except Exception as e:
            print(f"Google translation error: {e}")
            return None
    
    def translate_text(self, text: str, target_language: str = "zh") -> str:
        """翻译文本，优先使用OpenAI，失败时使用Google Translate"""
        if not text or not text.strip():
            return ""
        
        # 首先尝试OpenAI翻译
        if self.openai_api_key:
            translated = self.translate_with_openai(text, "Chinese")
            if translated:
                return translated
        
        # 如果OpenAI失败，使用免费Google Translate
        translated = self.translate_with_google_free(text, target_language)
        return translated if translated else text
    
    def translate_job_fields(self, job_data: dict) -> dict:
        """翻译工作信息的各个字段"""
        translated_data = job_data.copy()
        
        # 翻译标题
        if job_data.get('title'):
            translated_data['title_zh'] = self.translate_text(job_data['title'])
        
        # 翻译描述
        if job_data.get('description'):
            # 如果描述太长，分段翻译
            description = job_data['description']
            if len(description) > 2000:
                # 分段翻译
                chunks = self.split_text(description, 2000)
                translated_chunks = []
                for chunk in chunks:
                    translated_chunk = self.translate_text(chunk)
                    translated_chunks.append(translated_chunk)
                    time.sleep(1)  # 避免频率限制
                translated_data['description_zh'] = '\n\n'.join(translated_chunks)
            else:
                translated_data['description_zh'] = self.translate_text(description)
        
        # 翻译要求
        if job_data.get('requirements'):
            requirements = job_data['requirements']
            if len(requirements) > 2000:
                chunks = self.split_text(requirements, 2000)
                translated_chunks = []
                for chunk in chunks:
                    translated_chunk = self.translate_text(chunk)
                    translated_chunks.append(translated_chunk)
                    time.sleep(1)
                translated_data['requirements_zh'] = '\n\n'.join(translated_chunks)
            else:
                translated_data['requirements_zh'] = self.translate_text(requirements)
        
        translated_data['is_translated'] = True
        return translated_data
    
    def split_text(self, text: str, max_length: int) -> list:
        """将长文本分割成较小的块"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence + '. ') <= max_length:
                current_chunk += sentence + '. '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks