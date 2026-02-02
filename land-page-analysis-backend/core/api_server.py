from flask import Blueprint, request, jsonify, Response, stream_with_context
from core.task_service import TaskService
from flask_cors import CORS
import json

api_bp = Blueprint('api', __name__)
CORS(api_bp)
task_service = TaskService()

@api_bp.route('/history', methods=['GET'])
def get_history():
    return jsonify(task_service.get_search_history()), 200

@api_bp.route('/history', methods=['POST'])
def update_history():
    package = request.json.get('package')
    if not package:
        return jsonify({"error": "Missing package"}), 400
    new_history = task_service.add_search_history(package)
    return jsonify(new_history), 200

@api_bp.route('/get', methods=['POST'])
def get_image_urls():
    package = request.json.get('package')
    platform = request.json.get('platform')
    region = request.json.get('region', 'us').lower()
    lang = request.json.get('lang', 'en').lower()
    if not package or not platform:
        return jsonify({"error": "Missing params"}), 400
    images, task_id, region = task_service.get_single_record(package, platform, region, lang)
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
        for images, task_id, region in stream:
            yield json.dumps({
                "status": "success",
                "task_id": task_id,
                "images": images,
                "region": region
            }) + "\n"
    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')