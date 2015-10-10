from flask import session, render_template, request, redirect, url_for

from . import main
from .forms import AKIForm
from .utils import getTemps, avg_air_temp, ann_air_indices, \
    avg_air_indices, des_air_indices, communitiesSelect, datasetsSelect
from .models import DB


@main.route('/', methods=['GET', 'POST'])
def index():
    form = AKIForm()
    form.community.choices = communitiesSelect()
    form.dataset.choices = datasetsSelect()

    if form.validate_on_submit():
        session['community'] = request.form['community']
        session['minyear'] = request.form['minyear']
        session['maxyear'] = request.form['maxyear']
        if session['minyear'] > session['maxyear']:
            session['maxyear'] = session['minyear']

        session['datasets'] = request.form['dataset']
        return redirect(url_for('main.index'))

    session['community_data'] = None
    session['avg_temp'] = None
    session['avg_indices'] = None
    session['des_indices'] = None

    if 'community' in session:
        community_id = session['community']
        if all(key in session for key in ('minyear', 'maxyear', 'datasets')):
            community = DB.getCommunity(community_id)

            session['community_data'] = {
                'id': community_id,
                'name': community['name'],
                'latitude': round(community['latitude'], 5),
                'longitude': round(community['longitude'], 5),
            }

            session['ds_name'] = session['datasets'].split(',')

            temps_arr = getTemps(session)

            session['avg_temp'] = avg_air_temp(temps_arr)
            indices = ann_air_indices(temps_arr)
            session['avg_indices'] = avg_air_indices(indices)
            session['des_indices'] = des_air_indices(indices)

    return render_template('main/index.html', form=form)


@main.route('/datatypes')
def datatypes():
    return render_template('main/datatypes.html')


@main.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/details')
def details():
    temps = getTemps({'datasets': request.args.get('datasets', ''),
                     'minyear': request.args.get('minyear', ''),
                     'maxyear': request.args.get('maxyear', ''),
                     'community_data': {'id': request.args.get('community_id', '')}
    })
    return render_template('main/details.html',
                           lat=request.args.get('lat', ''),
                           lon=request.args.get('lon', ''),
                           community_name=request.args.get('name', ''),
                           temps=temps)


@main.route('/save')
def save():
    if 'save' in session:
        i = str(len(session['save']))
        save = session['save']
    else:
        save = dict()
        i = '0'

    save[i] = {
        'datasets': session['datasets'],
        'ds_name': session['ds_name'],
        'community_data': session['community_data'],
        'minyear': session['minyear'],
        'maxyear': session['maxyear'],
        'avg_temp': session['avg_temp'],
        'avg_indices': session['avg_indices'],
        'des_indices': session['des_indices'],
    }

    session.clear()
    session['save'] = save
    return redirect(url_for('main.index'))


@main.route('/delete')
def delete():
    record = request.args.get('record', '')
    session['save'].pop(record)
    return redirect(url_for('main.index'))
