from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.phone import Phone
from models.client import Client
from models.sale import Sale 

client = Blueprint('client', __name__)


@client.route('/api/clients') #Get all clients
def get_clients():
    client = Client.query.all()
    if not client:
        return jsonify ({'message: There are no clients registred'}), 200 
    return jsonify ([clients.serialize() for clients in client])

@client.route('/api/client/<int:id_client>') #We access a client through their ID.
def get_client_id(id_client):
    client = Client.query.get_or_404(id_client)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify(client.serialize()), 200

# @client.route('api/clients/<int:id_client>/phones', methods = 'GET') #We access the customer's phone number(s) through their ID
# def get_client_phones (id_client):
#     phone = phone.query.filter_by(id_client=id_client).all()
#     return jsonify([phone.serialize] for phone in phone) 

@client.route('/api/clients/', methods= ['POST'])
def add_client():
    data = request.get_json()

    required_fields = ['name', 'rut', 'street_address', 'district_address', 'number_address', 'city_address', 'phones']
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400
    if not isinstance(data.get('phones'), list):
        return jsonify({'error': 'Phones must be a list'}), 400
    for field in ['name', 'rut', 'street_address', 'district_address', 'number_address', 'city_address']:
        if not str(data.get(field, '')).strip():
            return jsonify({'error:': f'{field.title()} is required and cannot be empty'}), 400
    for phone_data in data['phones']:
        if not isinstance(phone_data, dict) or 'phone' not in phone_data or not str(phone_data['phone']).strip():
            return jsonify({'error': 'Each phone in the list must be a dictionary with a non-empty "phone" key'}), 400

    try:
        print(f"Date received: {data}")

        new_client = Client(
            data['name'],
            data['rut'],
            data['street_address'],
            data['number_address'],
            data['district_address'],
            data['city_address'],
        )

        db.session.add(new_client)
        db.session.flush()  # Necesario para obtener el ID del cliente

        # Crear y asociar los teléfonos
        for phone_data in data['phones']:
            new_phone = Phone(
                phone=phone_data['phone'],
                id_client=new_client.id_client
            )
            db.session.add(new_phone)

        db.session.commit()
        return jsonify({
            'message': 'Client successfully created',
            'client': new_client.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        if 'rut' in error_msg:
            return jsonify({'error': 'The rut number is already registered'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding client'}), 500

@client.route('/api/clients/<int:id_client>', methods = ['DELETE'])

def delete_client(id_client):
    client = Client.query.get(id_client)
    if not client:
        return jsonify({'message': 'client not found'}), 404
    
    try: 
        db.session.delete(client)
        db.session.commit()
        return jsonify ({'message': 'client delete successfully'}), 200
    
    except Exception as e: 
        db.session.rollback()
        return jsonify ({'error': str(e)})

@client.route('/api/clients/<int:id_client>', methods = ['PUT'])

def edit_client(id_client):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'},400)
    
    client = Client.query.get(id_client)
    if not client:
        return jsonify({'message': 'client not found'}), 404
    
    required_fields = ['name','district_address','rut','street_address','number_address','city_address']
    
    for field in required_fields:
        if not str(data.get(field,'')).strip():
            return jsonify ({'error':f'{field.title()} is required and cannot be empty'}), 400 
        
        try:
            if 'name' in data:
                client.name = data['name']
            if 'district_address' in data:
                client.district_address = data ['district_address']
            if 'rut' in data :
                client.rut = data['rut']
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

@client.route('/api/clients/<int:id_client>', methods = ['PATCH'])

def update_client(id_client):
    data = request.get_json()
    
    if not data : 
        return jsonify ({'error': 'No data received'}), 400 
    client = Client.query.get(id_client)
    
    if not client: 
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