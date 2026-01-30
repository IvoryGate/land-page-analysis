from concurrent.futures import as_completed
from core import CrawlerEngine
from core import DBManager
from config import Config
import pycountry

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
            return ({},task_id)

    def get_all_localization(self, package: str, platform: str):
        yield_list = []
        for country in pycountry.countries:
            region_code = country.alpha_2
            native_lang = Config.COUNTRY_LANG_MAP.get(region_code, 'en')
            task = self.engine.executor.submit(self.get_single_record, package, platform, region_code, native_lang)
            yield_list.append(task)
        
        for task in as_completed(yield_list):
            yield task.result()