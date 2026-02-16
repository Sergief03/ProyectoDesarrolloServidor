# Autor: Mateo Saez
# Fecha: 2026-02-10

from .db import db

from decimal import Decimal

class CulinaryExperience(db.Model):
    __tablename__ = "culinary_experience"
    
    idCulinaryExperience = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    occupants = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    
    location = db.relationship('Location', foreign_keys=[location])
    company = db.relationship('User', foreign_keys=[company])
    
    def _repr_(self):
        return f'<CulinaryExperience {self.idCulinaryExperience}: {self.category}>'

    @property
    def totalPrice(self):
        """Calculate total price based on price per person and number of occupants"""
        return Decimal(self.price) * self.occupants