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

    def _task_handling(self, platform:str, package:str, region:str, lang:str):
        # time.sleep(random.uniform(1, 2))
        try:
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

            for itype, img_url in image_records:
                print(itype,img_url)
            # print(f"成功抓取 [{platform}] {package}: 找到 {len(result['others'])} 张截图")
            return result

        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] 任务 / : {package} 失败，原因: {error_msg}")

    def add_job(self, platform: str, package: str, region: str, lang: str):
        """向线程池提交一个任务"""
        self.executor.submit(self._task_handling, package, platform, region, lang)

    def wait_complete(self):
        """等待所有已提交的任务完成并关闭线程池"""
        self.executor.shutdown(wait=True)