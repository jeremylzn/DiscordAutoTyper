# #1.0.0
# import json
# from os.path import exists
# import discum
# import time
# import urllib.request
# import sys


# UpdatePage = urllib.request.urlopen('https://raw.githubusercontent.com/Yarobonz/DiscordAutoTyper/main/AutoTyper.py')

# FullUpdate=UpdatePage.read().decode("utf-8")

# SelfPage = open(sys.argv[0], "r") 


# def GetLine(resp, n):
#     i = 1
#     while i < n:
#         resp.readline()
#         i += 1
#     return resp.readline()
    


# CurrentVersion = GetLine(SelfPage, 1).replace("\n","")
# GithubVersion=FullUpdate.partition('\n')[0].replace("\n","")

# if(CurrentVersion!=GithubVersion):
# 	print("Updating")
# 	f = open(sys.argv[0], "w+")
# 	f.write(FullUpdate)
# 	f.close()
# 	exit(1)

# DefualtConfig = \
#     '''
# {
#   "Token": "OTczNTEzNDg2NDU1OTQzMjA4.G7p2KU.lSQfghscE31LOwRz84G5gf0D9lol2jrzCTWoAs",
#   "Message": "Salut",
#   "ChannelID": "976177683207708709",
#   "Delay": 5
# }
# '''



# if exists('Config.json'):
#     with open('Config.json', 'r') as ConfigFile:
#         ConfigData = ConfigFile.read()
#     Config = json.loads(ConfigData)
#     import requests

#     headers = {'Authorization': Config['Token'],
#                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Optima 1315T 4G TT1108ML Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Safari/537.36',
#                'Content-Type': 'multipart/form-data'}

#                             #   'Content-Type': 'application/json'}


#     data = '{"content":"' + Config['Message'] + '"}'

#     # File
#     files = {
#         "file" : ("./image_test.jpeg", open("./image_test.jpeg", 'rb')), # The picture that we want to send in binary
#     }

#     while True:
#         response = \
#             requests.post('https://discordapp.com/api/channels/' + Config['ChannelID'] + '/messages'
#                           , headers=headers, data=data, files=files)
#         print(f"Sent Message | "+Config['Message']+"")
#         print(f"Waiting | "+str(Config['Delay'])+"")

#         print(response.content)
#         time.sleep(Config['Delay'])
# else:

#     print('Creating Config')
#     f = open('Config.json', 'w+')
#     f.write(DefualtConfig)
#     f.close()
#     print('Please Edit Config.json')

import requests

# User's Token
# header = {
    # 'Authorization': "OTczNTE1NjIxNDUzMTM1ODg0.GKPVMN.iFBZGDqe6VkJDVlckRAwyTLLSGnuH7fZIjggJM",
    # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Optima 1315T 4G TT1108ML Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Safari/537.36',
    # 'Content-Type': 'multipart/form-data'}

header = { 'Authorization': "OTczNTE1NjIxNDUzMTM1ODg0.GKPVMN.iFBZGDqe6VkJDVlckRAwyTLLSGnuH7fZIjggJM"}

# File
files = {
    "file" : ("./picture.jpg", open("./picture.jpg", 'rb')) # The picture that we want to send in binary
}

# Optional message to send with the picture
payload = {
    "content":""
}

channel_id = "976177683207708709" # Channel where we send the picture

r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header, files=files)
print(r.content)