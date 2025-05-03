from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.sale_product import SaleProduct
from models.product import Product
from models.sale import Sale

sale_product=Blueprint('sale_product',__name__)

@sale_product.route('/api/sale-products/get')
def get_sale_products():
    sale_products=SaleProduct.query.all()
    if not sale_products:
        return jsonify({'message':'There are no sale products registered'}),200
    return jsonify([sale_product.serialize() for sale_product in sale_products])

@sale_product.route('/api/sale-product/get/<int:id_sale_product>')
def get_sale_product(id_sale_product):
    sale_product=SaleProduct.query.get(id_sale_product)
    if not sale_product:
        return({'message':'Sale product not found'}),404
    return jsonify(sale_product.serialize()),200

@sale_product.route('/api/sale-product/add',methods=['POST'])
def add_sale_product():
    data=request.get_json()
    required_fields=['quantity','product_id','sale_id']
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400
    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400
    try:
        print(f"Data received: {data}")
        quantity = int(data['quantity'])
        product_id = int(data['product_id'])
        sale_id = int(data['sale_id'])
        product = Product.query.get(product_id)
        sale = Sale.query.get(sale_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404

        if product.stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400

        subtotal = quantity * product.current_price
        sould_price = product.current_price
        new_sale_product=SaleProduct(
            subtotal=subtotal, 
            quantity=quantity,
            sould_price=sould_price, 
            product_id=product_id,
            sale_id=sale_id
        )
        db.session.add(new_sale_product)
        product.stock= product.stock - quantity
        db.session.commit()
        return jsonify({
            'message': 'Sale product successfully created',
            'sale_product': new_sale_product.serialize()
        }),201
    except ValueError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data type. Ensure numeric fields are numbers.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding sale product'}), 500
    
@sale_product.route('/api/sale-product/delete/<int:id_sale_product>', methods=['DELETE'])
def delete_sale_product(id_sale_product):
    sale_product=SaleProduct.query.get(id_sale_product)
    if not sale_product:
        return jsonify({'message':'Sale product not found'}),404
    try:
        db.session.delete(sale_product)
        db.session.commit()
        return jsonify({'message':'Sale product delete successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
    
@sale_product.route('/api/sale-product/edit/<int:id_sale_product>', methods=['PUT'])
def edit_sale_product(id_sale_product):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    
    sale_product=SaleProduct.query.get(id_sale_product)

    if not sale_product:
        return jsonify({'message':'Sale product not found'}),404
    
    required_fields=['subtotal','quantity','sould_price','product_id','sale_id']
    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400
    try:
        if 'subtotal' in data:
            sale_product.subtotal = float(data['subtotal'])
        if 'quantity' in data:
            quantity = int(data['quantity'])
            if sale_product.quantity != quantity:
                product = Product.query.get(sale_product.product_id)
                if not product:
                    return jsonify({'error': 'Product not found'}), 400
                old_quantity = sale_product.quantity
                if quantity > old_quantity:
                    diff = quantity - old_quantity
                    if product.stock < diff:
                        return jsonify({'error': 'Insufficient stock'}), 400
                    product.stock -= diff
                elif quantity < old_quantity:
                    diff = old_quantity - quantity
                    product.stock += diff
                sale_product.quantity = quantity
        if 'sould_price' in data:
            sale_product.sould_price=float(data['sould_price'])
        if 'product_id' in data:
            product_id = int(data['product_id'])
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 400
            sale_product.product_id = product_id
        if 'sale_id' in data:
            sale_id = int(data['sale_id'])
            sale = Sale.query.get(sale_id)
            if not sale:
                return jsonify({'error': 'Sale not found'}), 400
            sale_product.sale_id = sale_id
        db.session.commit()
        return jsonify({'message': 'Sale product edit correctly', 'sale product': sale_product.serialize()}), 200
    except ValueError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data type. Ensure numeric fields are numbers.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@sale_product.route('/api/sale-product/update/<int:id_sale_product>', methods=['PATCH'])
def update_sale_product(id_sale_product):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    sale_product=SaleProduct.query.get(id_sale_product)
    if not sale_product:
        return jsonify({'message':'Sale product not found'}),404    
    try:
        if 'subtotal' in data:
            sale_product.subtotal = float(data['subtotal'])
        if 'quantity' in data:
            quantity = int(data['quantity'])
            if sale_product.quantity != quantity:
                product = Product.query.get(sale_product.product_id)
                if not product:
                    return jsonify({'error': 'Product not found'}), 400
                old_quantity = sale_product.quantity
                if quantity > old_quantity:
                    diff = quantity - old_quantity
                    if product.stock < diff:
                        return jsonify({'error': 'Insufficient stock'}), 400
                    product.stock -= diff
                elif quantity < old_quantity:
                    diff = old_quantity - quantity
                    product.stock += diff
                sale_product.quantity = quantity
        if 'sould_price' in data:
            sale_product.sould_price = float(data['sould_price'])
        if 'product_id' in data:
             product_id = int(data['product_id'])
             product = Product.query.get(product_id)
             if not product:
                return jsonify({'error': 'Product not found'}), 400
             sale_product.product_id = product_id
        if 'sale_id' in data:
            sale_id = int(data['sale_id'])
            sale = Sale.query.get(sale_id)
            if not sale:
                return jsonify({'error': 'Sale not found'}), 400
            sale_product.sale_id = sale_id
        db.session.commit()
        return jsonify({'message': 'Sale product update correctly', 'product': sale_product.serialize()}), 200
    except ValueError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data type. Ensure numeric fields are numbers.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}, 500)