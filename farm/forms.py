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
