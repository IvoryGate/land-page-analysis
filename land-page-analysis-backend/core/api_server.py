"""
# api_server.py

这个文件用来管理路由，编辑返回信息，只做简单的数据验证，其他的逻辑全部交给`task_service.py`

"""
from flask import Blueprint, request, jsonify, Response, stream_with_context
from core.task_service import TaskService
import json

api_bp = Blueprint('api', __name__)

task_service = TaskService()

@api_bp.route('/test', methods=['POST'])
def crawl_test():
    package = request.json.get('package')
    platform = request.json.get('platform')
    region = request.json.get('region', 'us').lower()
    lang = request.json.get('lang', 'en').lower()
    return jsonify({
        "status" : "success",
        "package": package,
        "platform": platform,
        "region": region,
        "lang": lang,
        "message": f"receive successfully"
    })

@api_bp.route('/get', methods=['POST'])
def get_image_urls():
    package = request.json.get('package')
    platform = request.json.get('platform')
    region = request.json.get('region', 'us').lower()
    lang = request.json.get('lang', 'en').lower()
    if not package or not platform:
        return jsonify({"error": "Missing params"}), 400
    images,task_id,region = task_service.get_single_record(package, platform, region, lang)
    return jsonify({
        "status": "success",
        "task_id": task_id,
        "images": images,
        "region": region
    }), 200

@api_bp.route('/compare', methods=['POST'])
def fetch_all_localization():
    package = request.json.get('package')
    platform = request.json.get('platform')
    if not package or not platform:
        return jsonify({"error": "Missing params"}), 400
    def generate():
        stream = task_service.get_all_localization(package, platform)
        for images,task_id,region in stream:
            yield json.dumps({
                "status": "success",
                "task_id": task_id,
                "images": images,
                "region": region
            }) + "\n"

    return Response(
        stream_with_context(generate()), 
        mimetype='application/x-ndjson'
    )