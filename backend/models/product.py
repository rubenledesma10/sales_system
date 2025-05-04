from models.db import db
#from models.supplier import Supplier
from models.category import Category

class Product(db.Model):
    __tablename__ = 'product'

    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    id_supplier = db.Column(db.Integer, db.ForeignKey('supplier.id_supplier'), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('category.id_category'), nullable=False)

    sales_products = db.relationship('SaleProduct', backref='product', lazy=True)

    def __init__(self, name, current_price, stock, id_supplier, id_category):
        self.name = name
        self.current_price = current_price
        self.stock = stock
        self.id_supplier = id_supplier
        self.id_category = id_category

    def serialize(self):
        return {
            'id_product': self.id_product,
            'name': self.name,
            'current_price': self.current_price,
            'stock': self.stock,

            'supplier': {
                'id_supplier': self.supplier.id_supplier,
                'name': self.supplier.name
            } if self.supplier else None,
            'category': {
                'id_category': self.category.id_category,
                'name': self.category.name
            } if self.category else None

        }
