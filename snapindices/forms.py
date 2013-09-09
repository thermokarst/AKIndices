# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import validators, ValidationError, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from snapindices.models import Community, Dataset, Temperature
from sqlalchemy import func

class SNAPYearField(IntegerField):
    def pre_validate(self, form):
        if form.model.data is not None:
            ymin,ymax = Temperature.query \
                         .with_entities(func.min(Temperature.year),
                                        func.max(Temperature.year)) \
                         .filter(Temperature.dataset_id == form.model.data.id) \
                         .all()[0]
            self.validators = [validators.NumberRange(min=ymin, max=ymax),
                               validators.Required()]

def communities():
    return Community.query.order_by('name')

def datasets():
    return Dataset.query.order_by('datatype', 'model', 'scenario')

def dataset_names(ds):
    return "{type} - {modelname} {scenario}".format(modelname=ds.modelname,
                                                      scenario=ds.scenario,
                                                      type=ds.datatype.lower()\
                                                           .capitalize())

class SNAPForm(Form):
    community = QuerySelectField(query_factory=communities,
                                 get_label='name',
                                 allow_blank=True,
                                 blank_text=u'---Select a community---',
                                 validators=[validators.Required(message='Please select a community')])

    minyear = SNAPYearField(u'minyear')

    maxyear = SNAPYearField(u'maxyear')

    model = QuerySelectField(query_factory=datasets,
                             get_label=dataset_names,
                             allow_blank=True,
                             blank_text=u'---Select a dataset---',
                             validators=[validators.Required(message='Please select a dataset')])
