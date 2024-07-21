from pymongo import MongoClient
import gridfs

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['receitas_db']
fs = gridfs.GridFS(db)
