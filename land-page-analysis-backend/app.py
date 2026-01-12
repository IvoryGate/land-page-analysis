import time
from core import CrawlerEngine

def main():
    # 1. 初始化爬虫引擎 (并发数设为 3，方便观察)
    engine = CrawlerEngine(max_workers=3)
    
    # 2. 准备测试数据 (包名, 平台, 国家, 语言)
    # 这里的包名建议使用你提供的 apple_html.txt 和 google_html.txt 对应的 ID 
    test_tasks = [
        ("com.facebook.orca", "google_play", "us", "en"),       # Google Play: Messenger
        ("1458316307", "app_store", "us", "en"),              # Apple Store: Ball Sort (对应你的参考文件)
        ("com.instagram.android", "google_play", "us", "en"),  # Google Play: Instagram
        ("284800453", "app_store", "us", "en")                 # Apple Store: Candy Crush
    ]

    print(f"--- 开始分发 {len(test_tasks)} 个爬取任务 ---")

    # 3. 分发任务 (add_job 内部会先写数据库 tasks 表获取 ID)
    for package, platform, region, lang in test_tasks:
        try:
            task_id = engine.add_job(package, platform, region, lang)
            print(f"[SUBMIT] 任务已提交: ID={task_id}, package={package}")
        except Exception as e:
            print(f"[SUBMIT ERROR] 提交 {package} 失败: {e}")

    print("\n--- 任务分发完毕，等待后台线程池执行 (约15秒) ---")

    # 4. 等待所有后台任务完成并关闭线程池
    # wait_complete 会阻塞直到所有线程运行结束
    engine.wait_complete()

    print("\n--- 所有爬取任务执行结束，请检查数据库 ---")
    print("SQL 参考:")
    print("SELECT * FROM tasks;")
    print("SELECT * FROM images;")

if __name__ == "__main__":
    main()