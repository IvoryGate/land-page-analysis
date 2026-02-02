import os
import json
import pycountry
from concurrent.futures import as_completed
from core import CrawlerEngine, DBManager
from config import Config

class TaskService:
    def __init__(self) -> None:
        self.db = DBManager()
        self.engine = CrawlerEngine()
        self.history_file = 'search_history.json'
        
    def get_search_history(self) -> list:
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def add_search_history(self, package: str) -> list:
        history = self.get_search_history()
        if package in history:
            history.remove(package)
        history.insert(0, package)
        history = history[:10]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
        return history

    def get_single_record(self, package: str, platform: str, region: str, lang: str) -> tuple:
        existing_id = self.db.check_task_valid(package, platform, region, lang)
        if existing_id:
            return self.db.get_task_images_list(existing_id), existing_id, region
        
        task_id = self.db.create_task(package, platform, region, lang)
        try:
            self.db.update_task_status(task_id, 'running')
            processed_images = self.engine._task_handling(platform, package, region, lang)
            if processed_images:
                self.db.add_images(task_id, processed_images)
            self.db.update_task_status(task_id, 'success')
            return self.db.get_task_images_list(task_id), task_id, region
        except Exception as e:
            self.db.update_task_status(task_id, 'failed', error_log=str(e))
            return ([], task_id, region)

    def get_all_localization(self, package: str, platform: str):
        yield_list = []
        for country in pycountry.countries:
            region_code = country.alpha_2
            native_lang = Config.COUNTRY_LANG_MAP.get(region_code, 'en')
            task = self.engine.executor.submit(self.get_single_record, package, platform, region_code, native_lang)
            yield_list.append(task)
        
        for task in as_completed(yield_list):
            yield task.result()