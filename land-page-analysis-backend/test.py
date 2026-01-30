import time
from core import TaskService

if __name__ == "__main__":
    task_service = TaskService()
    test_package = "com.vitastudio.mahjong"
    # test_package = "water.sort.color.puzzle.offline.games"
    test_platform = "google_play"
    try:
        stream = task_service.get_all_localization(test_package, test_platform)
        start_time = time.time()
        count = 0
        for result in stream:
            count += 1
            elapsed = time.time() - start_time   
            images, task_id = result    
            print(f"[{elapsed:.2f}s] 第 {count} 个结果返回 | TaskID: {task_id} | 图片数: {len(images)}")
            if images:
                print(f"   -> 样例图片: {images[1].get('url', 'No URL')}")          
    except KeyboardInterrupt:
        print("\n[!] 停止测试")
    except Exception as e:
        print(f"\n[!!!] 发生异常: {e}")
        
    print("\n>>> 测试结束")