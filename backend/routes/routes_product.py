from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.product import Product
from models.supplier import Supplier
from models.category import Category

product = Blueprint('product',__name__)

@product.route('/api/products/get')
def get_all_products():
    product=Product.query.all()
    if not product:
        return jsonify({'message':'There are no products registered'}),200
    return jsonify([products.serialize() for products in product])

@product.route('/api/product/get/<int:id_product>')
def get_product(id_product):
    product=Product.query.get(id_product)
    if not product:
        return jsonify({'message':'Product not found'}),404
    return jsonify(product.serialize()),200

@product.route('/api/product/add',methods=['POST'])
def add_product():
    data=request.get_json()
    required_fields=['name','current_price','stock','supplier_id','category_id']
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400
    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400
    try:
        print(f"Data received: {data}")
        new_product=Product(
            data['name'],
            data['current_price'],
            data['stock'],
            data['supplier_id'],
            data['category_id']
        )

        db.session.add(new_product)
        db.session.commit
        return jsonify({
            'message': 'Product successfully created',
            'product': new_product.serialize()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding mechanic'}), 500
    
@product.route('/api/product/delete/<int:id_product>',methods=['DELETE'])
def delete_product(id_product):
    product=Product.query.get(id_product)
    if not product:
        return jsonify({'message':'Product not found'}),404
    try:
        db.session.delete(product)
        db.session.commit
        return jsonify({'message':'Product delete successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
    
@product.route('/api/product/edit/<int:id_product>',methods=['PUT'])
def edit_product(id_product):   

    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    
    product=Product.query.get(id_product)
    if not product:
        return jsonify({'message':'Product not found'}), 404
    
    required_fields=['name','current_price','stock','supplier_id','category_id']
    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400
    try:
        if 'name' in data:
            product.name=data['name']
        if 'current_price' in data:
            product.current_price=data['current_price']
        if 'stock' in data:
            product.stock=data['stock']
        if 'supplier_id' in data:
            product.supplier_id=data['supplier_id']
        if 'category_id' in data:
            product.category_id=data['category_id']
        db.session.commit()
        return jsonify({'message':'Product edit correctly','product':product.serialize()}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@product.route('/api/product/update/<int:id_product>',methods=['PATCH'])
def update_product(id_product):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    product = Product.query.get(id)
    if not product:
        return jsonify({'message':'Product not found'}),404
    try:
        if 'name' in data:
            product.name=data['name']
        if 'current_price' in data:
            product.current_price=data['current_price']
        if 'stock' in data:
            product.stock=data['stock']
        if 'supplier_id' in data:
            product.supplier_id=data['supplier_id']
        if 'category_id' in data:
            product.category_id=data['category_id']
        db.session.commit()
        return jsonify({'message':'Product update correctly','product':product.serialize()}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


