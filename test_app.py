#!/usr/bin/env python3
"""
简单的测试启动脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.database import create_tables
import uvicorn

if __name__ == "__main__":
    # 创建数据库表
    create_tables()
    
    # 启动应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=12000,
        reload=False
    )