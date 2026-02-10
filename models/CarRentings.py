# Autor: Mateo Saez
# Fecha: 2026-02-10
from datetime import datetime
from decimal import Decimal # Importante para el to_dict
from .db import db

class CarRenting(db.Model):
    __tablename__ = "carRenting"

    # Corregido: idCarRenting según normas
    idCarRenting = db.Column(db.Integer, primary_key=True, autoincrement=True)

    maxPeople = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(80), nullable=False)     
    model = db.Column(db.String(80), nullable=False)     
    
    # --- CORRECCIÓN AQUÍ ---
    # 1. Cambiamos el nombre de la COLUMNA a 'idCompany'
    idCompany = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)    
    
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)

    price = db.Column(db.Numeric(10, 2), nullable=False)  
    image = db.Column(db.String(255), nullable=True)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 2. La RELACIÓN usa la columna 'idCompany' como llave foránea
    company = db.relationship('User', foreign_keys=[idCompany])
    
    def to_dict(self):
        return {
            "idCarRenting": self.idCarRenting,
            "maxPeople": self.maxPeople,
            "brand": self.brand,
            "model": self.model,
            "idCompany": self.idCompany, # Devolvemos el ID
            "startDate": self.startDate.strftime("%Y/%m/%d %H:%M:%S"),
            "endDate": self.endDate.strftime("%Y/%m/%d %H:%M:%S"),
            "price": float(self.price), # Mejor float para evitar problemas con JSON
            "image": self.image,
            "createdAt": self.createdAt.strftime("%Y/%m/%d %H:%M:%S"),
        }

    def validate_dates(self):
        if self.endDate <= self.startDate:
            raise ValueError("endDate must be after startDate.")