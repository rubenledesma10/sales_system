from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.sale import Sale
from models.sale_product import SaleProduct
from models.client import Client #We need to associate the customer model with the sale
from datetime import datetime  # Importe  'date' para el manejo de fechas 
from models.product import Product

sale_bp = Blueprint('sale', __name__)

@sale_bp.route('/api/sales')#Get all sales
def get_sales():
    sales = Sale.query.all()
    if not sales:
        return jsonify({'message': 'There are no sales registered'}), 404
    return jsonify([sale.serialize() for sale in sales])

@sale_bp.route('/api/sales/<int:sale_id>', methods=['GET'])
def get_sale_id(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'message': 'There are no sale registered'}), 404
    return jsonify(sale.serialize())

@sale_bp.route('/api/clients/<int:client_id>/sales', methods=['GET']) #We access ALL of a customer's sales through their ID
def get_client_sales(client_id):
    client = Client.query.get_or_404(client_id)
    sales = Sale.query.filter_by(id_client=client_id).all()
    return jsonify([sale.serialize() for sale in sales])

@sale_bp.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.get_json()

    try:
        id_client = data.get('id_client')
        client = Client.query.get(id_client)
        if not client:
            return jsonify({'message': 'Client not found'}), 404

        sale_date_str = data.get('sale_date')
        sale_date = None

        if sale_date_str:
            try:
                sale_date = datetime.strptime(sale_date_str, '%d-%m-%Y').date()
            except ValueError:
                return jsonify({'message': 'Incorrect date format. Must be dd-mm-yyyy'}), 400

        discount = data.get('discount', 0.0)

        new_sale = Sale(
            sale_date=sale_date,
            discount=discount,
            id_client=id_client
        )

        db.session.add(new_sale)
        db.session.flush()  

        sale_id = new_sale.id_sale
        sale_products_data = data.get('sale_products', [])

        if not isinstance(sale_products_data, list):
            db.session.rollback()
            return jsonify({'message': 'sale_products must be a list'}), 400

        total_amount = 0

        for product_data in sale_products_data:
            quantity = product_data.get('quantity')
            product_id = product_data.get('product_id')

            if not quantity or not product_id:
                db.session.rollback()
                return jsonify({'message': 'Quantity and product_id are required for each sale_product'}), 400

            try:
                quantity = int(quantity)
                product_id = int(product_id)
            except ValueError:
                db.session.rollback()
                return jsonify({'error': 'Quantity must be a number'}), 400

            product = Product.query.get(product_id)
            if not product:
                db.session.rollback()
                return jsonify({'error': f'Product with id {product_id} not found'}), 404

            if product.stock < quantity:
                db.session.rollback()
                return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400

            subtotal = quantity * product.current_price

        

            sould_price = subtotal / quantity

            new_sale_product = SaleProduct(
                subtotal=subtotal,
                quantity=quantity,
                sould_price=sould_price,
                product_id=product_id,
                sale_id=sale_id
            )

            db.session.add(new_sale_product)
            product.stock -= quantity
            total_amount += subtotal  

       
        if discount > 0:
            final_amount = total_amount - (total_amount * discount / 100)
        else:
            final_amount = total_amount

        new_sale.final_amount = final_amount

        db.session.commit()

        return jsonify({
            'message': 'Sale and sale products created successfully',
            'sale_id': sale_id,
            'final_amount': final_amount
        }), 201

    except ValueError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data type. Ensure numeric fields are numbers.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': f'Error creating sale: {str(e)}'}), 500
@sale_bp.route('/api/sales/<int:id_sale>', methods = ['DELETE'])

def delete_sale(id_sale):
    sale = Sale.query.get(id_sale)
    if not sale:
        return jsonify({'message': 'sale not found'}), 404
    
    try: 
        db.session.delete(sale)
        db.session.commit()
        return jsonify ({'message': 'sale delete successfully'}), 200
    
    except Exception as e: 
        db.session.rollback()
        return jsonify ({'error': str(e)})

@sale_bp.route('/api/sales/<int:sale_id>', methods=['PATCH'])
def update_sale(sale_id):
    data = request.get_json()
    sale = Sale.query.get(sale_id)
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'message': 'Sale not found'}), 404
    try:
        if 'final_amount' in data:
            #You add the final sale to the sale that is being made
            sale.final_amount = data['final_amount']

        if 'sale_date' in data:
            sale_date_str = data['sale_date']
            try:
                sale.sale_date = datetime.strptime(sale_date_str, '%d-%m-%Y').date()
                # Updates the sale date to the date of the last "sale after sale"
            except ValueError:
                return jsonify({'message': 'Incorrect date format for sale_date. Must be ddmmyyyy'}), 400

        db.session.commit()
        return jsonify({'message': 'Sale updated successfully', 'sale_id': sale.id_sale}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating sale: {str(e)}'}), 500

@sale_bp.route('/api/sales/<int:sale_id>', methods=['PUT'])
def update_sale_put(sale_id):

    data = request.get_json()
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'message': 'sale not found'}), 404
    
    try:
        id_client = data.get('id_client')
        sale_date_str = data.get('sale_date')
        discount = data.get('discount')
        final_amount = data.get('final_amount')

        # Validation of required fields
        if not id_client or not sale_date_str or discount is None or final_amount is None:
            return jsonify({'message': 'Missing required fields for sale update'}), 400

        client = Client.query.get_or_404(id_client)

        try:
            sale_date = datetime.strptime(sale_date_str, '%d-%m-%Y').date()
        except ValueError:
            return jsonify({'message': 'Incorrect date format for sale_date. Must be ddmmyyyy'}), 400

        db.session.commit()
        return jsonify({'message': 'Sale updated successfully ', 'sale_id': sale.id_sale}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating sale (PUT): {str(e)}'}), 500