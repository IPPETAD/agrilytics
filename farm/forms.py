from flask_wtf import Form
from wtforms import fields, validators
from farm import wtforms_extended_selectfield as extfields
from flask.ext.babel import gettext

class FieldForm(Form):
    name = fields.StringField(gettext(u'Name'), [validators.required()])
    size = fields.FloatField(gettext(u'Size in Acres'), id='map_acres')
    geo_data = fields.HiddenField(id='map_input')

class SectionForm(Form):
    name = fields.StringField('Name', [validators.required()])
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    acres = fields.FloatField('Acres of crop')

class BinForm(Form):
    name = fields.StringField('Name', [validators.required()])
    crop = fields.SelectField('Crop', choices=[])
    size = fields.FloatField('Size in tonnes')

class DeleteForm(Form):
    delete = fields.HiddenField(id='delete', default='delete')

class OfferForm(Form):
    crop = fields.SelectField('Crop', choices=[])
    tonnes = fields.FloatField('Size in Tonnes')
    user = fields.StringField('User')
    price = fields.StringField('Price')

class ContractForm(Form):
    crop = fields.SelectField('Crop', choices=[])
    company = fields.StringField('Company', [validators.required()])
    tonnes = fields.FloatField('Tonnes')
    fixed = fields.FloatField('Fixed')
    price_per_tonne = fields.FloatField('Price per Tonne')
    contract_value = fields.FloatField('Contract Value')
    price = fields.FloatField('Price')

class HarvestForm(Form):
    date = fields.DateTimeField('Date', id="date", format='%Y-%m-%d', validators=[validators.required()])
    section_from = extfields.ExtendedSelectField('From Field Section', id='section_from', validators=[validators.NoneOf(-1, message="Please select a field") , validators.required()])
    bin_to = fields.SelectField('To Bin', id='bin_to', choices=[], validators=[validators.required()])
    amount = fields.FloatField('Size in tonnes', validators=[validators.required()])
