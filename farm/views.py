from farm import app
from farm import forms
from flask import render_template, request, url_for, redirect
from flask_wtf.csrf import CsrfProtect

from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'

mongo = PyMongo(app)
csrf = CsrfProtect(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fields')
def fields():
    fields = mongo.db.fields.find()
    return render_template('fields.html', fields = fields)

@app.route('/bins')
def bins():
    bins = mongo.db.bins.find()
    return render_template('bins.html', bins = bins)

@app.route('/field/<field_id>/')
def field(field_id):
    field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
    crops = []
    for section in field['section']:
        if section['crop'] not in crops:
            crops.append(section['crop'].title())
    return render_template('field.html', field = field, crops=crops)

@app.route('/market')
def marketplace():
    crop = request.args.get("crop");
    offers = list(mongo.db.offers.find({"crop": crop}))
    crop_types = list(mongo.db.crop_types.find())
    return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types)

@app.route('/field/add', methods=['GET', 'POST'])
def field_add():
    form = forms.FieldForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = {"name": form.name.data, "size": form.size.data, "geo": form.geo_data.data, "section": []}
            field_id = mongo.db.fields.insert(post)
            return redirect(url_for('.field', field_id=field_id))
    else:
        return render_template('field_add.html', form=form)

@app.route('/field/<field_id>/edit', methods=['GET', 'POST'])
def field_edit(field_id):
    form = forms.FieldForm()
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    if request.method == 'POST':
        if form.validate_on_submit():
            field['name'] = form.name.data
            field['size'] = form.size.data
            field['geo'] = form.geo_data.data
            field_id = mongo.db.fields.save(field)
            return redirect(url_for('field', field_id=field_id))
    else:
        form.name.data = field['name']
        form.size.data = field['size']
        form.geo_data.data = field['geo']
        return render_template('field_edit.html', form=form)

@app.route('/field/<field_id>/section/add', methods=['GET','POST'])
def section_add(field_id):
    form = forms.SectionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
            if 'section' not in field.keys():
                field['section'] = []
            field['section'].append({'name': form.name.data, 'crop': form.crop.data, 'acres': form.acres.data})
            field_id = mongo.db.fields.save(field)
            return redirect(url_for('field', field_id=field_id))
    else:
        return render_template('section_add.html', form=form, field_id=field_id)

@app.route('/field/<field_id>/section/<name>')
def section(field_id, name):
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    for section in field['section']:
        if section['name'] == name:
            sec = section
            break
    return render_template('section.html', field=field, section=section)
        

@app.route('/bin/<bin_id>', methods=['GET', 'POST'])
def bin(bin_id):
    form = forms.DeleteForm()
    if request.method == 'POST' and 'delete' in request.form.keys():
        if mongo.db.bins.remove({ "_id": ObjectId(bin_id) }):
            return redirect(url_for('bins'))

    bin = mongo.db.bins.find_one({"_id": ObjectId(bin_id) })
    return render_template('bin.html', bin = bin, form = form)

@app.route('/bin/add', methods=['GET', 'POST'])
def bin_add():
    form = forms.BinForm()
    if request.method == 'POST':
        post = { "name": form.name.data, "crop": form.crop.data, "size": form.size.data }
        bin_id = mongo.db.bins.insert(post)
        return redirect(url_for('bin', bin_id =  bin_id))
    else:
        return render_template('bin_add.html', form=form)

@app.route('/bin/edit/<bin_id>', methods=['GET', 'POST'])
def bin_edit(bin_id):
    form = forms.BinForm()
    if request.method == 'POST':
        post = { "_id": ObjectId(bin_id), "name": form.name.data, "crop": form.crop.data, "size": form.size.data }
        if mongo.db.bins.save(post):
            return redirect(url_for('bin', bin_id=  bin_id))
    else:
        bin = mongo.db.bins.find_one({ "_id": ObjectId(bin_id) })
        form.name.data = bin['name']
        form.size.data = bin['size']
        form.crop.data = bin['crop']
        return render_template('bin_edit.html', form=form)


# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
