# Autor: Mateo Saez
# Fecha: 2026-02-10

from .db import db
from decimal import Decimal

class Tour(db.Model):
    __tablename__ = "tour"

    idTour = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    occupants = db.Column(db.Integer, nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    
    location = db.relationship('Location', foreign_keys=[location])
    company = db.relationship('User', foreign_keys=[company])
    
    def _repr_(self):
        return f'<Tour {self.idTour}: {self.title}>'

    @property
    def totalPrice(self):
        """Calculate total price based on price per person and number of occupants"""
        return Decimal(self.price) * self.occupants