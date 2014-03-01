import os
from flask import Flask

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'



from flask.ext.login import LoginManager
from flask.ext.browserid import BrowserID


from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo(app)


def get_user(browserid_response):
	email = browserid_response["email"]
	user = mongo.db.users.find_one({"email":email})
	if user:
		return user['_id']
	else: 
		return mongo.db.users.insert({"email":email})

def get_user_by_id(userid):
	user = mongo.db.users.find_one({"_id": ObjectId(userid) })
	return user
	

app = Flask(__name__)

login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)

browser_id = BrowserID()
browser_id.user_loader(get_user)
browser_id.init_app(app)



	
	
	
@login_manager.user_loader
def load_user(userid):
    return get_user(userid)
	
	





import farm.views