from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]=DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.product import Product
    from models.sale_product import SaleProduct
    from models.db import db
    from models.sale import Sale
    from datetime import datetime
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)