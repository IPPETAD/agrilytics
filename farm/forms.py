from flask_wtf import Form
from wtforms import fields, validators
from farm import wtforms_extended_selectfield as extfields
import time

class FieldForm(Form):
    name = fields.StringField('Name')
    size = fields.FloatField('Size in Acres')
    geo_data = fields.HiddenField(id='map_input')

class SectionForm(Form):
    name = fields.StringField('Name')
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    acres = fields.FloatField('Acres of crop')

class BinForm(Form):
    name = fields.StringField('Name', [validators.required()])
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    size = fields.FloatField('Size in tonnes')

class DeleteForm(Form):
    delete = fields.HiddenField(id='delete', default='delete')

class HarvestForm(Form):
    date = fields.DateTimeField('Date', format='%Y-%m-%d', validators=[validators.required()])
    section_from = extfields.ExtendedSelectField('From Field Section', validators=[validators.required()])
    bin_to = fields.SelectField('To Bin', validators=[validators.required()])
    amount = fields.FloatField('Size in tonnes', validators=[validators.required()])