from flask import request, jsonify
from . import service_tickets_bp
from ...models import ServiceTicket, Mechanic, Inventory
from ...schemas import service_ticket_schema, service_tickets_schema
from ...extensions import db, cache
from sqlalchemy import select
from marshmallow import ValidationError

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({'error': 'Ticket or Mechanic not found.'}), 404
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({'error': 'Ticket or Mechanic not found.'}), 404
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_mechanics_on_ticket(ticket_id):
    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    # Add mechanics
    for mid in add_ids:
        mechanic = db.session.get(Mechanic, mid)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
    # Remove mechanics
    for mid in remove_ids:
        mechanic = db.session.get(Mechanic, mid)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({'mechanics': [m.id for m in ticket.mechanics]})

@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)
    if not ticket or not part:
        return jsonify({'error': 'Ticket or Part not found'}), 404
    if part not in ticket.inventory_items:
        ticket.inventory_items.append(part)
        db.session.commit()
    return jsonify({'message': 'Part added to ticket', 'parts': [p.id for p in ticket.inventory_items]})

@service_tickets_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_service_tickets():
    limit = request.args.get('limit', default=10, type=int)
    query = select(ServiceTicket).limit(limit)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)
