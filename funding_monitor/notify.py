import requests
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_msg(msg, token=TOKEN, chat_id=CHAT_ID):
    q = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}'.format(
        token=token,
        chat_id=chat_id,
        msg=str(msg),
    )
    requests.get(q)
