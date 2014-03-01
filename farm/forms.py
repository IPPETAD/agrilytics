from flask_wtf import Form
from wtforms import fields, validators

class FieldForm(Form):
    name = fields.StringField('Name')
    size = fields.FloatField('Size in Acres')
    geo_data = fields.HiddenField(id='map_input')

