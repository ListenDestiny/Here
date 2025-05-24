#!/usr/bin/env python3
"""
Web3工作抓取器启动脚本
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

def main():
    """主函数"""
    # 获取配置
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "12000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("🚀 启动Web3工作抓取器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    print("=" * 50)
    
    # 启动应用
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        access_log=True,
        log_level="info" if debug else "warning"
    )

if __name__ == "__main__":
    main()