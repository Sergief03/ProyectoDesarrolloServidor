from .db import db

class Cruise(db.Model):
    __tablename__ = 'cruises'
    id = db.Column(db.Integer, primary_key=True)
    idCruise = db.Column(db.String(50), nullable=False)
    startLocation = db.Column(db.String(50), nullable=False)
    endLocation = db.Column(db.String(50), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, idCruise, startLocation, endLocation, startDate, endDate, description):
        self.idCruise = idCruise
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.startDate = startDate
        self.endDate = endDate
        self.description = description

# Metodos para obtener cruceros
    def getCruises(self):
        return Cruise.query.all()
    
    def getCruise(self, id):
        return Cruise.query.get(id)
    
    def getStartLocation(self, startLocation):
        return Cruise.query.filter_by(startLocation=startLocation).all()
    
    def getEndLocation(self, endLocation):
        return Cruise.query.filter_by(endLocation=endLocation).all()
    
    def getStartDate(self, startDate):
        return Cruise.query.filter_by(startDate=startDate).all()
    
    def getEndDate(self, endDate):
        return Cruise.query.filter_by(endDate=endDate).all()
    
    def getDescription(self, description):
        return Cruise.query.filter_by(description=description).all()

# Metodos para actualizar cruceros
    def setStartLocation(self, startLocation):
        self.startLocation = startLocation
    
    def setEndLocation(self, endLocation):
        self.endLocation = endLocation
    
    def setStartDate(self, startDate):
        self.startDate = startDate
    
    def setEndDate(self, endDate):
        self.endDate = endDate
    
    def setDescription(self, description):
        self.description = description