from farm import app
from farm import forms
from functools import wraps
from flask import render_template, request, url_for, redirect, abort, jsonify, make_response, g
from flask_wtf.csrf import CsrfProtect
from xml.etree import ElementTree as emtree
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
import requests
import json
from datetime import date

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'

mongo = PyMongo(app)
csrf = CsrfProtect(app)

TORONTO_WEATHER_DATA = r'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=xml&stationID=30247&Year=2013&Month=3&Day=1&timeframe=2&submit=Download+Data'

SMOKY_LAKE_WEATHER_DATA = r'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=xml&stationID=32456&Year=2013&Month=3&Day=1&timeframe=2&submit=Download+Data'

def farmer_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        if g.user != 'farmer':
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return func

@app.before_request
def load_user():
    g.user = request.cookies.get('user')
    g.province = request.cookies.get('province')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fields')
@farmer_required
def fields():
    fields = list(mongo.db.fields.find({'province': g.province}))
    bins = list(mongo.db.bins.find({'province' : g.province}))
    harvests = list(mongo.db.harvests.find({'province': g.province}))
    weather_link = SMOKY_LAKE_WEATHER_DATA if g.province == 'Alberta' else TORONTO_WEATHER_DATA
    weather_xml = requests.get(weather_link)
    weather_xml.encoding = 'utf-8'
    today = date.today()
    root = emtree.fromstring(weather_xml.content)
    station_data = {}
    for child in root:
        if child.attrib.get('month') == str(today.month) and child.attrib.get('day') == str(today.day):
            station_data = child
            break
    max_temp = filter(lambda x: x.tag == "maxtemp", station_data)[0]
    min_temp = filter(lambda x: x.tag == "mintemp", station_data)[0]
    total_precip = filter(lambda x: x.tag == "totalprecipitation", station_data)[0]
    # Jacob was using these for harvests. Just copying his code.
    # What works in Rome... comes out of Rome when it's refactored? No.. that's not how it goes. Hmm
    field_ids = [ObjectId(h['section_from']['_id']) for h in harvests]
    bin_ids = [ObjectId(h['bin_to']) for h in harvests]
    hbins = list(mongo.db.bins.find({ '_id': { '$in': bin_ids } }))
    hfields = list(mongo.db.fields.find({ '_id':{ '$in': field_ids } }))

    for h in harvests:
        h['date'] = h['date'].strftime('%Y-%m-%d')
        for f in hfields:
            if str(f['_id']) == h['section_from']['_id']:
                h['field'] = f
                break
        for b in hbins:
            if  str(b['_id']) == h['bin_to']:
                h['bin'] = b
                break

    return render_template('fields.html', fields = fields, bins = bins, harvests = harvests, max_temp=max_temp,
                           min_temp=min_temp, total_precip=total_precip)

@app.route('/market')
def marketplace():
    crop = request.args.get("crop");
    page = request.args.get("page", 0, type=int);
    offer_count = mongo.db.offers.find({"crop": crop}).count()
    crop_types = list(mongo.db.crop_types.find())

    # TODO: Filter by user name, location
    edits = mongo.db.offers.find().count()

    offers = list(mongo.db.offers.find({"crop": crop, "province" : g.province }))
    offers += list(mongo.db.offers.find({"crop": crop, "province" : { "$ne" : g.province } }))
    print offers
    if page == 0:
        return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types, offer_count = offer_count, edits = edits)
    else:
        offers = offers[(page-1)*10:page*10]
        return render_template('marketplace.html', offers = offers, crop = crop, crop_types = crop_types, offer_count = offer_count, page = int(page), edits = edits)
    

