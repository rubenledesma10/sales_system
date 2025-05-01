from models.db import db

class SaleProduct(db.Model):
    __tablename__ = 'sale_product'

    id_sale_product = db.Column(db.Integer, primary_key=True)
    subtotal = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sold_price = db.Column(db.Float, nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id_product'), nullable=False)
    id_sale = db.Column(db.Integer, db.ForeignKey('sale.id_sale'), nullable=False)

    def __init__(self, subtotal, quantity, sold_price, id_product, id_sale):
        self.subtotal = subtotal
        self.quantity = quantity
        self.sold_price = sold_price
        self.id_product = id_product
        self.id_sale = id_sale

    def serialize(self):
        return {
            'id_sale_product': self.id_sale_product,
            'subtotal': self.subtotal,
            'quantity': self.quantity,
            'sold_price': self.sold_price,
            'id_product': self.id_product,
            'id_sale': self.id_sale
        }
