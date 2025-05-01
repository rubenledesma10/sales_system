from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.sale import Sale
from models.sale_product import SaleProduct
from models.client import Client #We need to associate the customer model with the sale
from datetime import datetime, date  # Importa también 'date' si lo usas en tus modelos

sale_bp = Blueprint('sale', __name__)

@sale_bp.route('/api/sales')#Traemos todas las ventas
def get_sales():
    sales = Sale.query.all()
    if not sales:
        return jsonify({'message': 'There are no sales registered'}), 404
    return jsonify([sale.serialize() for sale in sales])

@sale_bp.route('/api/sales/<int:sale_id>', methods=['GET'])
def get_sale_id(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    return jsonify(sale.serialize())

@sale_bp.route('/api/clients/<int:client_id>/sales', methods=['GET']) #We access ALL of a customer's sales through their ID
def get_client_sales(client_id):
    client = Client.query.get_or_404(client_id)
    sales = Sale.query.filter_by(id_client=client_id).all()
    return jsonify([sale.serialize() for sale in sales])

@sale_bp.route('/api/add_sale', methods=['POST'])
def create_sale():
    data = request.get_json()

    try:
        id_client = data.get('id_client')
        client = Client.query.get_or_404(id_client)
        if not client:
            return jsonify({'message': 'Client not found'}), 404

        sale_date_str = data.get('sale_date')
        sale_date = None

        if sale_date_str:
            try:
                sale_date = datetime.strptime(sale_date_str, '%d%m%Y').date()
            except ValueError:
                return jsonify({'message': 'Incorrect date format. Must be ddmmyyyy'}), 400

        new_sale = Sale(
            sale_date=sale_date,
            discount=data.get('discount', 0.0),
            final_amount=data.get('final_amount'),
            id_client=id_client
        )

        db.session.add(new_sale)
        db.session.flush()
        db.session.commit()

        return jsonify({'message': 'Sale created successfully', 'sale_id': new_sale.id_sale}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error de integridad en la base de datos'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear la venta: {str(e)}'}), 500