from app.extensions.database import db
from datetime import datetime

class Package(db.Model):
    __tablename__ = "packages"

    PCK_packageId = db.Column(db.Integer, primary_key=True)
    PCK_USR_assigned_to = db.Column(db.Integer, db.ForeignKey('users.USR_userId'))  
    PCK_USR_assigned_by = db.Column(db.Integer, db.ForeignKey('users.USR_userId'))  
    PCK_street = db.Column(db.String(200), nullable=False)  
    PCK_ext_number = db.Column(db.String(10), nullable=False)  
    PCK_int_number = db.Column(db.String(10), nullable=True)  
    PCK_neighborhood = db.Column(db.String(50), nullable=False)  
    PCK_zip_code = db.Column(db.String(5), nullable=False)  
    PCK_city = db.Column(db.String(50), nullable=False)  
    PCK_state = db.Column(db.String(50), nullable=False)  
    PCK_special_instructions = db.Column(db.String(200), nullable=True)  
    PCK_client_name = db.Column(db.String(100), nullable=False)     
    PCK_client_phone_num = db.Column(db.String(15), nullable=False)               
    PCK_ST_statusId = db.Column(db.Integer, db.ForeignKey('status.ST_statusId')) 
    PCK_last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    PCK_delivery_date = db.Column(db.DateTime, nullable=True)

    assigned_to_user = db.relationship(
        "User", foreign_keys=[PCK_USR_assigned_to], backref="assigned_packages"
    )
    assigned_by_user = db.relationship(
        "User", foreign_keys=[PCK_USR_assigned_by], backref="created_packages"
    )
    status = db.relationship("Status", backref="packages")
    
    def __init__(
        self, PCK_USR_assigned_to, PCK_USR_assigned_by, PCK_street, PCK_ext_number,
        PCK_neighborhood, PCK_zip_code, PCK_city, PCK_state, PCK_client_name,
        PCK_client_phone_num, PCK_ST_statusId, PCK_int_number=None,
        PCK_special_instructions=None, PCK_delivery_date=None
    ):
        self.PCK_USR_assigned_to = PCK_USR_assigned_to
        self.PCK_USR_assigned_by = PCK_USR_assigned_by
        self.PCK_street = PCK_street
        self.PCK_ext_number = PCK_ext_number
        self.PCK_int_number = PCK_int_number
        self.PCK_neighborhood = PCK_neighborhood
        self.PCK_zip_code = PCK_zip_code
        self.PCK_city = PCK_city
        self.PCK_state = PCK_state
        self.PCK_special_instructions = PCK_special_instructions
        self.PCK_client_name = PCK_client_name
        self.PCK_client_phone_num = PCK_client_phone_num
        self.PCK_ST_statusId = PCK_ST_statusId
        self.PCK_delivery_date = PCK_delivery_date

    def __repr__(self):
        return (f"<Paquete {self.PCK_packageId} para {self.PCK_client_name} en "
                f"{self.PCK_street}, {self.PCK_ext_number}, asignado a {self.PCK_USR_assigned_to}>")
