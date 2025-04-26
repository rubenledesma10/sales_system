from models.db import db

class Product(db.Model):
    __tablename__= 'product'

    id_product=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullnable=False)
    current_price=db.Column(db.Float, nullnable=False)
    stock=db.Column(db.Integer, nullnable=0)
    supplier_id=db.Column(db.Integer,db.ForeignKey('suppliers.idSupplier'))
    category_id=db.Column(db.Integer,db.ForeignKey('category.idCategory'))

    def __init__(self, name, current_price, stock, supplier_id, category_id):
        self.name=name
        self.current_price=current_price
        self.stock=stock
        self.supplier_id=supplier_id
        self.category_id=category_id

    def serialize(self):
        return{
            'id_product':self.id_product,
            'name':self.name,
            'current_price':self.current_price,
            'stock':self.stock,
            'supplier_id':self.supplier_id,
            'category_id':self.category_id
        }
