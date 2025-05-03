from models.db import db

class Phone(db.Model):
    __tablename__ = 'phone'

    id_phone = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), nullable=False)
    phone = db.Column(db.String(50), nullable=False)


    def __init__(self, id_client, phone):

        self.id_client = id_client
        self.phone = phone

    def serialize(self):
        return {
            'id_phone': self.id_phone,
            'id_client': self.id_client,
            'phone': self.phone
        }
