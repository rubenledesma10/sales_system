from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.supplier import Supplier

supplier_bp = Blueprint('supplier', __name__)


@supplier_bp.route('/api/supplier', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    if not suppliers:
        return jsonify({'message': 'No suppliers have been registered'}), 200
    return jsonify([s.serialize() for s in suppliers]), 200


@supplier_bp.route('/api/get_supplier/<int:id>', methods=['GET'])
def get_supplier_by_id(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    return jsonify(supplier.serialize()), 200


@supplier_bp.route('/api/add_supplier', methods=['POST'])
def add_supplier():
    data = request.get_json()
    required = ['name', 'address', 'phone', 'web_page', 'rut']

    if not data or not all(key in data for key in required):
        return jsonify({'error': 'Missing data entry'}), 400

    for field in required:
        if not str(data.get(field, '')).strip():
            return jsonify({'error': f'{field.upper()} cannot be empty'}), 400

    try:
        print(f'Data received: {data}')
        new_supplier = Supplier(
            data['name'],
            data['address'],
            data['phone'],
            data['web_page'],
            data['rut']
        )

        db.session.add(new_supplier)
        db.session.commit()

        return jsonify({
            'message': 'Supplier successfully created',
            'supplier': new_supplier.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()

        if 'phone' in error_msg:
            return jsonify({'error': 'The phone number is already registered'}), 400
        elif 'rut' in error_msg:
            return jsonify({'error': 'The RUT is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e:
        db.session.rollback()
        print(f'Unexpected error: {e}')
        return jsonify({'error': 'Error adding supplier'}), 500


@supplier_bp.route('/api/delete_supplier/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@supplier_bp.route('/api/edit_supplier/<int:id>', methods=['PUT'])
def edit_supplier(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    required = ['name', 'address', 'phone', 'web_page', 'rut']
    for field in required:
        if not str(data.get(field, '')).strip():
            return jsonify({'error': f'{field.upper()} cannot be empty'}), 400

    try:
        supplier.name = data['name']
        supplier.address = data['address']
        supplier.phone = data['phone']
        supplier.web_page = data['web_page']
        supplier.rut = data['rut']

        db.session.commit()
        return jsonify({'message': 'Supplier updated successfully', 'supplier': supplier.serialize()}), 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()

        if 'phone' in error_msg:
            return jsonify({'error': 'The phone number is already registered'}), 400
        elif 'rut' in error_msg:
            return jsonify({'error': 'The RUT is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@supplier_bp.route('/api/update_supplier/<int:id>', methods=['PATCH'])
def update_supplier(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    try:
        if 'name' in data:
            supplier.name = data['name']
        if 'address' in data:
            supplier.address = data['address']
        if 'phone' in data:
            supplier.phone = data['phone']
        if 'web_page' in data:
            supplier.web_page = data['web_page']
        if 'rut' in data:
            supplier.rut = data['rut']

        db.session.commit()
        return jsonify({'message': 'Supplier updated successfully', 'supplier': supplier.serialize()}), 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()

        if 'phone' in error_msg:
            return jsonify({'error': 'The phone number is already registered'}), 400
        elif 'rut' in error_msg:
            return jsonify({'error': 'The RUT is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
