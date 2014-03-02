FarmSpot
========

Farming management services. Track profitability, monitor field rainfall, bid on the Crop Marketplace, and so much more.

Available to test [on Heroku](http://farmspot.herokuapp.com).

![FarmSpot](https://raw.github.com/IPPETAD/agrilytics/master/farm/static/field.jpg)
![Add Farm](http://i.imgur.com/QTvmqYx.png)
![Marketplace](http://i.imgur.com/e5ENZdu.png)
![Contracts](http://i.imgur.com/ZWIL3W3.png)
![French Analytics](http://i.imgur.com/4foidbH.png)

FarmSpot is a cloud service like no other. Using live data, geolocation services, and open federal data, the sky is the limit. You can use easily manage your farm operations on the field or at the office using our mobile-friendly implementations, or connect with farmers and brokers through our intuitive marketplace.

(This project was written in 48 hours for the [Canadian Open Data Experience](http://canadianopendataexperience.com).)

## Open Data Used

* [Farm product prices, crops, and livestock](http://data.gc.ca/data/en/dataset/666e5421-6909-4ce7-8777-a828b1ba3f95)
* [Historical climate records](http://climate.weather.gc.ca)

## Description

### Field Management

Manage your fields, bins, and harvests! Add a field by specify the geolocation of your farm, create bins to store and manage your existing produce. Track your harvests through our easy-to-use interface!

Open data is used to track temperature and rain fall data on your fields! Wow, that's pretty cool!

### MarketPlace

The marketplace provides a public crop listing service to find buyers and sellers for your produce. It has functionality to manage your own postings, as well as to search for listings across Canada.

Open data is used in this section for current market prices!

#### Post Listing

You can post your own listing to the MarketPlace. Specify your crop, amount in tonnes, and expected price. 
The market price for the crop is pulled from national data (and queried to your province) to recommend prices for your quantity. On posting, your listing will be populated with your location and relevant information. It's really that easy!

#### Your Listings

Through this page, you can manage your existing listings. There are existing listings for your viewing. Any items you add or remove will update the listings.

#### Search Listings

You can search public listings by crop type. Listing information is provided, and the items are filtered such that your province is displayed first to help you find nearby farms. You can then contact the provider. This helps brokers and farmers connect.


### Contracts

Manage your contracts and finances! This convenient spreadsheet allows simplified cataloguing of your existing contracts and how they're set. These columns were gathered from real farm elicitations. Add rows, remove rows, then save and share!

### Analytics

Using open government data, view past and current market trends. These dynamic graphs provide effective visualizations filtered by produce and province.


### French Language

We have French translations for everything!
Except the README. We're sort of writing this last minute.


## Tech Stack

* Database: [MongoDB](http://www.mongodb.org)
* Back-end web: [Python](https://www.python.org) with modules in [requirements.txt](requirements.txt), including:
 * [Flask](http://flask.pocoo.org) web framework
 * [WTForms](http://wtforms.readthedocs.org) for form handling
 * [Babel](http://babel.pocoo.org) for 
* Front-end web: 
 * [Bootstrap](http://getbootstrap.com) based CSS theme
 * [D3.js](http://d3js.org) for interactive visualizations
 * [jQuery](http://jquery.com) to make JavaScript easier
 * [Leaflet](http://leafletjs.com) to make pretty maps

## Initial installation

	git clone git@github.com:IPPETAD/agrilytics.git
	cd agrilytics

	virtualenv venv
	source venv/bin/activate
	
	mongorestore sample_database

	pip install -r requirements.txt
	python runserver.py



