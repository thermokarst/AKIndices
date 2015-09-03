from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import NumberRange, Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import func

from .models import Community, Dataset, Temperature


class AKIYearField(IntegerField):
    def pre_validate(self, form):
        if form.model.data is not None:
            ymin, ymax = Temperature.query \
                .with_entities(func.min(Temperature.year),
                               func.max(Temperature.year)) \
                .filter(Temperature.dataset_id == form.model.data.id).all()[0]
            self.validators = [NumberRange(min=ymin, max=ymax), Required()]


def communities():
    return Community.query.order_by('name')


def datasets():
    return Dataset.query.order_by('datatype', 'model', 'scenario')


def dataset_names(ds):
    return "{0.type} ({0.resolution}) - {0.modelname} {0.scenario}".format(ds)


class AKIForm(Form):
    community = QuerySelectField(query_factory=communities,
                                 get_label='name',
                                 allow_blank=True,
                                 blank_text='---Select a community---',
                                 validators=[Required(message='Please select a community')])

    minyear = AKIYearField('minyear')
    maxyear = AKIYearField('maxyear')

    model = QuerySelectField(query_factory=datasets,
                             get_label=dataset_names,
                             allow_blank=True,
                             blank_text='---Select a dataset---',
                             validators=[Required(message='Please select a dataset')])
