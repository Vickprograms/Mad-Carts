from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_history_service import SearchHistoryService
from app.db import get_db_connection

search_history_bp = Blueprint('search_history', __name__)
conn = get_db_connection()
search_service = SearchHistoryService(conn)


@search_history_bp.route('/search-history', methods=['POST'])
@jwt_required()
def create_search():
    data = request.get_json()
    user_id = get_jwt_identity()
    search_term = data.get('search_term')

    if not search_term:
        return jsonify({'error': 'search_term is required'}), 400

    response, status = search_service.create_search_history(user_id, search_term)
    return jsonify(response), status


@search_history_bp.route('/search-history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    response, status = search_service.get_search_history(user_id)
    return jsonify(response), status



@search_history_bp.route('/search-history/<id>', methods=['DELETE'])
@jwt_required()
def delete_history(id):
    user_id = get_jwt_identity()

   
    if not search_service.owned_by_user(id, user_id):
        return jsonify({'error': 'Unauthorized access'}), 403

    response, status = search_service.delete_history(id)
    return jsonify(response), status
