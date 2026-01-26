from config import Config
from typing import List, Tuple, Optional
import pymysql

class DBManager(object):
    def __init__(self) -> None:
        """
        加载数据库配置
        """
        self.config = {
            'host': Config.HOST,
            'port': Config.PORT,
            'user': Config.USR,
            'password': Config.PASSWORD,
            'database': Config.DATABASE,
            'charset': Config.CHARSET,
            'cursorclass': pymysql.cursors.DictCursor
        }
        self._init_tables()

    def _get_connection(self):
        return pymysql.connect(**self.config)
    
    def _init_tables(self):
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                existing_tables = {list(row.values())[0] for row in cursor.fetchall()}
                if 'tasks' not in existing_tables:
                    print("tasks表初始化...")
                    create_tasks_table = """
                        CREATE TABLE IF NOT EXISTS tasks (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        package_name VARCHAR(255) NOT NULL,
                        platform ENUM('google_play', 'apple_store') NOT NULL,
                        region VARCHAR(10) NOT NULL,
                        language VARCHAR(10) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        erro_log TEXT,
                        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_package (package_name),
                        INDEX idx_reg (region),
                        INDEX idx_lang (language)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                    """
                    cursor.execute(create_tasks_table)
                    print("tasks表创建完成")

                if 'images' not in existing_tables:
                    print("images表初始化...")
                    create_images_table = """
                    CREATE TABLE IF NOT EXISTS images (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        task_id INT NOT NULL,
                        Image_type ENUM('icon', 'other') NOT NULL,
                        url TEXT NOT NULL,
                        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                    """
                    cursor.execute(create_images_table)
                    print("images表创建完成")
                conn.commit()
        except Exception as e:
            print(f"初始化表失败: {e}")
            conn.rollback()
        finally:
            conn.close()

    def check_task_valid(self, package: str, platform: str, region: str, lang: str) -> Optional[int]:
        sql = """
            SELECT id FROM tasks 
            WHERE package_name=%s AND platform=%s AND region=%s AND language=%s 
            AND status='success' 
            AND update_at > DATE_SUB(NOW(), INTERVAL 7 DAY)
            LIMIT 1
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (package, platform, region, lang))
                result = cursor.fetchone()
                return result['id'] if result else None
        finally:
            conn.close()

    def create_task(self, package: str, platform: str, region: str, lang: str) -> int:
        clean_platform = platform.strip().lower()
        
        sql = """
            INSERT INTO tasks (package_name, platform, region, language, status) 
            VALUES (%s, %s, %s, %s, 'pending')
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (package, clean_platform, region, lang))
                conn.commit()
                task_id = cursor.lastrowid
                return task_id
        except Exception as e:
            conn.rollback()
            print(f"[DB ERROR] 创建任务失败: {e} | Params: {package}, {clean_platform}")
            raise e
        finally:
            conn.close()
            
    def update_task_status(self, task_id: int, status: str, error_log: str = ""):
        sql = "UPDATE tasks SET status=%s, erro_log=%s WHERE id=%s"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (status, error_log, task_id))
                conn.commit()
        finally:
            conn.close()

    def add_images(self, task_id: int, image_list: List[Tuple[str, str]]) -> None:
        if not image_list:
            return

        sql = "INSERT INTO images (task_id, Image_type, url) VALUES (%s, %s, %s)"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, [
                    (task_id, itype, url) for itype, url in image_list
                ])
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[DB ERROR] 批量写入图片失败 (TaskID: {task_id}): {e}")
            raise e
        finally:
            conn.close()
    
    def get_task_images_list(self, task_id: int) -> List[dict]:
        """专门为 API 提供的图片获取方法"""
        sql = "SELECT Image_type as type, url FROM images WHERE task_id = %s"
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (task_id,))
                return cursor.fetchall() # 返回 [{'type': 'icon', 'url': '...'}, ...]
        finally:
            conn.close()