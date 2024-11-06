from extensions.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    USR_userId = db.Column(db.Integer, primary_key=True)  
    USR_PER_permitId = db.Column(db.Integer, db.ForeignKey('permits.PMT_permitId'))
    USR_email = db.Column(db.String(120), unique=True, nullable=False)  
    USR_password = db.Column(db.String(250), nullable=False)  
    USR_password_salt = db.Column(db.String(250), nullable=False)  # New column for the password salt
    USR_telephone = db.Column(db.String(15))               
    USR_name = db.Column(db.String(80), nullable=False)     
    USR_last_name = db.Column(db.String(80), nullable=False) 
    USR_ST_statusId = db.Column(db.Integer, db.ForeignKey('status.ST_statusId'))
    USR_address = db.Column(db.String(50),  nullable = True)
    USR_last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    permit = db.relationship("Permit", backref="users") 
    status = db.relationship("Status", backref="users") 
    
    def __repr__(self):
        return f"<Usuario {self.USR_name} {self.USR_last_name}, {self.USR_userId}>"