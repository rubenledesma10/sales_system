from models.db import db
#from models.product import Product

class Supplier(db.Model):
    __tablename__ = 'supplier'

    id_supplier = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    web_page = db.Column(db.String(20),nullable=False)
    rut = db.Column(db.String(20),nullable=False)

    products = db.relationship('Product', backref='supplier', lazy=True,cascade='all, delete-orphan')

    def __init__(self, name, address, phone, web_page, rut):
        self.name = name
        self.address = address
        self.phone = phone
        self.web_page = web_page
        self.rut = rut



    def serialize_basic(self):
        return {
            'id_supplier': self.id_supplier,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'web_page': self.web_page,
            'rut': self.rut,
        }

    def serialize(self):
        return {
            'id_supplier': self.id_supplier,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'web_page': self.web_page,
            'rut': self.rut,
            'products': [product.serialize() for product in self.products]
        }
    

    
