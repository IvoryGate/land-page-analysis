import time
from core import CrawlerEngine

def main():
    # 1. 初始化爬虫引擎 (并发数设为 3，方便观察)
    engine = CrawlerEngine(max_workers=3)
    
    # 2. 准备测试数据 (包名, 平台, 国家, 语言)
    # 这里的包名建议使用你提供的 apple_html.txt 和 google_html.txt 对应的 ID 
    test_tasks = [
        ("com.facebook.orca", "google_play", "us", "en"),
        ("6745133405", "apple_store", "us", "en"),
        ("com.instagram.android", "google_play", "us", "en"),
        ("6739490118", "apple_store", "us", "en")
    ]

    print(f"--- 开始分发 {len(test_tasks)} 个爬取任务 ---")

    for package, platform, region, lang in test_tasks:
        try:
            task_id = engine.add_job(package, platform, region, lang)
            print(f"[SUBMIT] 任务已提交: ID={task_id}, package={package}")
        except Exception as e:
            print(f"[SUBMIT ERROR] 提交 {package} 失败: {e}")

if __name__ == "__main__":
    main()