import time
import random
from config import Config
from core import DBManager
from concurrent.futures import ThreadPoolExecutor
from core import parse_google_play,parse_apple_store

class CrawlerEngine:
    def __init__(self, max_workers: int = 0) -> None:
        workers = max_workers or Config.CRAWLER_MAX_WORKERS
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def _task_handling(self, platform: str, package: str, region: str, lang: str):
        if platform == 'google_play':
            raw_data = parse_google_play(package, region, lang)
        elif platform == 'apple_store':
            raw_data = parse_apple_store(package, region, lang)
        else:
            raise ValueError(f"unknow platform: {platform}")
        return self._format_data(raw_data=raw_data)
    
    def _format_data(self, raw_data):
        processed_images = []
        icon_url = raw_data.get("icon")
        if icon_url:
            processed_images.append(('icon', icon_url))
        others = raw_data.get("others", [])
        for url in others:
            processed_images.append(('other', url))  
        return processed_images

    # def add_job(self, platform: str, package: str, region: str, lang: str):
    #     existing_id = self.db.check_task_valid(package, platform, region, lang)
    #     if existing_id:
    #         print(f"[SKIP] {package} ({platform}) 在7天内已抓取成功 (ID: {existing_id})，跳过。")
    #         return
    #     try:
    #         task_id = self.db.create_task(package, platform, region, lang)
            
    #         self.executor.submit(self._task_handling, task_id, platform, package, region, lang)
    #     except Exception as e:
    #         print(f"[SUBMIT ERROR] 无法创建任务记录: {e}")

    def wait_complete(self):
        self.executor.shutdown(wait=True)