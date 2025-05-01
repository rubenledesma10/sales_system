from models.db import db

class Sale(db.Model):
    __tablename__ = 'sale'

<<<<<<< HEAD

    id_sale = db.Column(db.Integer, primary_key = True)
    sale_date = db.Column(db.Date, nullable = False)
    discount = db.Column(db.Float, nullable = False)
    final_amount = db.Column(db.Float, nullable = True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'))
    
    client = db.relationship("Client", backref=db.backref("sales", lazy=True))
    sale_product =db.relationship('sale_product',backref='sale_product', lazy=True)
    
    def __init__(self,sale_date,discount,final_amount):
=======
    id_sale = db.Column(db.Integer, primary_key=True)
    sale_date = db.Column(db.Date, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), nullable=False)

    sale_products = db.relationship('SaleProduct', backref='sale', lazy=True)

    def __init__(self, sale_date, final_amount, id_client, discount):
>>>>>>> f9f7c1ad3473ec4e32ae494a3332b0b320e8b3f7
        self.sale_date = sale_date
        self.discount = discount
        self.final_amount = final_amount
        self.id_client = id_client

<<<<<<< HEAD
def serialize(self):
    return {
            'id_sale': self.id_sale,
            'sale_date': self.sale_date.strftime('%d%m%Y') if self.sale_date else None,
            # asi formateamos y detallamos la fecha con el año,el horario y el mes.
=======
    def serialize(self):
        return {
            'id_sale': self.id_sale,
            'sale_date': self.sale_date.isoformat(), # Serialize date as ISO string
>>>>>>> f9f7c1ad3473ec4e32ae494a3332b0b320e8b3f7
            'discount': self.discount,
            'final_amount': self.final_amount,
            'id_client': self.id_client,
            'sale_products': [sp.serialize() for sp in self.sale_products]
        }