@app.route('/market/new', methods=['GET', 'POST'])
@farmer_required
def marketplace_add():
    form = forms.OfferForm()
        
    if request.method == 'POST':
        post = { "province": g.province, "crop" : form.crop.data, "tonnes" : form.tonnes.data, "user" : form.user.data, "price" : form.price.data }
        post_id = mongo.db.offers.insert(post) 
        return redirect(url_for('marketplace'))
    else:
        crop_types = list(mongo.db.crop_types.find())
        choices = [(x['name'],x['label']) for x in crop_types]
        form.crop.choices = choices

        return render_template('marketplace_add.html', form=form, user = g)

@app.route('/market/user', methods=['GET', 'POST'])
@farmer_required
def marketplace_user():
    offers = mongo.db.offers.find({'province': g.province})
    crop_types = list(mongo.db.crop_types.find())
    return render_template('marketplace_user.html', offers = offers, crop_types = crop_types)    

@app.route('/marketplace/_delete/<offer_id>', methods=['DELETE'])
@farmer_required
def marketplace_delete(offer_id):
    if mongo.db.offers.remove({ "_id" : ObjectId(offer_id) }):
        return jsonify({ 'success': True })

@app.route('/field/add', methods=['GET', 'POST'])
@farmer_required
def field_add():
    form = forms.FieldForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = {"province": g.province, "name": form.name.data, "size": form.size.data, "geo": form.geo_data.data, "section": []}
            field_id = mongo.db.fields.insert(post)
            return redirect(url_for('.field', field_id=field_id))
    else:
        return render_template('field_add.html', form=form)


#@app.route('/field/<field_id>/')
#@farmer_required
#def field(field_id):
##    form = forms.DeleteForm()
 #   if request.method == 'POST':
 #       if mongo.db.fields.remove({'_id': ObjectId(field_id)}):
 ##           return redirect(url_for('fields'))
#    else:
#        field = mongo.db.fields.find_one({"_id": ObjectId(field_id) })
#        crops = []
#        for section in field['section']:
#            if section['crop'] not in crops:
#                crops.append(section['crop'].title())
#        return render_template('field.html', field = field, crops=crops, form=form)


@app.route('/field/<field_id>/edit', methods=['GET', 'POST'])
@farmer_required
def field_edit(field_id):
    form = forms.FieldForm()
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    if request.method == 'POST':
        if form.validate_on_submit():
            field['name'] = form.name.data
            field['size'] = form.size.data
            field['geo'] = form.geo_data.data
            field['province'] = g.province
            field_id = mongo.db.fields.save(field)
            return redirect(url_for('field', field_id=field_id))
    else:
        form.name.data = field['name']
        form.size.data = field['size']
        form.geo_data.data = field['geo']
        return render_template('field_edit.html', form=form, field_id=field_id)

@app.route('/field/<field_id>/', methods=['GET', 'POST'])
@farmer_required
def field(field_id):
    form_delete = forms.DeleteForm()
    form_field = forms.FieldForm()
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    crop_types = list(mongo.db.crop_types.find())
    form_field.name.data = field["name"]

    # Delete field
    if request.method == 'POST' and 'delete' in request.form.keys():
        if mongo.db.fields.remove({"_id": ObjectId(field_id)}):
            return redirect(url_for('fields'))
    # Save field
    if request.method == 'POST':
        if form_field.validate_on_submit():
            field['name'] = form_field.name.data
            field['size'] = form_field.size.data
            field['geo'] = form_field.geo_data.data
            field['province'] = g.province
            field_id = mongo.db.fields.save(field)
            return redirect(url_for('field', field_id=field_id))
    # Set field
    form_field.name.data = field['name']
    form_field.size.data = field['size']
    form_field.geo_data.data = field['geo']

    return render_template('field.html', field = field, form_field=form_field, form_delete=form_delete, crop_types=crop_types)


