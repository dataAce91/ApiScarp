import requests 
from bs4 import BeautifulSoup
import pymongo
MomngoDB = "<db ENDPOINT>"
DBname = "DB Name"
collection="CollectionName"
#headers =  {"Content-Type":"application/json"}


def getGroups():
    url = 'https://attack.mitre.org/groups/'
    response = requests.get(url)
    htmldata = response.content
    soup = BeautifulSoup(htmldata, 'html.parser')
    data = []
    datax = soup.find("table",{"class":"table table-bordered table-alternate mt-2"})
    #rows = datax[0].find('tr')
    for link in datax.find_all('tr')[1:] :
        data.append(link.find('td').find('a').get('href'))
    return data
def gettechniqueIDs(datax):
    data=[]
    x= datax.find_all('tr')
    if x :
        for link in x[1:]:
            cells = link.findAll("td")
            tid = cells[1].text
            data.append(tid.replace("\n", ""))
    return data

def getGroupinfos(path):
    url ="https://attack.mitre.org%s"%(path)
    response = requests.get(url)
    htmldata = response.content
    soup = BeautifulSoup(htmldata, 'html.parser')
    print ("calling URL %s"%(url))
    datax = soup.find("h1")
    data ={
        "name": datax.text.replace("\n", "").strip(),
        "id":path.replace("/groups/",""),
        "description":soup.find("div",{"class":"description-body"}).find("p").text, 
    } 
    tidtable = soup.find("table",{"class":"table techniques-used background table-bordered"})
    if tidtable:
        data.update({
        "techniqueIDs":gettechniqueIDs(tidtable)
        })
    return data 


def PushToDB(data):
    mongoclient = pymongo.MongoClient(MomngoDB)
    Db = mongoclient[DBname]
    Dbcol = Db[collection]
    Dbcol.insert_many(data)

groups = getGroups()

data = []
for i in groups:
    grupinfos = getGroupinfos(i)
    data.append(grupinfos)
PushToDB(data)
