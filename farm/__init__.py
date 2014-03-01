import os
from flask import Flask

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot'




import farm.views