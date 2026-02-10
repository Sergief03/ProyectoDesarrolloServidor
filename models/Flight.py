from .db import db

class Flight(db.Model):
    __tablename__ = 'flight'

    idFlight = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    maxOccupants = db.Column(db.Integer, nullable=False)
    idCompany = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    idLocationStart = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)
    idLocationEnd = db.Column(db.Integer, db.ForeignKey('location.idLocation'), nullable=False)

    company = db.relationship('User', foreign_keys=[idCompany])
    origin = db.relationship('Location', foreign_keys=[idLocationStart])
    destination = db.relationship('Location', foreign_keys=[idLocationEnd])

    def toDict(self):
        return {
            "idFlight": self.idFlight,
            "airline": self.airline,
            "startDate": self.startDate.strftime('%Y/%m/%d %H:%M:%S'),
            "endDate": self.endDate.strftime('%Y/%m/%d %H:%M:%S'),
            "price": self.price,
            "maxOccupants": self.maxOccupants,
            "idCompany": self.idCompany,
            "idLocationStart": self.idLocationStart,
            "idLocationEnd": self.idLocationEnd
        }