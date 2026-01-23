import time
from core import CrawlerEngine

def main():

    engine = CrawlerEngine(max_workers=3)
    
    # 准备测试数据 (包名, 平台, 国家, 语言)
    test_tasks = [
        ("com.facebook.orca", "google_play", "us", "en"),
        ("6745133405", "apple_store", "us", "en"),
        ("com.instagram.android", "google_play", "us", "en"),
        ("6739490118", "apple_store", "us", "en")
    ]

    print(f"--- 开始分发 {len(test_tasks)} 个爬取任务 ---")

    for package, platform, region, lang in test_tasks:
        try:
            task_id = engine.add_job(platform, package, region, lang)
            print(f"[SUBMIT] 任务已提交: ID={task_id}, package={package}")
        except Exception as e:
            print(f"[SUBMIT ERROR] 提交 {package} 失败: {e}")

if __name__ == "__main__":
    main()