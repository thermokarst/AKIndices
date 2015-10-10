from flask_wtf import Form
from wtforms import IntegerField, SelectField
from wtforms.validators import NumberRange, Required


class AKIYearField(IntegerField):
    def pre_validate(self, form):
        if form.data['dataset'] == 'CRU,TS31':
            self.validators = [NumberRange(min=1901, max=2009), Required()]
        else:
            self.validators = [NumberRange(min=2001, max=2099), Required()]


class AKIForm(Form):
    community = SelectField(coerce=int,
                            validators=[Required(message='Please select a community')])
    dataset = SelectField(validators=[Required(message='Please select a dataset')])
    minyear = AKIYearField('minyear')
    maxyear = AKIYearField('maxyear')
