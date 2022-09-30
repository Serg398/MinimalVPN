from pymongo import MongoClient
import datetime
from wireguard import updatePeer
import telebot


API_TOKEN = '5653584102:AAFRDX9fQu2tO13ZpnhI6Z3LVxwj4d_mEhk'
bot = telebot.TeleBot(API_TOKEN)

money = 100
date = datetime.datetime.now() + datetime.timedelta(days=31)
date_timestamp = int(round(date.timestamp()))


client = MongoClient('localhost', 27017)
db = client['bd']
users = db['users']
peers = db['peers']


def updatePeerDB(telegramID):
    peersBD = list(peers.find({"telegramID": telegramID}))
    for peer in peersBD:
        if peer['state'] == True:
            updatePeer(mongoID=str(peer['_id']), state='enable')
        if peer['state'] == False:
            updatePeer(mongoID=str(peer['_id']), state='disable')


def updateUserDB(telegramID):
    userBD = list(users.find({"telegramID": telegramID}))
    if userBD[0]['end_date'] < int(round(datetime.datetime.now().timestamp())):
        if userBD[0]['balance'] >= money:
            users.update_one({"telegramID": telegramID}, {"$set": {'state': True, 'balance': userBD[0]['balance'] - money, "end_date": date_timestamp}})
            peers.update_many({"telegramID": telegramID}, {"$set": {'state': True}})
            print('Продлен')
        else:
            users.update_one({"telegramID": telegramID}, {"$set": {'state': False}})
            peers.update_many({"telegramID": telegramID}, {"$set": {'state': False}})
            print('Нет средств')

    updatePeerDB(telegramID=telegramID)
