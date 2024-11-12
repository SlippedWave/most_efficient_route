from datetime import datetime
import bcrypt
from app.extensions.database import db

class User(db.Model):
    __tablename__ = "users"

    USR_userId = db.Column(db.Integer, primary_key=True)  
    USR_PER_permitId = db.Column(db.Integer, db.ForeignKey('permits.PMT_permitId'))
    USR_email = db.Column(db.String(120), unique=True, nullable=False)  
    USR_password = db.Column(db.String(250), nullable=False)  
    USR_telephone = db.Column(db.String(15))               
    USR_name = db.Column(db.String(80), nullable=False)     
    USR_last_name = db.Column(db.String(80), nullable=False) 
    USR_ST_statusId = db.Column(db.Integer, db.ForeignKey('status.ST_statusId'))
    USR_address = db.Column(db.String(150), nullable=True)
    USR_modified_by = db.Column(db.Integer, db.ForeignKey('users.USR_userId'), nullable= False)
    USR_last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    permit = db.relationship("Permit", backref="users") 
    status = db.relationship("Status", backref="users") 
    modified_by = db.relationship(
        "User",
        remote_side=[USR_userId],
        backref="modified_users"
    )

    def __init__(self, USR_email, plain_password, USR_name, USR_last_name, USR_modified_by, USR_telephone=None, USR_address=None, USR_PER_permitId=None, USR_ST_statusId=None):
        self.USR_email = USR_email
        self.set_password(plain_password)
        self.USR_name = USR_name
        self.USR_last_name = USR_last_name
        self.USR_telephone = USR_telephone
        self.USR_address = USR_address
        self.USR_PER_permitId = USR_PER_permitId
        self.USR_ST_statusId = USR_ST_statusId
        self.USR_modified_by = USR_modified_by

    def set_password(self, plain_password):
        salt = bcrypt.gensalt()
        self.USR_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)

    def check_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.USR_password.encode('utf-8'))
    
    def get_id(self):
        return self.USR_userId
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True if self.status.ST_statusId == 6 else False
    
    def get_permit(self):
        return self.permit.PMT_type
    
    def save(self):
        db.session.add(self)  
        db.session.commit()    
    
    def __repr__(self):
        return f"{self.USR_last_name}, {self.USR_name}"