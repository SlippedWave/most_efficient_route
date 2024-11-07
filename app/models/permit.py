from app.extensions.database import db

class Permit(db.Model):
    __tablename__ = "permits" 

    PMT_permitId = db.Column(db.Integer, primary_key=True)  
    PMT_type = db.Column(db.String(80), nullable=False) 

    def __init__(self, PMT_type):
        self.PMT_type = PMT_type

    def __repr__(self):
        return f"<Permiso {self.PMT_type}, {self.PMT_permitId}>"
