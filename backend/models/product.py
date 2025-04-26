from models.db import db

class Product(db.Model):
    __tablename__= 'product'

    id_product=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullnable=False)
    current_price=db.Column(db.Float, nullnable=False)
    stock=db.Column(db.Integer, nullnable=0)
    id_supplier=db.Column(db.Integer,db.ForeignKey('suppliers.idSupplier'))
    id_category=db.Column(db.Integer,db.ForeignKey('category.idCategory'))

    def __init__(self, name, current_price, stock, id_supplier, id_category):
        self.name=name
        self.current_price=current_price
        self.stock=stock
        self.id_supplier=id_supplier
        self.id_category=id_category

    def serialize(self):
        return{
            'id_product':self.id_product,
            'name':self.name,
            'current_price':self.current_price,
            'stock':self.stock,
            'id_supplier':self.id_supplier,
            'id_category':self.id_category
        }
