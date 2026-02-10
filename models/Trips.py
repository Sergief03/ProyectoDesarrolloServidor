# Autor: Mateo Saez
# Fecha: 2026-02-10

from .db import db
from datetime import datetime
from decimal import Decimal

class Trip(db.Model):
    __tablename__ = 'trip'
    
    idTrip = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startLocation = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)
    endLocation = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    occupants = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price per person
    idCompany = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)  # FK to User with role COMPANY
    
    start_location = db.relationship('Location', foreign_keys=[startLocation])
    end_location = db.relationship('Location', foreign_keys=[endLocation])
    company = db.relationship('User', foreign_keys=[idCompany])
    
    def _repr_(self):
        return f'<Trip {self.idTrip}: {self.start_location.name} -> {self.end_location.name}>'
    
    @property
    def totalPrice(self):
        """Calculate total price based on price per person and number of occupants"""
        return Decimal(self.price) * self.occupants
    
    def to_dict(self):
        return {
            'idTrip': self.idTrip,
            'startLocation': self.startLocation,
            'startLocationName': self.start_location.name if self.start_location else None,
            'endLocation': self.endLocation,
            'endLocationName': self.end_location.name if self.end_location else None,
            'startDate': self.startDate.strftime('%Y/%m/%d %H:%M:%S') if self.startDate else None,
            'endDate': self.endDate.strftime('%Y/%m/%d %H:%M:%S') if self.endDate else None,
            'occupants': self.occupants,
            'price': float(self.price),
            'totalPrice': self.totalPrice,
            'idCompany': self.idCompany,
            'companyName': self.company.name if self.company else None
        }

