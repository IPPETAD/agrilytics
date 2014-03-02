import csv
import pymongo
from pymongo import MongoClient

# Table 002-0043 . Farm product prices, crops and livestock
# http://data.gc.ca/data/en/dataset/666e5421-6909-4ce7-8777-a828b1ba3f95

# Multiply weight by 22.04623 for potatoes to get metric tonnes
# per metric tonne

# mongo troup.mongohq.com:10058/FarmSpot -u farmspot -pfarmspot



s_in = "Prices_002-0043.csv"

client = MongoClient('mongodb://farmspot:farmspot@troup.mongohq.com:10058/FarmSpot')
db = client.FarmSpot
with open(s_in) as fin:
        r = csv.reader(fin)
        for row in r:
            if not row[5] == '..' and not row[5] == '#VALUE':
                post = {"date": row[0],
                        "province": row[1],
                        "crop": row[2],
                        "vector": row[3],
                        "coordinate": row[4],
                        "value": row[5] }
                db.gov_prices.insert(post);
fin.close()
