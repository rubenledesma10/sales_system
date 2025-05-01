from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.phone import Phone
from models.client import Client

client = Blueprint('client', __name__)


@client.route('api/clients') #Get all clients
def get_clients():
    client = Client.query.all()
    if not client:
        return jsonify ({'message: There are no clients registred'}), 200 
    return jsonify ([clients.serialize() for clients in client])

@client.route('api/get_clients/<int:id_client>') #We access a client through their ID.
def get_client_id(id):
    client = Client.query.get_or_404(id)
    if not client:
        return jsonify({'message: Client not found'}), 404 
    return jsonify (client.serialize()), 200

# @client.route('api/clients/<int:id_client>/phones', methods = 'GET') #We access the customer's phone number(s) through their ID
# def get_client_phones (id_client):
#     phone = phone.query.filter_by(id_client=id_client).all()
#     return jsonify([phone.serialize] for phone in phone) 

@client.route('/api/add_client', methods = 'POST')
def add_client():
    data = request.json()
    
    required_fields = ['name','rut','street_address','district_address','number_address','city_address','sale','phone']
    if not data or not all (key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400
    for field in required_fields:
        if not str(data.get(field,'')).strip():
            return jsonify({'error:':f'{field.title()}is required and cannot be empty'}), 400
    
    try:
        print(f"Date received: {data}")
        
        new_client = Client(
            data['name'],
            data['rut'],
            data['street_address'],
            data['district_address'],
            data['number_address'],
            data['city_address'],
            data['sale'],
            data['phone']
        )
        
        db.session.add(new_client)
        db.session.commit()
        return jsonify({
            'message': 'Client successfully created',
            'client': new_client.serialize()
        }), 201 
        
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        
        if 'rut' in error_msg:
            return jsonify({'error': 'The rut number is already registred'}), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify ({'error': 'Error adding client'}), 500 

@client.route('/api/delete_client/<int:id_client>', methods = 'DELETE')

def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({'message': 'client not found'}), 404
    
    try: 
        db.session.delete(client)
        db.session.commit()
        return jsonify ({'message': 'client delete successfully'}), 200
    
    except Exception as e: 
        db.session.rollback()
        return jsonify ({'error': str(e)})

@client.route('/api/update_client/<int: id_client>', methods = 'PUT')

def edit_client(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'},400)
    
    client = Client.query.get(id):
    if not client:
        return jsonify({'message': 'client not found'}), 404
    
    required_fields = ['name','district_address','street_address','number_address','city_address']
    
    for field in required_fields:
        if not str(data.get(field,'')).strip():
            return jsonify ({'error':f'{field.title()} is required and cannot be empty'}), 400 
        
        try:
            if 'name' in data:
                client.name = data['name']
            if 'district_address' in data:
                client.district_address = data ['district_address']
            if 'street_address' in data :
                client.street_address = data ['street_address']
            if 'number_address' in data:
                client.number_address = data ['number_address']
            if 'city_address' in data :
                client.city_address = data['city_address']
            db.session.commit()
            return jsonify({'message': 'Client update correctly','car': client.serialize()}), 200
        
        except IntegrityError as e: 
            db.session.rollback()
            error_msg = str(e.orig).lower()
            if "rut" in error_msg:
                return jsonify({'error': 'The rut is already registred'}), 400 
            
        except Exception as e: 
            db.session.rollback
            return jsonify ({'error': str(e)}), 500

@client.route('/api/update_client/<int:id_client>', methods = 'PATCH')

def update_client(id):
    data = request.get_json()
    
    if not data : 
        return jsonify ({'error': 'No data received'}), 400 
    client = Client.query.get(id)
    
    if not car: 
        return jsonify ({'message': 'Client not found'}), 404
    
    try: 
        if 'name' in data:
                client.name = data['name']
        if 'district_address' in data:
                client.district_address = data ['district_address']
        if 'street_address' in data :
                client.street_address = data ['street_address']
        if 'number_address' in data:
                client.number_address = data ['number_address']
        if 'city_address' in data :
                client.city_address = data['city_address']
        db.session.commit()
        return jsonify({'message': 'Client update correctly','car': client.serialize()}), 200
    
    except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig).lower()

            if 'rut' in error_msg:
                return jsonify({'error': 'The rut is allready registered'}), 400
            else:
                return jsonify({'error': 'Integrity constraint violated'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500