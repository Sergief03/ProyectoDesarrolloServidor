# Autor: Mateo Saez
# Fecha: 2026-02-10
from datetime import datetime
from decimal import Decimal
from .db import db


class CarRenting(db.Model):
    __tablename__ = "carRenting"

    idRent = db.Column(db.Integer, primary_key=True, autoincrement=True)

    maxPeople = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(80), nullable=False)     
    model = db.Column(db.String(80), nullable=False)     
    company = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)    
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)

    price = db.Column(db.Decimal(10, 2), nullable=False)  
    image = db.Column(db.String(255), nullable=True)      # URL o path

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    company = db.relationship('User', foreign_keys=[company])
    
    def to_dict(self):
        return {
            "idRent": self.idRent,
            "maxPeople": self.maxPeople,
            "brand": self.brand,
            "model": self.model,
            "company": self.company,
            "startDate": self.startDate.strftime("%Y/%m/%d %H:%M:%S"),
            "endDate": self.endDate.strftime("%Y/%m/%d %H:%M:%S"),
            "price": Decimal(self.price),
            "image": self.image,
            "createdAt": self.createdAt.strftime("%Y/%m/%d %H:%M:%S"),
        }

    def validate_dates(self):
        if self.endDate <= self.startDate:
            raise ValueError("endDate must be after startDate.")