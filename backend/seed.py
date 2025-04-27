import os 
import json
from app import app
from models.db import db
from models.product import Product
from models.sale_product import SaleProduct

DATA_DIR = 'data'

def populate_products(data):
    created = 0
    for item in data:
        name = item.get('name')
        current_price = item.get('current_price')
        stock = item.get('stock')
        supplier_id = item.get('supplier_id')
        category_id = item.get('category_id')

        if not name or current_price is None or stock is None or supplier_id is None or category_id is None:
            continue

        exists = Product.query.filter(Product.name == name).first()
        if exists:
            continue

        product = Product(
            name=name,
            current_price=current_price,
            stock=stock,
            supplier_id=supplier_id,
            category_id=category_id
        )
        db.session.add(product)
        created += 1
    return created  # <- Agregado para devolver cuántos se crearon

def populate_sale_products(data):
    created = 0
    for item in data:
        subtotal = item.get('subtotal')
        quantity = item.get('quantity')
        sould_price = item.get('sould_price')
        product_id = item.get('product_id')
        sale_id = item.get('sale_id')

        if subtotal is None or quantity is None or sould_price is None or product_id is None or sale_id is None:
            continue

        sale_product = SaleProduct(
            subtotal=subtotal,
            quantity=quantity,
            sould_price=sould_price,
            product_id=product_id,
            sale_id=sale_id
        )
        db.session.add(sale_product)
        created += 1
    return created  # <- Agregado para devolver cuántos se crearon

def populate_all():
    with app.app_context():
        print("Entering the context of the app...")
        total_products = 0
        total_sale_products = 0

        for filename in os.listdir(DATA_DIR):
            print(f"Revisando el archivo: {filename}")
            if not filename.endswith('.json'):
                print(f"Archivo ignorado: {filename}")
                continue

            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

            print(f"Datos cargados desde {filename}: {data}")

            if 'product' in filename and 'sale' not in filename:
                created = populate_products(data)
                total_products += created
                print(f"{created} productos cargados desde {filename}")
            elif 'sale_product' in filename:
                created = populate_sale_products(data)
                total_sale_products += created
                print(f"{created} sale-products cargados desde {filename}")
            else:
                print(f"Se ignoró el archivo {filename}, tipo desconocido")

        print("Committing to the database...")
        db.session.commit()
        print(f"Se crearon en total {total_products} productos y {total_sale_products} sale-products.")

if __name__ == '__main__':
    populate_all()
