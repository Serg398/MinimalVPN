from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from wireguard import createPeer, deletePeer
from syncUser import updateUserDB

date = datetime.datetime.now() + datetime.timedelta(days=31)
date_timestamp = int(round(date.timestamp()))


client = MongoClient('localhost', 27017)
db = client['bd']
users = db['users']
peers = db['peers']


def createUserDB(telegramID):
    user = list(users.find({"telegramID": telegramID}))
    if user == []:
        newUser = {
            "telegramID": telegramID,
            "state": True,
            "end_date": date_timestamp,
            "balance": 100
        }
        users.insert_one(newUser)


def createPeerDB(telegramID):
    user = list(users.find({"telegramID": telegramID}))
    peersAll = list(peers.find({"telegramID": telegramID}))
    if len(peersAll) > 1:
        return False
    else:
        newPeer = {
            "telegramID": telegramID,
            "state": user[0]["state"]
        }
        send = peers.insert_one(newPeer)
        createPeer(wgID=send.inserted_id)
        return send.inserted_id


def getUserPeersDB(telegramID):
    peersAll = list(peers.find({"telegramID": telegramID}))
    return peersAll


def updateBalanceDB(telegramID, summ):
    userBD = list(users.find({"telegramID": telegramID}))
    balance = userBD[0]['balance']
    users.update_one({"telegramID": telegramID}, {"$set": {'balance': balance + summ}})
    updateUserDB(telegramID=telegramID)


def deletePeerDB(mongoID):
    peers.delete_one({'_id': ObjectId(mongoID)})
    deletePeer(wgID=mongoID)

