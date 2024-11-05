from ..extensions import db

class User(db.Model):
    __tablename__ = "users"

    USR_userId = db.Column(db.Integer, primary_key=True)  
    USR_PER_PermitId = db.Column(db.Integer, db.ForeignKey('permits.PMT_permit_Id'))
    USR_Email = db.Column(db.String(120), unique=True, nullable=False)  
    USR_Password = db.Column(db.String(128), nullable=False)  
    USR_telephone = db.Column(db.String(15))               
    USR_name = db.Column(db.String(80), nullable=False)     
    USR_last_name = db.Column(db.String(80), nullable=False) 
    USR_ST_status_Id = db.Column(db.Integer, db.ForeignKey('status.ST_statusId'))

    permit = db.relationship("Permit", backref="users") 
    status = db.relationship("Status", backref="users") 
    
    def __repr__(self):
        return f"<Usuario {self.USR_name} {self.USR_last_name}, {self.USR_userId}>"  
