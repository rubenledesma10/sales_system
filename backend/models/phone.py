from models.db import db

class phone(db.Model):
    tablename = 'phone'

    id_phone = db.Column(db.Integer(20), primary_key= True )
    id_client = db.Columndb.Column(db.Integer,db.ForeignKey('client.idClient'))
    phone = db.Column(db.String(50), unique=True,nullable = False)

    def init(self,id_client,phone):
        self.id_client = id_client
        self.phone = phone

    def serialize(self):
        return {
            'id_phone' : self.id_phone,
            'id_client' : self.id_client,
            'phone' : self.phone,
        }   
