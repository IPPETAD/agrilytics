from farm import app
from farm import forms
from flask import render_template, request, url_for, redirect, abort, jsonify, make_response, g
from flask_wtf.csrf import CsrfProtect

from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

import json
from datetime import date

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'

mongo = PyMongo(app)
csrf = CsrfProtect(app)

@app.before_request
def load_user():
    g.user = request.cookies.get('user')


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
    form = forms.DeleteForm()
    if request.method == 'POST':
        if mongo.db.fields.remove({'_id': ObjectId(field_id)}):
            return redirect(url_for('fields'))
    else:
        field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
        crops = []
        for section in field['section']:
            if section['crop'] not in crops:
                crops.append(section['crop'].title())
        return render_template('field.html', field = field, crops=crops, form=form)

@app.route('/market')
def marketplace():
    crop = request.args.get("crop");
    page = request.args.get("page");
    offer_count = mongo.db.offers.count()
    crop_types = list(mongo.db.crop_types.find())

    # TODO: Filter by user name
    edits = mongo.db.offers.count()

    if page is None:
        offers = list(mongo.db.offers.find({"crop": crop}))
        return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types, offer_count = offer_count, edits = edits)
    else:
        offers = list(mongo.db.offers.find({"crop": crop}).limit(10).skip(10*(int(page)-1)))
        return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types, offer_count = offer_count, page = int(page), edits = edits)
    

@app.route('/market/new', methods=['GET', 'POST'])
def marketplace_add():
    form = forms.OfferForm()
        
    if request.method == 'POST':
        post = { "crop" : form.crop.data, "tonnes" : form.tonnes.data, "user" : form.user.data, "price" : form.price.data }
        post_id = mongo.db.offers.insert(post) 
        return redirect(url_for('marketplace'))
    else:
        crop_types = list(mongo.db.crop_types.find())
        choices = [(x['name'],x['label']) for x in crop_types]
        form.crop.choices = choices

        return render_template('marketplace_add.html', form=form)

@app.route('/market/user', methods=['GET', 'POST'])
def marketplace_user():
    offers = mongo.db.offers.find()
    crop_types = list(mongo.db.crop_types.find())
    return render_template('marketplace_user.html', offers = offers, crop_types = crop_types)    

@app.route('/marketplace/_delete/<offer_id>', methods=['DELETE'])
def marketplace_delete(offer_id):
    if mongo.db.offers.remove({ "_id" : ObjectId(offer_id) }):
        return jsonify({ 'success': True })

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
        return render_template('field_edit.html', form=form, field_id=field_id)

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

@app.route('/field/<field_id>/section/<index>/')
def section(field_id, index):
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    form = forms.DeleteForm()
    section = field['section'][int(index)]
    if request.method == 'POST':
        form['section'].remove(section)
        mongo.db.fields.save(form)
        return redirect(url_for('field', field_id=field_id))
    else:
        return render_template('section.html', field=field, section=section, form=form)

@app.route('/field/<field_id>/section/<index>/edit', methods=['GET', 'POST'])
def section_edit(field_id, index):
    form = forms.SectionForm()
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    section = field['section'][index]
    if request.method == 'POST':
        if form.validate_on_submit():
            section['name'] = form.name.data
            section['crop'] = form.crop.data
            section['acres'] = form.acres.data
            mongo.db.fields.save(field)
            return redirect(url_for('section', field_id=field_id, name=name))
    else:
        form.name.data = section['name']
        form.acres.data = section['acres']
        form.crop.data = section['crop']
        return render_template('section_edit.html', form=form, field_id=field_id, name=name)

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

@app.route('/contract/')
def contracts():
    contracts = mongo.db.contracts.find()
    return render_template('contracts.html', contracts=contracts)
    

@app.route('/contract/<contract_id>/', methods=['GET', 'POST'])
def contract(contract_id):
    contract = mongo.db.contracts.find_one({"_id": ObjectId(contract_id)})
    form = forms.DeleteForm()
    if request.method == 'POST':
        if mongo.db.fields.remove({'_id': ObjectId(contract_id)}):
            return redirect(url_for('contracts'))
    else:
        return render_template('contract.html', contract=contract, form=form)

