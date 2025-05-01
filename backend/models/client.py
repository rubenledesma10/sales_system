from models.db import db

class Client (db.Model):
    __tablename__= "client"
    
    id_client= db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String(50), nullable = False)
    rut = db.Column(db.String(50), nullable = False)
    street_address=db.Column(db.String (50), nullable = False)
    number_address=db.Column(db.String(50), nullable = False)
    district_address=db.Column(db.String(50), nullable = False)
    city_address = db.Column(db.String(50),nullable = False )
    phone=db.relationship('phone', backref='phone', lazy=True)
    sale=db.relationship('sale',backref='sale', lazy=True)
    
    def __init__(self,name,rut,street_address,number_address,district_address,city_address, phone, sale):
        self.name = name
        self.rut = rut
        self.street_address = street_address
        self.number_address = number_address
        self.district_address = district_address
        self.city_address = city_address
        self.phone=phone
        self.sale=sale
    
    def serialize (self):
        return {
            'id': self.id_client,
            'name': self.name,
            'rut': self.rut,
            'street_address': self.street_address,
            'number_address': self.number_address,
            'district_address': self.district_address,
            'city_address': self.city_address,
            'phone':self.phone,
            'sale':self.sale
        }