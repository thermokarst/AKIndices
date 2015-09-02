from numpy import arange, hstack

from flask import session, render_template, request, redirect, current_app

from . import main
from .forms import AKIForm
from .utils import getTemps, avg_air_temp, ann_air_indices, avg_air_indices, des_air_indices
from app.models import Community, Dataset, Temperature


@main.route('/', methods=['GET'])
def index():
    form = AKIForm()
    session['community_data'] = None
    session['avg_temp'] = None
    session['avg_indices'] = None
    session['des_indices'] = None

    if 'community' in session:
        community_id = session['community']
        if all(key in session for key in ('minyear', 'maxyear', 'datasets')):
            community = Community.query.get_or_404(community_id)

            # TODO: clean this up
            session['community_data'] = dict()
            session['community_data']['id'] = community_id
            session['community_data']['name'] = community.name
            session['community_data']['latitude'] = round(community.latitude, 5)
            session['community_data']['longitude'] = round(community.longitude, 5)

            session['ds_name'] = Dataset.query. \
                with_entities(Dataset.modelname, Dataset.scenario). \
                filter_by(id=session['datasets']).all()
            temps_arr = getTemps(session['datasets'], community_id, session['minyear'], session['maxyear'])

            session['avg_temp'] = avg_air_temp(temps_arr)
            indices = ann_air_indices(temps_arr)
            session['avg_indices'] = avg_air_indices(indices)
            session['des_indices'] = des_air_indices(indices)

    return render_template("index.html", form=form)


@main.route('/', methods=['POST'])
def index_submit():
    form = AKIForm()
    if form.validate():
        session['community'] = request.form['community']
        session['minyear'] = request.form['minyear']
        session['maxyear'] = request.form['maxyear']
        if session['minyear'] > session['maxyear']:
            session['maxyear'] = session['minyear']

        session['datasets'] = request.form['model']
        return redirect('/')
    else:
        return render_template("index.html", form=form)


@main.route('/datatypes')
def datatypes():
    return render_template("datatypes.html")


@main.route('/reset')
def reset():
    session.clear()
    return redirect('/')


@main.route('/details')
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
        temps=temps)


@main.route('/save')
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


@main.route('/delete')
def delete():
    record = request.args.get('record', '')
    session['save'].pop(record)
    return redirect('/')
