#SCrap Data 

import requests
import pymongo
MomngoDB = "<db ENDPOINT>"
DBname = "DB Name"
collection="CollectionName"


def ReadData():
    URL = "https://haveibeenpwned.com/api/v3/breaches"
    headers =  {"Content-Type":"application/json"}
    response = requests.get(URL,headers=headers,verify=False)
    if response.status_code ==200:
        data = response.json()
    else:
        print("Something went Wrong HTTP STAUS CODE Returned : %s"%(response.status_code))
        data = []
        
    return data 
def PushToDB(data):
    mongoclient = pymongo.MongoClient(MomngoDB)
    Db = mongoclient[DBname]
    Dbcol = Db[collection]
    Dbcol.insert_many(data)

data = ReadData()
if data:
    PushToDB(data)
else:
    print("No data to Insert")


