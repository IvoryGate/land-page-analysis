from flask import Flask, request, jsonify
from flask_cors import CORS
from core.crawler_engine import CrawlerEngine
from core import DBManager
from config import Config

app = Flask(__name__)
CORS(app)

# 全局初始化引擎和数据库管理
db = DBManager()
engine = CrawlerEngine()

@app.route('/api/crawl', methods=['POST'])
def add_crawl_task():
    data = request.json
    package = data.get('package')
    platform = data.get('platform')
    region = data.get('region', 'us').lower()
    lang = data.get('lang', 'en').lower()

    if not package or not platform:
        return jsonify({"error": "Missing package or platform"}), 400

    try:
        existing_id = db.check_task_valid(package, platform, region, lang)
        if existing_id:
            print(f"[*] 命中缓存: {existing_id}")
            images = db.get_task_images_list(existing_id)
            return jsonify({
                "status": "success",
                "task_id": existing_id,
                "images": images,
                "from_cache": True
            }), 200

        new_task_id = db.create_task(package, platform, region, lang)
        
        success, error_info = engine._task_handling(new_task_id, platform, package, region, lang)
        
        if success:
            images = db.get_task_images_list(new_task_id)
            return jsonify({
                "status": "success",
                "task_id": new_task_id,
                "images": images,
                "from_cache": False
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "error": error_info
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表（可视化分页预览）"""
    # 这里可以扩展从数据库查询最新的 20 条记录
    conn = db._get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks ORDER BY create_at DESC LIMIT 20")
            tasks = cursor.fetchall()
            return jsonify(tasks)
    finally:
        conn.close()

@app.route('/api/task/<int:task_id>/images', methods=['GET'])
def get_task_images(task_id):
    """获取某个任务抓取到的图片"""
    conn = db._get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Image_type, url FROM images WHERE task_id = %s", (task_id,))
            images = cursor.fetchall()
            return jsonify({"task_id": task_id, "images": images})
    finally:
        conn.close()