from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.phone import phone
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

@client.route('api/clients/<int:id_client>/phones', methods = 'GET') #We access the customer's phone number(s) through their ID
def get_client_phones (id_client):
    phone = phone.query.filter_by(id_client=id_client).all()
    return jsonify([phone.serialize] for phone in phone) 
