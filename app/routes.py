from flask import Blueprint, request, jsonify
from .models import db, User, Connection

bp = Blueprint('main', __name__)

@bp.route('/connect', methods=['POST'])
def connect_users():
    data = request.get_json()
    source_name = data.get('source')
    target_name = data.get('target')

    if not source_name or not target_name or source_name == target_name:
        return jsonify({'error': 'Invalid names'}), 400

    source = User.query.filter_by(username=source_name).first()
    if not source:
        source = User(username=source_name)
        db.session.add(source)

    target = User.query.filter_by(username=target_name).first()
    if not target:
        target = User(username=target_name)
        db.session.add(target)

    db.session.commit()

    existing = Connection.query.filter_by(source_id=source.id, target_id=target.id).first()
    if not existing:
        connection = Connection(source_id=source.id, target_id=target.id)
        db.session.add(connection)
        db.session.commit()

    return jsonify({'message': 'Connection added'}), 201

@bp.route('/disconnect', methods=['DELETE'])
def disconnect_users():
    data = request.get_json()
    source_name = data.get('source')
    target_name = data.get('target')

    if not source_name or not target_name:
        return jsonify({'error': 'Source and target names are required'}), 400

    source = User.query.filter_by(username=source_name).first()
    if not source:
        return jsonify({'error': 'Source user not found'}), 404

    target = User.query.filter_by(username=target_name).first()
    if not target:
        return jsonify({'error': 'Target user not found'}), 404

    # Находим и удаляем исходящее соединение
    connection = Connection.query.filter_by(source_id=source.id, target_id=target.id).first()
    if not connection:
        return jsonify({'error': 'Connection not found'}), 404

    db.session.delete(connection)
    db.session.commit()

    return jsonify({'message': 'Connection removed'}), 200

@bp.route('/user/<username>', methods=['GET'])
def get_user_connections(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 200

    outgoing = [conn.target_user.username for conn in user.outgoing]
    ingoing = [conn.source_user.username for conn in user.ingoing]

    return jsonify({
        'username': user.username,
        'outgoing': outgoing,
        'ingoing': ingoing
    })
    
@bp.route('/graph', methods=['GET'])
def get_full_graph():
    users = User.query.all()
    nodes = [{'id': user.username} for user in users]

    connections = Connection.query.all()
    links = [
        {
            'source': conn.source_user.username,
            'target': conn.target_user.username
        }
        for conn in connections
    ]

    return jsonify({
        'nodes': nodes,
        'links': links
    })
