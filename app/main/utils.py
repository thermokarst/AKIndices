import numpy

from app.models import Temperature, Dataset


def getTemps(datasets, community_id, minyear, maxyear):
    temps = Temperature.query.join(Dataset). \
            filter(Dataset.id == Temperature.dataset_id,
                   Dataset.id == datasets,
                   Temperature.community_id == community_id,
                   Temperature.year >= minyear,
                   Temperature.year <= maxyear)

    length = int(maxyear) - int(minyear)
    temps_arr = numpy.zeros((length+1, 12))

    i = 0
    for t in temps.all():
        temps_arr[i,:] =  [t.january, t.february, t.march,
                           t.april, t.may, t.june,
                           t.july, t.august, t.september,
                           t.october, t.november, t.december]
        i += 1
    return temps_arr


def avg_air_temp(temps):
    return numpy.average(temps)


def ann_air_indices(temps):
    ATI, AFI = 0.0, 0.0
    indices = numpy.zeros((temps.shape[0], 2), dtype='int')
    months = [0.0 for m in range(12)]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    i = 0
    for year in temps:
        j = 0
        for month in months:
            months[j] = days[j] * year[j]
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
    temp = numpy.average(indices, axis=0)
    return (int(temp[0]), int(temp[1]))


def des_air_indices(indices):
    if indices.shape[0] > 2:
        ati = numpy.sort(indices[:,0])
        afi = numpy.sort(indices[:,1])
        dti = (ati[-1] + ati[-2] + ati[-3]) / 3.0
        dfi = (afi[0] + afi[1] + afi[2]) / 3.0
        return (int(dti), int(dfi))
    else:
        return (None, None)


def c_to_f(temp):
    return (temp * 9. / 5.) + 32.
