from flask_wtf import Form
from wtforms import fields, validators

class FieldForm(Form):
    crop = fields.SelectField('Crop', choices=[('rye', 'Rye'), ('oats', 'Oats'), ('canola', 'Canola')])
    size = fields.DecimalField('Size in Acres', places=2)
    geo_data = fields.HiddenField(id='map_input')

