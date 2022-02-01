#1.0.0
import json
from os.path import exists
import discum
import time
import urllib.request
import sys


UpdatePage = urllib.request.urlopen('https://raw.githubusercontent.com/Yarobonz/DiscordAutoTyper/main/AutoTyper.py')

FullUpdate=UpdatePage.read().decode("utf-8")

SelfPage = open(sys.argv[0], "r") 


def GetLine(resp, n):
    i = 1
    while i < n:
        resp.readline()
        i += 1
    return resp.readline()
    
CurrentVersion = GetLine(SelfPage, 1)
GithubVersion=GetLine(UpdatePage, 1).decode("utf-8") 
if(CurrentVersion!=GithubVersion):
	print("Updating")
	f = open(sys.argv[0], "w+")
	f.write(FullUpdate)
	f.close()
	exit(1)

DefualtConfig = \
    '''
{
  "Token": "TOKEN",
  "Message": "MESSAGE",
  "ChannelID": "ID",
  "Delay": 5
}
'''



if exists('Config.json'):
    with open('Config.json', 'r') as ConfigFile:
        ConfigData = ConfigFile.read()
    Config = json.loads(ConfigData)
    import requests

    headers = {'Authorization': Config['Token'],
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Optima 1315T 4G TT1108ML Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Safari/537.36',
               'Content-Type': 'application/json'}

    data = '{"content":"' + Config['Message'] + '"}'
    while True:
        response = \
            requests.post('https://discordapp.com/api/channels/920079912369553483/messages'
                          , headers=headers, data=data)
        print(f"Sent Message | "+Config['Message']+"")
        print(f"Waiting | "+str(Config['Delay'])+"")

        time.sleep(Config['Delay'])
else:

    print('Creating Config')
    f = open('Config.json', 'w+')
    f.write(DefualtConfig)
    f.close()
    print('Please Edit Config.json')
