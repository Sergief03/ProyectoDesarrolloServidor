# Autor: Mateo Saez
# Fecha: 2026-02-10

from .db import db
from decimal import Decimal

class Tour(db.Model):
    __tablename__ = "tour"

    idTour = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # --- CAMBIO 1: Renombrar Columnas (ids) ---
    idLocation = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    occupants = db.Column(db.Integer, nullable=False)
    
    # --- CAMBIO 2: Renombrar Columnas (ids) ---
    idCompany = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    
    # --- CAMBIO 3: La relación apunta a las nuevas columnas ---
    location = db.relationship('Location', foreign_keys=[idLocation])
    company = db.relationship('User', foreign_keys=[idCompany])
    
    # Corrección: __repr__ lleva DOBLE guion bajo
    def __repr__(self):
        return f'<Tour {self.idTour}: {self.title}>'

    @property
    def totalPrice(self):
        """Calculate total price based on price per person and number of occupants"""
        return Decimal(self.price) * self.occupants

    # Método útil para el controlador (opcional pero recomendado)
    def toDict(self):
        return {
            "idTour": self.idTour,
            "title": self.title,
            "description": self.description,
            "idLocation": self.idLocation,
            "image": self.image,
            "price": float(self.price),
            "startDate": self.startDate.strftime("%Y/%m/%d %H:%M:%S"),
            "endDate": self.endDate.strftime("%Y/%m/%d %H:%M:%S"),
            "occupants": self.occupants,
            "idCompany": self.idCompany
        }