import requests


url = "http://62.3.58.53:51821"
session = requests.Session()


def getCookies():
    session.post(f'{url}/api/session', json={"password": "*****"})
    return session.cookies.get_dict()


def createPeer(wgID):
    cookies = getCookies()
    response = session.post(f'{url}/api/wireguard/client', cookies=cookies, json={"name": f"{wgID}"})
    return response.json()['name']


def deletePeer(wgID):
    cookies = getCookies()
    peersAllWG = session.get(f'{url}/api/wireguard/client', cookies=cookies).json()
    for peer in peersAllWG:
        if peer['name'] == wgID:
            peerID = peer['id']
            session.delete(f'{url}/api/wireguard/client/{peerID}', cookies=cookies)


def updatePeer(mongoID, state):
    cookies = getCookies()
    peersAllWG = session.get(f'{url}/api/wireguard/client', cookies=cookies).json()
    for peer in peersAllWG:
        if peer['name'] == mongoID:
            peerID = peer['id']
            session.post(f'{url}/api/wireguard/client/{peerID}/{state}', cookies=cookies)


def getFile(id):
    cookies = getCookies()
    peersAllWG = session.get(f'{url}/api/wireguard/client', cookies=cookies).json()
    for peerWG in peersAllWG:
        if peerWG['name'] == id:
            configId = peerWG['id']
            file = session.get(f'{url}api/wireguard/client/{configId}/configuration', cookies=cookies)
            return file.content
