from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.routes_product import product
from routes.routes_client import client as client_bp  # Importa el Blueprint

app = Flask(__name__)
app.register_blueprint(product)
app.register_blueprint(client_bp)  # ¡Registra el Blueprint aquí!

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    from models.product import Product
    from models.sale_product import SaleProduct
    from models.category import Category
    from models.client import Client
    from models.phone import Phone
    from models.sale import Sale
    from models.supplier import Supplier
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)