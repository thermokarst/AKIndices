# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Index
from akindices.database import Base


class UniqueMixin(object):
    """
    Usage recipe from:
    http://www.sqlalchemy.org/trac/wiki/UsageRecipes/UniqueObject
    """
    @classmethod
    def unique_hash(cls, *arg, **kw):
        """
        Unique hash stub
        """
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *args, **kw):
        """
        Unique filter stub
        """
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, *arg, **kw):
        """
        as_unique
        """
        return _unique(session, cls, cls.unique_hash, cls.unique_filter,
                       cls, arg, kw)

class Community(UniqueMixin, Base):
    """
    Defines the data model for a Community

    :returns Community data
    """

    __tablename__ = 'communities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    northing = Column(Float, nullable=False)
    easting = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    temperatures = relationship("Temperature", backref='communities')

    @classmethod
    def unique_hash(cls, name, northing, easting, latitude, longitude):
        return name

    @classmethod
    def unique_filter(cls, query, name, northing, easting, latitude, longitude):
        return query.filter(Community.name == name,
                            Community.northing == northing,
                            Community.easting == easting,
                            Community.latitude == latitude,
                            Community.longitude == longitude)

    def __init__(self, name, northing, easting, latitude, longitude):
        self.name = name
        self.northing = northing
        self.easting = easting
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "Community{data}".format(data=(self.name, self.northing,
                                              self.easting, self.latitude,
                                              self.longitude))


class Dataset(Base):
    """
    Defines the data model for a Dataset

    :returns Dataset data
    """

    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    datatype = Column(String(15), nullable=False)
    model = Column(String(15), nullable=False)
    modelname = Column(String(50), nullable=True)
    scenario = Column(String(15), nullable=False)
    resolution = Column(String(15), nullable=False)

    temperatures = relationship("Temperature", backref='datasets')

    def __init__(self, datatype, model, modelname, scenario, resolution):
        self.datatype = datatype
        self.model = model
        self.modelname = modelname
        self.scenario = scenario
        self.resolution = resolution

    def __repr__(self):
        return "Dataset{data}".format(data=(self.datatype, self.model,
                                            self.modelname, self.scenario,
                                            self.resolution))


class Temperature(Base):
    """
    Defines the data model for a Temperature

    :returns Temperature data
    """

    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    community_id = Column(Integer, ForeignKey('communities.id'))
    year = Column(Integer, nullable=False)
    january = Column(Float, nullable=False)
    february = Column(Float, nullable=False)
    march = Column(Float, nullable=False)
    april = Column(Float, nullable=False)
    may = Column(Float, nullable=False)
    june = Column(Float, nullable=False)
    july = Column(Float, nullable=False)
    august = Column(Float, nullable=False)
    september = Column(Float, nullable=False)
    october = Column(Float, nullable=False)
    november = Column(Float, nullable=False)
    december = Column(Float, nullable=False)
    updated = Column(DateTime, nullable=True)

    dataset = relationship("Dataset", primaryjoin=dataset_id == Dataset.id)

    def __init__(self, year, january, february, march, april, may, june,
                 july, august, september, october, november, december, updated):
        self.year = year
        self.january = january
        self.february = february
        self.march = march
        self.april = april
        self.may = may
        self.june = june
        self.july = july
        self.august = august
        self.september = september
        self.october = october
        self.november = november
        self.december = december
        self.updated = updated

    def __repr__(self):
        return "Temperature{data}".format(data=(self.year,
                                                self.january,
                                                self.february,
                                                self.march,
                                                self.april,
                                                self.may,
                                                self.june,
                                                self.july,
                                                self.august,
                                                self.september,
                                                self.october,
                                                self.november,
                                                self.december,
                                                self.updated))

    __table_args__ = (Index('idx_temps', 'dataset_id', 'community_id', 'year', unique=True),)


def _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw):
    """
    Function to checks for an existing instances
    """
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*arg, **kw))
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj
