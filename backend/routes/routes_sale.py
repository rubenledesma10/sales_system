from sqlalchemy import IntegrityError 
from flask import Blueprint, jsonify, request
from models.db import db
from models.sale import Sale

sale = Blueprint('sale',__name__)

@sale.route ('/api/sales'): #Traemos todas las ventas
def get_sale():
        sales = Sale.query.all()
        return jsonify([sale.serialize() for sale in sales]) 

@sale.route ('api/add_sale', method = ['POST'])
def add_sale():
    data = request.get_json()