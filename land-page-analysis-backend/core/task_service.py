from core.crawler_engine import CrawlerEngine
from core import DBManager


class TaskService:
    def __init__(self) -> None:
        self.db = DBManager()
        self.engine = CrawlerEngine()
        
    @classmethod
    def get_single_record(cls, package: str, platform: str, region: str, lang: str):
        pass