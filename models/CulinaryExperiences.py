# Autor: Mateo Saez
# Fecha: 2026-02-10

from .db import db
from decimal import Decimal

class CulinaryExperience(db.Model):
    __tablename__ = "culinary_experience"
    
    idCulinaryExperience = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    occupants = db.Column(db.Integer, nullable=False)

    # --- CORRECCIÓN 1: Renombrar Columnas (ids) ---
    idLocation = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)
    idCompany = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    
    # --- CORRECCIÓN 2: Apuntar la relación a las nuevas columnas ---
    # La relación se sigue llamando 'location' (el objeto), pero se basa en 'idLocation' (el dato)
    location = db.relationship('Location', foreign_keys=[idLocation])
    company = db.relationship('User', foreign_keys=[idCompany])
    
    # Corrección extra: es __repr__ (doble guion bajo), no _repr_
    def __repr__(self):
        return f'<CulinaryExperience {self.idCulinaryExperience}: {self.category}>'

    @property
    def totalPrice(self):
        """Calculate total price based on price per person and number of occupants"""
        # Convertimos a float para evitar líos, o lo dejamos en Decimal si lo necesitas exacto
        return Decimal(self.price) * self.occupants

    def toDict(self):
        return {
            "idCulinaryExperience": self.idCulinaryExperience,
            "category": self.category,
            "price": float(self.price),
            "startDate": self.startDate.strftime("%Y/%m/%d %H:%M:%S"),
            "occupants": self.occupants,
            "totalPrice": float(self.totalPrice),
            "idLocation": self.idLocation,
            "idCompany": self.idCompany
        }