import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # 数据库配置
    HOST: str | None = os.getenv("HOST")
    PORT: int | None = int(os.getenv("PORT"))
    USR: str | None = os.getenv("USR")
    PASSWORD: str | None = os.getenv("PASSWORD")
    DATABASE: str | None = os.getenv("DATABASE")
    CHARSET: str | None = os.getenv("CHARSET")

    # --- 爬虫配置信息 ---
    CRAWLER_MAX_WORKERS: int | None = int(os.getenv("CRAWLER_MAX_WORKERS"))
    CRAWLER_TIMEOUT: int | None = int(os.getenv("CRAWLER_TIMEOUT"))
    
    HEADERS: dict | None = {
        'User-Agent': os.getenv('USER_AGENT')
    }

    # --- Google Play Url 配置 ---
    GOOGLE_URL: str | None = os.getenv("GOOGLE_URL")

    # --- Apple Store Url 配置 ---
    APPLE_URL: str | None = os.getenv("APPLE_URL")