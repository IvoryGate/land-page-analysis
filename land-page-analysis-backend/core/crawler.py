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

    def _task_handling(self, task_id: int, platform:str, package:str, region:str, lang:str):
        # time.sleep(random.uniform(1, 2))
        try:
            self.db.update_task_status(task_id=task_id, status='running')
            if platform == 'google_play':
                result = parse_google_play(package, region, lang)
            elif platform == 'app_store':
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
            
            self.db.update_task_status(task_id, 'success')
            print(f"[OK] 任务 {task_id}: {package} ({platform}) 抓取并存库成功")
            # print(f"成功抓取 [{platform}] {package}: 找到 {len(result['others'])} 张截图")
            return result

        except Exception as e:
            error_msg = str(e)
            self.db.update_task_status(task_id, 'failed', error_log=error_msg)
            print(f"[ERROR] 任务 {task_id}: {package} 失败，原因: {error_msg}")

    def add_job(self, platform: str, package: str, region: str, lang: str):
        """向线程池提交一个任务"""
        task_id = self.db.create_task(package, platform, region, lang)
        # 2. 异步执行
        self.executor.submit(self._task_handling, task_id, package, platform, region, lang)

    def wait_complete(self):
        """等待所有已提交的任务完成并关闭线程池"""
        self.executor.shutdown(wait=True)