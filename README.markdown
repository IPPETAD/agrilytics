FarmSpot
========

Farming management services. Track profitability, monitor field rainfall, bid on the Crop Marketplace, and so much more..

FarmSpot is a cloud service like no other. Using live data, geolocation services, and open federal data, the sky is the limit. You can use easily manage your farm operations on the field or at the office using our mobile-friendly implementations, or connect with farmers and brokers through our intuitive marketplace.

![FarmSpot](https://raw.github.com/IPPETAD/agrilytics/master/farm/static/field.jpg)

## Description

Field Management

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


## Contracts

Manage your contracts and finances! This convenient spreadsheet allows simplified cataloguing of your existing contracts and how they're set. These columns were gathered from real farm elicitations. Add rows, remove rows, then save and share!

##Analytics

Using open government data, view past and current market trends. These dynamic graphs provide effective visualizations filtered by produce and province.


##French Language

We have French translations for everything!
Except the README. We're sort of writing this last minute.

## Initial installation

	git clone git@github.com:IPPETAD/agrilytics.git
	cd farmspot

	virtualenv venv
	source venv/bin/activate

	pip install -r requirements.txt
	python runserver.py



