from app.extensions.database import db

class Status(db.Model):
    __tablename__ = "status" 

    ST_statusId = db.Column(db.Integer, primary_key=True)  
    ST_value = db.Column(db.String(80), nullable=False)
    ST_status_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Estado {self.ST_statusId}, {self.ST_value}>"  
