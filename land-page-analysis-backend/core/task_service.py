from core.crawler_engine import CrawlerEngine
from core import DBManager


class TaskService:
    def __init__(self) -> None:
        self.db = DBManager()
        self.engine = CrawlerEngine()
        
    def get_single_record(self, package: str, platform: str, region: str, lang: str) -> tuple:
        
        images = []
        task_id = 0
        return (images, task_id)