@app.route('/contract/add/', methods=['GET', 'POST'])
def contract_add():
    form = forms.ContractForm()
    crop_types = list(mongo.db.crop_types.find())
    choices = [(x['name'],x['label']) for x in crop_types]
    form.crop.choices = choices
    if request.method == 'POST':
        print('Posted')
        if form.validate_on_submit():
            print('validated')
            post = {'crop': form.crop.data, 'company': form.company.data, 'tonnes': form.tonnes.data,
                    'fixed': form.fixed.data, 'price': form.price_per_tonne.data, 'value': form.contract_value.data}
            contract_id = mongo.db.contracts.insert(post)
            return redirect(url_for('contract', contract_id=contract_id))
        print(form.errors)
    else:
        return render_template('contract_add.html', form=form)

@app.route('/contract/<contract_id>/edit/', methods=['GET', 'POST'])
def contract_edit(contract_id):
    form = forms.ContractForm()
    contract = mongo.db.contracts.find_one({'_id': ObjectId(contract_id)})
    print(contract)
    crop_types = list(mongo.db.crop_types.find())
    choices = [(x['name'],x['label']) for x in crop_types]
    form.crop.choices = choices
    if request.method == 'POST':
        if form.validate_on_submit():
            contract['crop'] = form.crop.data
            contract['company'] = form.company.data
            contract['tonnes'] = form.tonnes.data
            contract['fixed'] = form.fixed.data
            contract['price'] = form.price_per_tonne.data
            contract['value'] = form.contract_value.data
            mongo.db.contracts.save(contract)
            return redirect(url_for('contract', contract_id=contract_id))
    else:
        form.crop.data = contract['crop']
        form.company.data = contract['company']
        form.tonnes.data = contract['tonnes']
        form.fixed.data = contract['fixed']
        form.price_per_tonne.data = contract['price']
        form.contract_value.data = contract['value']
        return render_template('contract_edit.html', form=form)

@app.route('/market/price_history')
def price_history():
	province = request.args["province"]
	crop = request.args["crop"]
	history = []
	history = list ( mongo.db.gov_prices.find({"province": province, "crop": crop}, { "date": 1, "value": 1, "_id":0 }) )
	for month in history:
		month["month"] = month.pop("date")
		month["price"] = month.pop("value")
	return json.dumps(history)

@app.route('/harvests')
def harvests():
    harvests = list(mongo.db.harvests.find())
    bin_ids = [ObjectId(h['bin_to']) for h in harvests]
    bins = list(mongo.db.bins.find({ '_id': { '$in': bin_ids } }))
    field_ids = [ObjectId(h['section_from']['_id']) for h in harvests]
    fields = list(mongo.db.fields.find({ '_id':{ '$in': field_ids } }))
    
    for h in harvests:
        h['date'] = h['date'].strftime('%Y-%m-%d')
        for f in fields:
            if str(f['_id']) == h['section_from']['_id']:
                h['field'] = f
                break
        for b in bins:
            if  str(b['_id']) == h['bin_to']:
                h['bin'] = b
                break

    return render_template('harvests.html', harvests = harvests)

@app.route('/harvest/add', methods=['GET', 'POST'])
def harvest_add():
    form = forms.HarvestForm()
    if request.method == 'POST':
        post = { 'section_from': json.loads(form.section_from.data), 'bin_to': form.bin_to.data, 'date': form.date.data, 'amount': form.amount.data }
        harvest_id = mongo.db.harvests.insert(post)
        return redirect(url_for('bin', bin_id = form.bin_to.data))
    
    form.date.data = date.today()
    fields = mongo.db.fields.find()
    field_choices = [(-1, 'Choose one...')]
    for f in fields:
        field_choices.append((f['name'], [(json.dumps({ 'i': i, '_id': str(f['_id']) }), s['name']) for i,s in enumerate(f['section'])]))

    form.section_from.choices = field_choices
    return render_template('harvest_add.html', form=form)

@app.route('/harvest/inc')
def harvest_update():
    """Add two numbers server side, ridiculous but well..."""
    field_id = json.loads(request.args.get('value'))['_id']
    field = list(mongo.db.fields.find({"_id": ObjectId(field_id)}))
    crop_type = field[0]['section'][0]['crop']

    bins = list(mongo.db.bins.find({"crop" : crop_type}))
    for bin in bins:
        bin['_id'] = str(bin['_id'])
    
    return json.dumps(bins)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/login/farmer/')
def login_farmer():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', 'farmer')
    return response

@app.route('/login/buyer/')
def login_buyer():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', 'buyer')
    return response

@app.route('/login/anon/')
def login_anon():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', 'anon')
    return response

@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', '', expires=0)
    return response

# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
