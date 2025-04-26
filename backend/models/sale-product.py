from models.db import db

class SaleProduct(db.Model):
    __table__='sale-product'

    id_sale_product=db.Column(db.Integer, primaryKey=True)
    subtotal=db.Column(db.Float, nullnable=False)
    quantity=db.Column(db.Integer, nullnable=False)
    sould_price=db.Column(db.Float, nullnable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.idProduct'))
    sale_id=db.Column(db.Integer,db.ForeignKey('sale.idSale'))

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