@app.route('/field/<field_id>/section/add', methods=['GET','POST'])
@farmer_required
def section_add(field_id):
    form = forms.SectionForm()

    crop_types = list(mongo.db.crop_types.find())
    choices = [(x['name'],x['label']) for x in crop_types]
    form.crop.choices = choices

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
@farmer_required
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
@farmer_required
def section_edit(field_id, index):
    form = forms.SectionForm()
    field = mongo.db.fields.find_one({'_id': ObjectId(field_id)})
    section = field['section'][int(index)]
    if request.method == 'POST':
        if form.validate_on_submit():
            section['name'] = form.name.data
            section['crop'] = form.crop.data
            section['acres'] = form.acres.data
            mongo.db.fields.save(field)
            return redirect(url_for('section', field_id=field_id, index=index))
    else:
        form.name.data = section['name']
        form.acres.data = section['acres']
        form.crop.data = section['crop']
        return render_template('section_edit.html', form=form, field_id=field_id, index=index)

@app.route('/bin/<bin_id>', methods=['GET', 'POST'])
@farmer_required
def bin(bin_id):
    form = forms.DeleteForm()
    if request.method == 'POST' and 'delete' in request.form.keys():
        if mongo.db.bins.remove({ "_id": ObjectId(bin_id) }):
            return redirect(url_for('fields'))

    bin = mongo.db.bins.find_one({"_id": ObjectId(bin_id) })
    return render_template('bin.html', bin = bin, form = form)

@app.route('/bin/add', methods=['GET', 'POST'])
@farmer_required
def bin_add():
    form = forms.BinForm()
    crop_types = list(mongo.db.crop_types.find())
    choices = [(x['name'],x['label']) for x in crop_types]
    form.crop.choices = choices
    
    if request.method == 'POST':
        post = {"province": g.province, "name": form.name.data, "crop": form.crop.data, "size": form.size.data }
        bin_id = mongo.db.bins.insert(post)
        return redirect(url_for('bin', bin_id =  bin_id))
    else:
        return render_template('bin_add.html', form=form)

@app.route('/bin/edit/<bin_id>', methods=['GET', 'POST'])
@farmer_required
def bin_edit(bin_id):
    form = forms.BinForm()
    if request.method == 'POST':
        post = {'province': province, "_id": ObjectId(bin_id), "name": form.name.data, "crop": form.crop.data, "size": form.size.data }
        if mongo.db.bins.save(post):
            return redirect(url_for('bin', bin_id=  bin_id))
    else:
        bin = mongo.db.bins.find_one({ "_id": ObjectId(bin_id) })
        form.name.data = bin['name']
        form.size.data = bin['size']
        form.crop.data = bin['crop']
        return render_template('bin_edit.html', form=form)

@app.route('/contract/', methods=['GET', 'POST'])
@farmer_required
def contracts():
    contracts = mongo.db.contracts.find({'province': g.province})
    crop_types = list(mongo.db.crop_types.find())
    if request.method == 'POST':
        print request.form.keys()
        json_str = json.loads(request.form['rows'])
        print json_str
        mongo.db.contracts.remove({'province': g.province})
        for row in json_str:
            post = {'crop': row.get('Crop'), 'company': row.get('Company'), 'tonnes': row.get('Tonnes'),
                    'fixed': row.get('Fixed'), 'pricepertonne': row.get('Price per Tonne'),
                    'value': row.get('Contract Value'), 'province': g.province}
            mongo.db.contracts.insert(post)
        return "Contracts Saved"
    return render_template('contracts.html', contracts=contracts, crop_types=crop_types)
    

@app.route('/contract/<contract_id>/', methods=['GET', 'POST'])
@farmer_required
def contract(contract_id):
    contract = mongo.db.contracts.find_one({"_id": ObjectId(contract_id)})
    form = forms.DeleteForm()
    if request.method == 'POST':
        if mongo.db.fields.remove({'_id': ObjectId(contract_id)}):
            return redirect(url_for('contracts'))
    else:
        return render_template('contract.html', contract=contract, form=form)

