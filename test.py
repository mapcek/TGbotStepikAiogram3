import requests
import time
import tg_token

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = tg_token.TOKEN
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)
    #  чтоб видеть в консоли что код жив
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    #  запрашиваем апдейт от сервера

    if updates['result']:
    #  если апдейт пришел, то парсим его на информацию
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            image_response = requests.get('https://random.dog/woof.json').json()
            image = image_response['url']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={image}')

    time.sleep(1)
    counter += 1
    