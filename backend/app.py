from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.supplier import supplier_bp
from routes.routes_product import product


app=Flask(__name__)

app.register_blueprint(product)

app.config["SQLALCHEMY_DATABASE_URI"]=DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(supplier_bp)

with app.app_context():
    from models.product import Product
    from models.sale_product import SaleProduct
<<<<<<< HEAD
=======
    from models.category import Category
    from models.client import Client
    from models.phone import Phone
    from models.sale import Sale
>>>>>>> 2e0e4be7e8ce72e4741a9afa9def84abba93aee7
    from models.supplier import Supplier
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)