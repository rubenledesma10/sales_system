from models.db import db
        
class Client(db.Model):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(150), nullable=False)
    number_address = db.Column(db.String(50), nullable=False)
    district_address = db.Column(db.String(150), nullable=False)
    city_address = db.Column(db.String(50), nullable=False)

    phones = db.relationship('Phone', backref='client', lazy=True)
    sales = db.relationship('Sale', backref='client', lazy=True)

    def __init__(self, rut, name, street_address, number_address, district_address, city_address):

        self.rut = rut
        self.name = name
        self.street_address = street_address
        self.number_address = number_address
        self.district_address = district_address
        self.city_address = city_address

    def serialize(self):
        return {
            'id_client': self.id_client,
            'rut': self.rut,
            'name': self.name,
            'street_address': self.street_address,
            'number_address': self.number_address,
            'district_address': self.district_address,
            'city_address': self.city_address,
            'phones': [phone.serialize() for phone in self.phones] if self.phones else [],
            'sales': [sale.serialize() for sale in self.sales] if self.sales else []
        }