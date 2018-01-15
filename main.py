from flask import Flask, render_template, request
from steam.guard import SteamAuthenticator
import json
import bna
import requests

app = Flask(__name__,instance_relative_config=True)

app.config.from_pyfile('config.py')
global BANbean
BANbean = None

def removeSymbol(inString):
    return inString.replace("-", "")

def getSteamKey():
    mnjson = app.config['STEAM_KEY']
    mjson = json.loads(mnjson)
    authbean = SteamAuthenticator(mjson)
    steamcode = authbean.get_code()
    return steamcode

def InitBNA():
    global BANbean
    if BANbean == None:
        serial =  app.config['BNA_SERIAL']
        restorecode =app.config['BNA_RESTORECODE']
        BANbean = bna.restore(serial,restorecode)
    return BANbean

def getBNAkey():
    bean = InitBNA()
    return bna.get_token(bean)

@app.route('/getOnekey' ,methods =['GET'])
def onekeyAccept():
    bnakey,nextTime = getBNAkey()
    url = 'https://www.battlenet.com.cn/login/authenticator/pba?serial=%s&code=%08d'%(
        removeSymbol(app.config['BNA_SERIAL']),
        bnakey)
    cookies = getCookie()
    headers = {'Cookie':cookies}  
    r = requests.get(url,headers=headers)
    if(r.status_code==200):
        print(r.status_code)
        return r.text
    else:
        pass

def getCookie():
    bnakey,nextTime = getBNAkey()
    url = 'https://www.battlenet.com.cn/login/authenticator/pba?serial=%s&code=%08d'%(
        removeSymbol(app.config['BNA_SERIAL']),
        bnakey)
    resp = requests.get(url)
    g_cookie = resp.headers['set-cookie']
    return g_cookie
    
@app.route('/AcceptBattleNetLogin' ,methods =['GET'])
def Accept():
    bnakey,nextTime = getBNAkey()
    reqid = request.args.get('requestId')
    url = 'https://www.battlenet.com.cn/login/authenticator/pba?serial=%s&requestId=%s&code=%08d&accept=true'%(
        removeSymbol(app.config['BNA_SERIAL']),
        reqid,
        bnakey)
    r = requests.post(url)
    if(r.status_code==200):
        print(r.status_code)
        return r.text
    else:
        pass

@app.route('/getkey' ,methods =['GET'])
def err():
    return "methods != post"
@app.route('/getkey' ,methods=['POST'])
def showcode():
    steameky = getSteamKey()
    bnakey,nextTime = getBNAkey()
    return "<h2>Steam:&nbsp&nbsp%s</h2> <h2>Battle.net:&nbsp&nbsp%08d</h2> <p id='time'>Time:%s</p>"%(steameky,bnakey,nextTime)

@app.route('/')
def hello():
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')