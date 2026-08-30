## THIS WAS DIRECTLY COPIED FROM MONGO-DB
from pymongo import MongoClient

uri = "mongodb+srv://<TYPE_USERNAME_HERE>:<ADD_PASSWORD_HERE>@cluster0.jaqx1un.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
