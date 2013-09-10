# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, flash, redirect, url_for, session, current_app
from snapindices import application
from snapindices.database import db_session
from snapindices.models import Community, Temperature, Dataset
from forms import SNAPForm
from numpy import zeros, arange, hstack
from processing import ann_air_indices, avg_air_indices, des_air_indices, avg_air_temp, c_to_f

@application.route('/', methods = ['GET', 'POST'])
def index():
    form = SNAPForm()

    # Deal with form posting here
    if request.method == 'POST':
        if form.validate():
            session['community'] = request.form['community']
            session['minyear'] = request.form['minyear']
            session['maxyear'] = request.form['maxyear']
            if session['minyear'] > session['maxyear']:
                session['maxyear'] = session['minyear']

            session['datasets'] = request.form['model']
            return redirect('/')
        else:
            return render_template("index.html",
            title = application.config['TITLE'],
            form = form,
            )

    # Deal with page gets here
    if request.method == 'GET':
        session['community_data'] = None
        modelstash = None # Need this
        session['avg_temp'] = None
        session['avg_indices'] = None
        session['des_indices'] = None

        if 'community' in session:
            community_id = session['community']

            if all (key in session for key in ('minyear', 'maxyear', 'datasets')):
                session['community_data'] = dict()
                session['community_data']['id'] = community_id
                session['community_data']['name'] = db_session.query(Community).get(community_id).name
                session['community_data']['latitude'] = round(db_session.query(Community).get(community_id).latitude, 5)
                session['community_data']['longitude'] = round(db_session.query(Community).get(community_id).longitude, 5)

                session['ds_name'] = db_session.query(Dataset.modelname, Dataset.scenario). \
                                                      filter(Dataset.id == session['datasets']).all()
                temps_arr = getTemps(session['datasets'], community_id, session['minyear'], session['maxyear'])

                session['avg_temp'] = avg_air_temp(temps_arr)
                indices = ann_air_indices(temps_arr)
                session['avg_indices'] = avg_air_indices(indices)
                session['des_indices'] = des_air_indices(indices)

        return render_template("index.html",
            title = application.config['TITLE'],
            form = form
            )

@application.route('/reset')
@application.route('/clear')
def reset():
    session.clear()
    return redirect('/')

@application.route('/save')
def save():
    if 'save' in session:
        i = len(session['save'])
        save = session['save']
    else:
        save = dict()
        i = 0

    save[i] = dict()
    save[i]['datasets'] = session['datasets']
    save[i]['ds_name'] = session['ds_name']
    save[i]['community_data'] = session['community_data']
    save[i]['minyear'] = session['minyear']
    save[i]['maxyear'] = session['maxyear']
    save[i]['avg_temp'] = session['avg_temp']
    save[i]['avg_indices'] = session['avg_indices']
    save[i]['des_indices'] = session['des_indices']
    session.clear()
    session['save'] = save
    return redirect('/')

@application.route('/delete')
def delete():
    record = request.args.get('record', '')
    session['save'].pop(record)
    return redirect('/')

@application.route('/datatypes')
def datatypes():
    return render_template("datatypes.html",
        title=application.config['TITLE'])

@application.route('/details')
def details():
    datasets = request.args.get('datasets', '')
    community_id = request.args.get('community_id', '')
    minyear = request.args.get('minyear', '')
    maxyear = request.args.get('maxyear', '')
    temps = getTemps(datasets, community_id, minyear, maxyear)
    years = arange(int(minyear), int(maxyear)+1).reshape(int(maxyear)-int(minyear) + 1, 1)
    temps = hstack((years, temps))
    return render_template("details.html",
        lat=request.args.get('lat', ''),
        lon=request.args.get('lon', ''),
        community_name=request.args.get('name', ''),
        temps=temps,
        title=application.config['TITLE'])

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def getTemps(datasets, community_id, minyear, maxyear):
    # Get the temps
    temps = db_session.query(Temperature, Dataset). \
            filter(Dataset.id == Temperature.dataset_id,
                   Dataset.id == datasets,
                   Temperature.community_id == community_id,
                   Temperature.year >= minyear,
                   Temperature.year <= maxyear)

    length = int(maxyear) - int(minyear)
    temps_arr = zeros((length+1, 12))

    i = 0
    for temp in temps.all():
        t = temp[0]
        temps_arr[i,:] =  [t.january, t.february, t.march,
                           t.april, t.may, t.june,
                           t.july, t.august, t.september,
                           t.october, t.november, t.december]
        i += 1
    return temps_arr

@application.before_request
def log_request():
    current_app.logger.info('Request\nIP: {addr}\nSESSION: {session}' \
                            .format(addr=request.remote_addr,
                                    session=session))

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           title=application.config['TITLE']), 404

@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html',
                           title=application.config['TITLE']), 500
