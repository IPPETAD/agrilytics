from flask_wtf import Form
from wtforms import fields, validators

class FieldForm(Form):
    name = fields.StringField('Name', [validators.required()])
    size = fields.FloatField('Size in Acres')
    geo_data = fields.HiddenField(id='map_input')

class SectionForm(Form):
    name = fields.StringField('Name', [validators.required()])
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    acres = fields.FloatField('Acres of crop')

class BinForm(Form):
    name = fields.StringField('Name', [validators.required()])
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    size = fields.FloatField('Size in Tonnes')

class DeleteForm(Form):
    delete = fields.HiddenField(id='delete', default='delete')
