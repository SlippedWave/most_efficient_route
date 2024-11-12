from app.extensions.database import db
from datetime import datetime

class Package(db.Model):
    __tablename__ = "packages"

    PCK_packageId = db.Column(db.Integer, primary_key=True)
    PCK_USR_assigned_to = db.Column(db.Integer, db.ForeignKey('users.USR_userId'), nullable = True)  
    PCK_USR_modified_by = db.Column(db.Integer, db.ForeignKey('users.USR_userId'), nullable = False)  
    PCK_ADD_addressId = db.Column(db.Integer, db.ForeignKey('addresses.ADD_addressId'), nullable=False)
    PCK_client_name = db.Column(db.String(100), nullable=False)     
    PCK_client_phone_num = db.Column(db.String(15), nullable=False)               
    PCK_ST_statusId = db.Column(db.Integer, db.ForeignKey('status.ST_statusId')) 
    PCK_last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    PCK_delivery_date = db.Column(db.DateTime, nullable=True)
    PCK_special_delivery_instructions = db.Column(db.String(200), nullable=True)
    
    assigned_to_user = db.relationship(
        "User", foreign_keys=[PCK_USR_assigned_to], backref="assigned_packages"
    )
    assigned_by_user = db.relationship(
        "User", foreign_keys=[PCK_USR_modified_by], backref="created_packages"
    )
    status = db.relationship("Status", backref="packages")
    address = db.relationship("Address", backref="packages")

    def __init__(
        self, PCK_USR_assigned_to, PCK_USR_modified_by, PCK_ADD_addressId, 
        PCK_client_name, PCK_client_phone_num, PCK_ST_statusId, 
        PCK_delivery_date=None, PCK_special_delivery_instructions= None
    ):
        self.PCK_USR_assigned_to = PCK_USR_assigned_to
        self.PCK_USR_modified_by = PCK_USR_modified_by
        self.PCK_ADD_addressId = PCK_ADD_addressId
        self.PCK_client_name = PCK_client_name
        self.PCK_client_phone_num = PCK_client_phone_num
        self.PCK_ST_statusId = PCK_ST_statusId
        self.PCK_delivery_date = PCK_delivery_date
        self.PCK_special_delivery_instructions = PCK_special_delivery_instructions

    def __repr__(self):
        return (f"Paquete {self.PCK_packageId} para {self.PCK_client_name} en dirección con ID {self.PCK_ADD_addressId}, "
                f"asignado a {self.PCK_USR_assigned_to}")
