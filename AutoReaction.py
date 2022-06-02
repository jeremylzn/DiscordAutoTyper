import requests
import emoji


def add_reaction(emoji):
    headers = {'Authorization': 'OTczNTE1NjIxNDUzMTM1ODg0.GKPVMN.iFBZGDqe6VkJDVlckRAwyTLLSGnuH7fZIjggJM',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Optima 1315T 4G TT1108ML Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Safari/537.36',
               'Content-Type': 'application/json'}
    r = requests.put(f'https://discord.com/api/channels/976177683207708709/messages/981818755845857350/reactions/{emoji}/%40me', headers=headers)

    print(r.content)

add_reaction(emoji.emojize(':thumbs_up:'))