import os 
import json
from app import app
from models.db import db
from models.product import Product

DATA_DIR='data'

def populate_products(data):
    created=0
    for item in data:
        name=item.get('name')
        current_price=item.get('current_price')
        stock=item.get('stock')
        supplier_id=item.get('supplier_id')
        category_id=item.get('category_id')

        if not name or current_price is None or stock is None or supplier_id is None or category_id is None:
            continue
        exists=Product.query.filter(Product.name==name).first()
        if exists:
            continue

        product=Product(name=name,current_price=current_price,stock=stock,supplier_id=supplier_id,category_id=category_id)
        db.session.add(product)
        created+=1

def populate_all():
    with app.app_context():
        print("Entering the context of the app...")
        for filename in os.listdir(DATA_DIR):
            print(f"Revisando el archivo: {filename}")
            if not filename.endswith('.json'):
                print(f"Archivo ignorado: {filename}")
                continue
            filepath=os.path.join(DATA_DIR, filename)
            with open(filepath, 'r',encoding='utf-8') as file:
                data=json.load(file)

            print(f"Datos cargados desde {filename}:{data}")
            if 'product' in filename:
                created = populate_products(data)
                print(f"{created} products uploaded from {filename}")
            else:
                print(f"Se ignoro el archivo {filename}, tipo desconocido")
        print("Committing to the database...")
        db.session.commit()
if __name__ == '__main__':
    populate_all()