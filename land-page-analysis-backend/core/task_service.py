from core.crawler_engine import CrawlerEngine
from core import DBManager


class TaskService:
    def __init__(self) -> None:
        self.db = DBManager()
        self.engine = CrawlerEngine()
        
    def get_single_record(self, package: str, platform: str, region: str, lang: str) -> tuple:
        existing_id = self.db.check_task_valid(package, platform, region, lang)
        if existing_id:
            return self.db.get_task_images_list(existing_id), existing_id
        task_id = self.db.create_task(package, platform, region, lang)
        try:
            self.db.update_task_status(task_id, 'running')
            processed_images = self.engine._task_handling(platform, package, region, lang)
            if processed_images:
                self.db.add_images(task_id, processed_images)
            self.db.update_task_status(task_id, 'success')
            return self.db.get_task_images_list(task_id), task_id
        except Exception as e:
            self.db.update_task_status(task_id, 'failed', error_log=str(e))
            raise e
        
    def get_all_localization(self):
        pass