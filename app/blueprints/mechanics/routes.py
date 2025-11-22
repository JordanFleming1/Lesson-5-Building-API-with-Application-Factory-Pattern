from flask import request, jsonify
from . import mechanics_bp
from ...models import Mechanic
from ...schemas import mechanic_schema, mechanics_schema
from ...extensions import db, cache, limiter
from sqlalchemy import select
from marshmallow import ValidationError

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/', methods=['GET'])
@limiter.limit('10 per minute')
@cache.cached(timeout=60)
def get_mechanics():
    limit = request.args.get('limit', default=10, type=int)
    query = select(Mechanic).limit(limit)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found.'}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found.'}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': f'Mechanic id: {id}, successfully deleted.'}), 200

@mechanics_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    from ...models import Mechanic
    from ...extensions import db
    from sqlalchemy import select
    mechanics = db.session.execute(select(Mechanic)).scalars().all()
    # Assume Mechanic has a .service_tickets relationship
    mechanics_sorted = sorted(mechanics, key=lambda m: len(getattr(m, 'service_tickets', [])), reverse=True)
    limit = request.args.get('limit', default=10, type=int)
    return jsonify([
        {'id': m.id, 'name': getattr(m, 'name', None), 'ticket_count': len(getattr(m, 'service_tickets', []))}
        for m in mechanics_sorted[:limit]
    ])
