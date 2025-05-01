from models.db import db

class SaleProduct(db.Model):
    __tablename__='sale_product'

    id_sale_product=db.Column(db.Integer, primary_key=True)
    subtotal=db.Column(db.Float, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    sould_price=db.Column(db.Float, nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id_product'))
    sale_id=db.Column(db.Integer,db.ForeignKey('sale.id_sale'))
    

    def __init__(self, subtotal, quantity, sould_price, product_id, sale_id):
        self.subtotal=subtotal
        self.quantity=quantity
        self.sould_price=sould_price
        self.product_id=product_id
        self.sale_id=sale_id

    def serialize(self):
        return{
            'id_sale_product':self.id_sale_product,
            'subtotal':self.subtotal,
            'quantity':self.quantity,
            'sould_price':self.sould_price,
            'product_id':self.product_id,
            'sale_id':self.sale_id
        }