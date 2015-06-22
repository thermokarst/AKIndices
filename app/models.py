from . import db


class Community(db.Model):
    __tablename__ = 'communities'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(50), nullable=False, unique=True)
    northing     = db.Column(db.Float, nullable=False)
    easting      = db.Column(db.Float, nullable=False)
    latitude     = db.Column(db.Float, nullable=False)
    longitude    = db.Column(db.Float, nullable=False)
    temperatures = db.relationship('Temperature', backref='communities')


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id           = db.Column(db.Integer, primary_key=True
    datatype     = db.Column(db.String(15), nullable=False)
    model        = db.Column(db.String(15), nullable=False)
    modelname    = db.Column(db.String(50), nullable=False)
    scenario     = db.Column(db.String(15), nullable=False)
    resolution   = db.Column(db.String(15), nullable=False)
    temperatures = db.relationship('Temperature', backref='datasets')


class Temperature(db.Model):
    __tablename__ = 'temperatures'

    id           = db.Column(db.Integer, primary_key=True)
    dataset_id   = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    year         = db.Column(db.Integer, nullable=False)
    january      = db.Column(db.Float, nullable=False)
    february     = db.Column(db.Float, nullable=False)
    march        = db.Column(db.Float, nullable=False)
    april        = db.Column(db.Float, nullable=False)
    may          = db.Column(db.Float, nullable=False)
    june         = db.Column(db.Float, nullable=False)
    july         = db.Column(db.Float, nullable=False)
    august       = db.Column(db.Float, nullable=False)
    september    = db.Column(db.Float, nullable=False)
    october      = db.Column(db.Float, nullable=False)
    november     = db.Column(db.Float, nullable=False)
    december     = db.Column(db.Float, nullable=False)
    updated      = db.Column(db.DateTime, nullable=True)
