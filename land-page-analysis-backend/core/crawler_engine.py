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
        self.db = DBManager()

    def _task_handling(self, task_id: int, platform: str, package: str, region: str, lang: str):
        try:
            self.db.update_task_status(task_id, 'running')

            if platform == 'google_play':
                result = parse_google_play(package, region, lang)
            elif platform == 'apple_store':
                result = parse_apple_store(package, region, lang)
            else:
                print(f"未知平台: {platform}")
                return
            image_records = []
            if result.get("icon"):
                image_records.append(('icon', result["icon"]))
            for img_url in result.get("others", []):
                image_records.append(('other', img_url))

            if image_records:
                self.db.add_images(task_id, image_records)

            # 4. 更新状态为成功
            self.db.update_task_status(task_id, 'success')
            print(f"[SUCCESS] 任务 {task_id} 完成: {package}")

        except Exception as e:
            error_msg = str(e)
            self.db.update_task_status(task_id, 'failed', error_log=error_msg)
            print(f"[ERROR] 任务 {task_id}: {package} 失败: {error_msg}")

    def add_job(self, platform: str, package: str, region: str, lang: str):
        existing_id = self.db.check_task_valid(package, platform, region, lang)
        if existing_id:
            print(f"[SKIP] {package} ({platform}) 在7天内已抓取成功 (ID: {existing_id})，跳过。")
            return
        print(platform)

        try:
            task_id = self.db.create_task(package, platform, region, lang)
            
            self.executor.submit(
                self._task_handling, 
                task_id,
                platform,
                package,
                region, 
                lang
            )
        except Exception as e:
            print(f"[SUBMIT ERROR] 无法创建任务记录: {e}")

    def wait_complete(self):
        self.executor.shutdown(wait=True)