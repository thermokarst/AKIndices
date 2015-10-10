from flask_wtf import Form
from wtforms import IntegerField, SelectField
from wtforms.validators import NumberRange, Required
from sqlalchemy import func

from .models import Temperature, DB

from flask import current_app


class AKIYearField(IntegerField):
    def pre_validate(self, form):
        pass
        # if form.dataset.data is not None:
        #     ymin, ymax = Temperature.query \
        #         .with_entities(func.min(Temperature.year),
        #                        func.max(Temperature.year)) \
        #         .filter(Temperature.dataset_id == form.dataset.data.id).all()[0]
        #     self.validators = [NumberRange(min=ymin, max=ymax), Required()]


class AKIForm(Form):
    community = SelectField(coerce=int,
                            validators=[Required(message='Please select a community')])
    dataset = SelectField(validators=[Required(message='Please select a dataset')])
    minyear = AKIYearField('minyear')
    maxyear = AKIYearField('maxyear')
