from models.db import db

class category(db.model):
    __tablename__='category' 
    id_category = db.Column(db.Integer, primary_key=True ) 
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(250), nullable = False)

    def __init__(self, name,description): 
        self.name = name
        self.description = description

    def serialize(self): 
        return{
            "id_category":self.id_category,
            "name": self.name,
            "description": self.description
        }
