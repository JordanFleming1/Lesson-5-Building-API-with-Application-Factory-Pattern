from flask import request, jsonify
from . import inventory_bp
from ...models import Inventory
from ...extensions import db
from .schemas import inventory_schema, inventories_schema
from sqlalchemy import select

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.json
    new_item = Inventory(**data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    items = db.session.execute(select(Inventory)).scalars().all()
    return inventories_schema.jsonify(items)

@inventory_bp.route('/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return inventory_schema.jsonify(item)

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.json
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return inventory_schema.jsonify(item)

@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item {item_id} deleted'})