@app.route('/contract/add/', methods=['GET', 'POST'])
@farmer_required
def contract_add():
    form = forms.ContractForm()
    crop_types = list(mongo.db.crop_types.find())
    choices = [(x['name'],x['label']) for x in crop_types]
    form.crop.choices = choices
    if request.method == 'POST':
        print('Posted')
        if form.validate_on_submit():
            print('validated')
            post = {'province': g.province, 'crop': form.crop.data, 'company': form.company.data, 'tonnes': form.tonnes.data,
                    'fixed': form.fixed.data, 'price': form.price_per_tonne.data, 'value': form.contract_value.data}
            contract_id = mongo.db.contracts.insert(post)
            return redirect(url_for('contract', contract_id=contract_id))
        print(form.errors)
    else:
        return render_template('contract_add.html', form=form)

@app.route('/contract/<contract_id>/edit/', methods=['GET', 'POST'])
@farmer_required
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
	history = list ( mongo.db.gov_prices.find({"province": province, "crop": crop}, { "date": 1, "value": 1, "_id":0 }).sort("date", 1) )
	for month in history:
		month["month"] = month.pop("date")
		month["price"] = month.pop("value")
	return json.dumps(history)

	
@app.route('/history')
def history():
    crop = request.args.get("crop");
    page = request.args.get("page");
    crop_types = list(mongo.db.crop_types.find({"gov_label":{"$exists":"true"}}))
    provinces = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan"]
    return render_template('history.html', crop = crop, crop_types = crop_types, provinces = provinces)

@app.route('/harvest/add', methods=['GET', 'POST'])
@farmer_required
def harvest_add():
    form = forms.HarvestForm()
    fields = mongo.db.fields.find({'province': g.province})
    if request.method == 'POST':
        post = { 'section_from': json.loads(form.section_from.data), 'bin_to': form.bin_to.data, 'date': form.date.data, 'amount': form.amount.data , 'province': g.province }
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
@farmer_required
def harvest_update():
    field_id = json.loads(request.args.get('value'))['_id']
    field = list(mongo.db.fields.find({"_id": ObjectId(field_id)}))
    crop_type = field[0]['section'][0]['crop']

    bins = list(mongo.db.bins.find({'province': g.province, "crop" : crop_type}))
    for bin in bins:
        bin['_id'] = str(bin['_id'])
    
    return json.dumps(bins)
@app.route('/api/_marketprice')
def current_crop_price():
    crop_name = request.args.get('crop')
    crop_type = list(mongo.db.crop_types.find( { "name" : crop_name } ))[0]['gov_label']
    province = request.args.get('province')
    
    if province == '':
        gov_row = mongo.db.gov_prices.find({ "crop" : crop_type } ).sort( "date" , -1 ).limit(1)[0]
    else:
        gov_row = mongo.db.gov_prices.find({ "province" : province, "crop" : crop_type } ).sort( "date" , -1 ).limit(1)[0]
    gov_row['_id'] = str(gov_row['_id'])

    return json.dumps(gov_row)

@app.route('/login/')
def login():
    next = request.args.get("next");
    return render_template('login.html', next=next)

@app.route('/login/farmer_ab/')
def login_farmer_ab():
    next = request.args.get("next")
    if next:
        response = make_response(redirect(next))
    else:
        response = make_response(redirect(url_for('index')))
    print response
    response.set_cookie('user', 'farmer')
    response.set_cookie('province', 'Alberta')
    return response

@app.route('/login/farmer_on/')
def login_farmer_on():
    next = request.args.get("next")
    if next:
        response = make_response(redirect(next))
    else:
        response = make_response(redirect(url_for('index')))
    print response
    response.set_cookie('user', 'farmer')
    response.set_cookie('province', 'Ontario')
    return response

@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', '', expires=0)
    response.set_cookie('province', '', expires=0)
    return response

# For debugging, not production
app.secret_key = '\xe2t\xebJ\xb7\xf0r\xef\xe7\xe6\\\xf5_G\x0b\xd5B\x94\x815\xc1\xec\xda,'
