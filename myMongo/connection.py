from pymongo.mongo_client import MongoClient
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['roteiro']