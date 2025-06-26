from flask import Blueprint, request, jsonify
from app.services.search_history_service import SearchHistoryService
from app.db import get_db_connection

search_history_bp = Blueprint('search_history', __name__)
conn = get_db_connection()
search_service = SearchHistoryService(conn)

@search_history_bp.route('/search-history', methods=['POST'])
def create_search():
    data = request.get_json()
    user_id = data.get('user_id')
    search_term = data.get('search_term')

    if not user_id or not search_term:
        return jsonify({'error': 'user_id and search_term are required'}), 400

    response, status = search_service.create_search_history(user_id, search_term)
    return jsonify(response), status


@search_history_bp.route('/search-history/<user_id>', methods=['GET'])
def get_history(user_id):
    response, status = search_service.get_search_history(user_id)
    return jsonify(response), status


@search_history_bp.route('/search-history/<id>', methods=['DELETE'])
def delete_history(id):
    response, status = search_service.delete_history(id)
    return jsonify(response), status
