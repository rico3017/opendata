import os

basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = "testkey"

apis = {
        "property_url" : "http://landregistry.data.gov.uk/data/ppi/transaction-record.json",
        "ttl" : "https://api.tfl.gov.uk", 
        "postcode" : "https://postcodes.io",
        "police" : "https://data.police.uk/api"
}

page_size = 50

db = {"host":"127.0.0.1",
        "user":"root",
        "password":'root',
        "port":3306 ,
        "database":"open_data",
        "charset":"utf8"
        }

db_option = {"pool_size": 5,
            "max_overflow" : 0}

app_id = "09f9e340"
app_key = "a83a636c5c84d773ea7ccb2ad3d3addb"


del os
