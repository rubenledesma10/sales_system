from models.db import db

class Sale(db.Model):
    __tablename__ = 'sale'

    id_sale = db.Column(db.Integer, unique = True, primary_key=True)
    sale_date = db.Column(db.Date, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=True)

    id_client = db.Column(db.Integer,db.ForeignKey('client.id_client'), nullable=False)

    sale_products = db.relationship('SaleProduct', backref='sale', lazy=True, cascade="all, delete-orphan")

    def __init__(self, sale_date, id_client, discount,final_amount=None):
        self.sale_date = sale_date
        self.discount = discount
        self.final_amount = final_amount
        self.id_client = id_client

    def serialize(self):
        return {
            'id_sale': self.id_sale,
            'sale_date': self.sale_date.isoformat(), 
            'discount': self.discount,
            'final_amount': self.final_amount,
            'id_client': self.id_client,
            'sale_products': [sp.serialize() for sp in self.sale_products]
        }