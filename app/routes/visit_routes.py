from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.visit_services import VisitService


visit_bp = Blueprint('visit_bp', __name__)
visit_service = VisitService()

@visit_bp.route('/recent-visits', methods=['POST'])
@jwt_required()
def create_recent_visit():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400

    result, status = visit_service.log_visit(user_id, product_id)
    return jsonify(result), status


@visit_bp.route('/recent-visits', methods=['GET'])
@jwt_required()
def get_recent_visits():
    user_id = get_jwt_identity()
    result, status = visit_service.get_recent_visits(user_id)
    return jsonify(result), status
