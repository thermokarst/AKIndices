import numpy

from .models import DB


def getTemps(datasets, community_id, minyear, maxyear):
    model, scenario = datasets.split(',')
    data = DB.getTemps(minyear, maxyear, community_id, model, scenario)
    return data


def avg_air_temp(temps):
    year_counter, total = 0, 0
    for temp in temps:
        total += sum(temp[1])
        year_counter += 1
    return total / (year_counter * 12)


def ann_air_indices(temps):
    ATI, AFI = 0.0, 0.0
    # TODO: drop numpy
    indices = numpy.zeros((len(temps), 2), dtype='int')
    months = [0.0 for m in range(12)]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    i = 0
    for year in temps:
        j = 0
        for month in months:
            months[j] = days[j] * year[1][j]
            j += 1

        for ind in months:
            if ind >= 0.0:
                ATI = ATI + ind
            else:
                AFI = AFI + ind
        indices[i, 0], indices[i, 1] = int(ATI), int(AFI)
        ATI, AFI = 0.0, 0.0
        i += 1
    return indices


def avg_air_indices(indices):
    # TODO: drop numpy
    temp = numpy.average(indices, axis=0)
    return (int(temp[0]), int(temp[1]))


def des_air_indices(indices):
    if indices.shape[0] > 2:
        # TODO: drop numpy
        ati = numpy.sort(indices[:, 0])
        afi = numpy.sort(indices[:, 1])
        dti = (ati[-1] + ati[-2] + ati[-3]) / 3.0
        dfi = (afi[0] + afi[1] + afi[2]) / 3.0
        return (int(dti), int(dfi))
    else:
        return (None, None)


def communitiesSelect():
    return [(c.id, c.name) for c in DB.getCommunities()]


def datasetsSelect():
    return [("{0.modelname},{0.scenario}".format(d),
        "{x} ({d.resolution}) - {d.modelname} {d.scenario}".format(d=d,
                                                                   x=d.datatype.title()))
        for d in DB.getDatasets()]
