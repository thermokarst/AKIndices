# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from snapindices import application
import os

engine = create_engine(application.config['ENGINE'],
                        convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    tempsnap = application.config['SNAPDATA']

    import snapextract
    import numpy
    import models
    import datetime

    datafiles = [ f for f in os.listdir(tempsnap) if os.path.isfile(os.path.join(tempsnap,f)) ]
    for f in datafiles:
        print f

    datafiles.remove('.DS_Store')
    community_file =application.config['COMMUNITIES']
    dt = numpy.dtype({'names':['community', 'northing', 'easting'],
                   'formats':['S100', 'f8', 'f8']})
    communities, eastings, northings = numpy.loadtxt(community_file,
                                                     skiprows=1, delimiter=',',
                                                     unpack=True, dtype=dt)
    communities = communities.tolist()

    modelnames =    {
                        '5modelAvg': '5 Model Avg.',
                        'cccma_cgcm3_1': 'CCCMA CGCM 3.1',
                        'CRU': 'CRU',
                        'gfdl_cm2_1': 'GFDL CM 2.1',
                        'miroc3_2_medres': 'MIROC 3.2, medres',
                        'mpi_echam5': 'MPI ECHAM 5',
                        'ukmo_hadcm3': 'UKMO HADCM 3.1'
                    }

    datasets = []

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    for filename in datafiles:
        dataset = snapextract.GeoRefData(os.path.join(tempsnap, filename))
        tokens = filename.split('_')
        startyr = int(tokens[-2])
        endyr = int(tokens[-1].split('.')[0])
        if endyr == 2100:
            endyr = 2099
        starttime = datetime.datetime.now()
        print datetime.datetime.now().strftime('%m-%d-%Y %I:%M%p')
        print filename, startyr, endyr, dataset.model, dataset.scenario

        extracted_temps = dataset.extract_points(northings, eastings,
                                                 startyr, endyr)
        print "Loading data into database..."

        if dataset.model == 'CRU':
            datasetType = 'HISTORICAL'
        else:
            datasetType = 'PROJECTION'

        dataset_sql = models.Dataset.query.filter(models.Dataset.model == dataset.model,
                                              models.Dataset.scenario == dataset.scenario).first()

        if dataset_sql is None:
            print "not in dataset...", (dataset.model, dataset.scenario)
            dataset_sql = models.Dataset(datasetType,
                             dataset.model,
                             modelnames[dataset.model],
                             dataset.scenario)
            db_session.add(dataset_sql)
            datasets.append((dataset.model, dataset.scenario))
            db_session.commit()

        min_year = numpy.min(extracted_temps['year'])
        max_year = numpy.max(extracted_temps['year'])

        time_years = max_year - min_year + 1
        i = 0
        for community in communities:
            longitude, latitude, elev = snapextract.ne_to_wgs(northings[i], eastings[i])
            location = models.Community.as_unique(db_session, name=community,
                                                    northing=northings[i],
                                                    easting=eastings[i],
                                                    latitude=latitude,
                                                    longitude=longitude)
            db_session.add(location)

            # Load up the temperature data
            db_data = numpy.zeros((time_years, 13))
            db_data[:, 0] = numpy.arange(min_year, max_year+1)
            db_data[:, 1:] = extracted_temps[i, :]['temperature'].reshape(time_years, 12)

            for row in db_data:
                data = [models.Temperature(year=row[0],
                                          january=row[1], february=row[2],
                                          march=row[3], april=row[4],
                                          may=row[5], june=row[6],
                                          july=row[7], august=row[8],
                                          september=row[9], october=row[10],
                                          november=row[11], december=row[12],
                                          updated=starttime)]

                dataset_sql.temperatures.extend(data)
                location.temperatures.extend(data)

            db_session.commit()
            i += 1

    db_session.close()
