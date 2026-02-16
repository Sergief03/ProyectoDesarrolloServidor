# Autor: Mateo Saez (Corregido para compatibilidad)
# Fecha: 2026-02-10

from .db import db

class CruiseRoute(db.Model):
    __tablename__ = "cruise_route"

    idCruiseRoute = db.Column(db.Integer, primary_key=True)
    
    # Referencia corregida a 'cruises' (el plural que usó Esther)
    # Importante: idCruise en el archivo de Esther es String(50), así que aquí también.
    idCruise = db.Column(db.String(50), db.ForeignKey("cruises.idCruise"), nullable=False)
    
    # Se elimina idRoute porque no existe una tabla 'route' y causaba error.
    # La ruta es esta propia clase.
    
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    
    # Referencias a Localización (Asegúrate de que en Location.py el id sea idLocation)
    idStartLocation = db.Column(db.Integer, db.ForeignKey("location.idLocation"), nullable=False)
    idEndLocation = db.Column(db.Integer, db.ForeignKey("location.idLocation"), nullable=False)
    
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, idCruise, startDate, endDate, idStartLocation, idEndLocation, description):
        self.idCruise = idCruise
        self.startDate = startDate
        self.endDate = endDate
        self.idStartLocation = idStartLocation
        self.idEndLocation = idEndLocation
        self.description = description