import os
import json
from app import app
from models.db import db
from models.supplier import Supplier
from models.category import Category
from models.product import Product
from models.client import Client
from models.phone import Phone
from models.sale import Sale
from models.sale_product import SaleProduct
from datetime import datetime

DATA_DIR = 'data'

def populate_suppliers(data):
    created = 0
    for item in data:
        print(f"Intentando crear proveedor con: {item}")
        supplier = Supplier(**item)
        db.session.add(supplier)
        created += 1
    return created

def populate_categories(data):
    created = 0
    for item in data:
        category = Category(**item)
        db.session.add(category)
        created += 1
    return created

def populate_products(data):
    created = 0
    for item in data:
        product = Product(**item)
        db.session.add(product)
        created += 1
    return created

def populate_clients(data):
    created = 0
    for item in data:
        client = Client(**item)
        db.session.add(client)
        created += 1
    return created

def populate_phones(data):
    created = 0
    for item in data:
        phone = Phone(**item)
        db.session.add(phone)
        created += 1
    return created

def populate_sales(data):
    created = 0
    for item in data:
        item['sale_date'] = datetime.strptime(item['sale_date'], '%Y-%m-%d').date()
        sale = Sale(**item)
        db.session.add(sale)
        created += 1
    return created

def populate_sale_products(data):
    created = 0
    for item in data:
        sale_product = SaleProduct(**item)
        db.session.add(sale_product)
        created += 1
    return created

def populate_all():
    with app.app_context():
        print("Entrando en el contexto de la app...")
        db.session.commit()

        filenames = [
            'suppliers.json',
            'categories.json',
            'clients.json',
            'phones.json',
            'products.json',
            'sales.json',
            'sale_products.json'
        ]

        for filename in filenames:
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath) and filename.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                print(f"Datos cargados desde {filename}: {data}")

                if filename == 'suppliers.json':
                    created = populate_suppliers(data)
                    print(f'{created} proveedores cargados desde {filename}')
                elif filename == 'categories.json':
                    created = populate_categories(data)
                    print(f'{created} categorías cargadas desde {filename}')
                elif filename == 'clients.json':
                    created = populate_clients(data)
                    print(f'{created} clientes cargados desde {filename}')
                elif filename == 'phones.json':
                    created = populate_phones(data)
                    print(f'{created} teléfonos cargados desde {filename}')
                elif filename == 'products.json':
                    created = populate_products(data)
                    print(f'{created} productos cargados desde {filename}')
                elif filename == 'sales.json':
                    created = populate_sales(data)
                    print(f'{created} ventas cargadas desde {filename}')
                elif filename == 'sale_products.json':
                    created = populate_sale_products(data)
                    print(f'{created} detalles de venta cargados desde {filename}')
                else:
                    print(f'Se ignoró el archivo {filename}, tipo desconocido.')
            else:
                print(f'Archivo no encontrado o no es JSON: {filename}')

        print("Haciendo commit final a la base de datos...")
        db.session.commit()

if __name__ == '__main__':
    populate_all()