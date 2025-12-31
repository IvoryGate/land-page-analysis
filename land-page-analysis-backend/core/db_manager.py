from config import Config
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
                        platform ENUM('google_play', 'app_store') NOT NULL,
                        region VARCHAR(10) NOT NULL,
                        language VARCHAR(10) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        erro_log TEXT,
                        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_pkg (package_name),
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