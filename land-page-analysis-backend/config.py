import os
import random
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
    CRAWLER_MAX_WORKERS: int = int(os.getenv("CRAWLER_MAX_WORKERS"))
    CRAWLER_TIMEOUT: int = int(os.getenv("CRAWLER_TIMEOUT"))
    
    # HEADERS: dict | None = {
    #     'User-Agent': os.getenv('USER_AGENT')
    # }

    UA_POOL: list[str] = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        # Chrome on MacOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        # Safari on MacOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]

    # --- Google Play Url 配置 ---
    GOOGLE_URL: str = str(os.getenv("GOOGLE_URL"))

    # --- Apple Store Url 配置 ---
    APPLE_URL: str = str(os.getenv("APPLE_URL"))

    @classmethod
    def get_random_headers(cls) -> dict[str, str]:
        """每次调用返回一个带有随机 UA 的 Headers 字典"""
        return {
            'User-Agent': random.choice(cls.UA_POOL),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'
        }