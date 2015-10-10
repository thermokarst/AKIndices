from .models import DB


def getTemps(session):
    modelname, scenario = session['datasets'].split(',')
    data = DB.getTemps(session['minyear'],
                       session['maxyear'],
                       session['community_data']['id'],
                       modelname,
                       scenario)
    return data


def avg_air_temp(temps):
    year_counter, total = 0, 0
    for temp in temps:
        total += sum(temp[1])
        year_counter += 1
    return total / (year_counter * 12)


def ann_air_indices(temps):
    ATI, AFI = 0.0, 0.0
    indices = [[0 for x in range(2)] for y in range(len(temps))]
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
        indices[i][0], indices[i][1] = int(ATI), int(AFI)
        ATI, AFI = 0.0, 0.0
        i += 1
    return indices


def avg_air_indices(indices):
    year_counter, total_freezing, total_thawing = 0, 0, 0
    for index in indices:
        total_thawing += index[0]
        total_freezing += index[1]
        year_counter += 1
    return (int(total_thawing / year_counter), int(total_freezing / year_counter))


def des_air_indices(indices):
    if len(indices) > 2:
        ati = sorted(indices, key=lambda arr: arr[0])
        afi = sorted(indices, key=lambda arr: arr[1])
        dti = (ati[-1][0] + ati[-2][0] + ati[-3][0]) / 3.0
        dfi = (afi[0][1] + afi[1][1] + afi[2][1]) / 3.0
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
