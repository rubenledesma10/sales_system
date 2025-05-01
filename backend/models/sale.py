from models.db import db

class Sale(db.Model): 
    __tablename__ ='sale'

    id_sale = db.Column(db.Integer, primary_key = True)
    sale_date = db.Column(db.Date, nullable = False)
    discount = db.Column(db.Float, nullable = False)
    final_amount = db.Column(db.Float, nullable = True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'))
    
    client = db.relationship("Client", backref=db.backref("sales", lazy=True))
    sale_product =db.relationship('sale_product',backref='sale_product', lazy=True)
    
    def __init__(self,sale_date,discount,final_amount):
        self.sale_date = sale_date
        self.discount = discount
        self.final_amount = final_amount 
        
    def __repr__(self): #Realizamos el repr, representacion, para mostrar el id, la  fecha y el id del cliente que realizo la venta.
        return f"<Sale(id_sale={self.id_sale}, sale_date={self.sale_date}, client_id={self.id_client})>"

def serialize(self):
    return {
            'id_sale': self.id_sale,
            'sale_date': self.sale_date.strftime('%d%m%Y') if self.sale_date else None,
            # asi formateamos y detallamos la fecha con el año,el horario y el mes.
            'discount': self.discount,
            'final_amount': self.final_amount,
            'id_client': self.id_client
    }