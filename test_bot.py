from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import time

import json
import requests
#  для запроса ссылки на картинку
import tg_token as tok
import weather as w


#  инициализация бота и диспетчера
bot = Bot(token=tok.TOKEN)
dp = Dispatcher()


#  обработка команды /start при запуске бота или ручном вводе команды в бот
async def start_command(message: Message):
    await message.answer(
        'Привет\nМеня зовут Марсек '
        '- я бот!\nНапиши мне что нибудь...'
        )


#  хэндлер обработки команды /help
async def help_command(message: Message):
    await message.answer(
        'сообщение с подсказкой'
        )


#  хэндлер отправки рандомной пикчи с собаками по команде /dog
async def send_dog(message: Message):
    image_response = requests.get('https://random.dog/woof.json').json()
    image = image_response['url']
    await message.answer_photo(photo=image)


async def send_piza(message: Message):
    gotovim = 'https://sun6-21.userapi.com/impg/B50N47WBDqHoeLJxxC0EdGriePv1F0iyZRVedw/_2S3EhrjouI.jpg?size=1280x954&quality=96&sign=17d1f08a47481b2f059e9d65420720e8&c_uniq_tag=KrFFKdZWnVPSx6tZ4W1s9ALFNa2Tk9Vc5LkyixCV0UI&type=album'
    piza = 'https://sun9-53.userapi.com/impf/WVkxqJdoFwn1YSleLs4PXM8WA6IopsaGhGJjYQ/g7FvT6vQYyw.jpg?size=640x800&quality=96&sign=41e235670272a803abe138255128ab40&c_uniq_tag=QSL5K5xjRii4k4GgoV153TpUqw5SGE_RtZJ4OuGkiEo&type=none'
    await message.answer_photo(photo=gotovim)
    await message.answer('Начали готовить пицу...')
    time.sleep(10)
    await message.answer_photo(photo=piza)
    await message.answer('Получите вашу ебейшую пицу...')


async def weather_command(message: Message):
    await message.answer('Что бы узнать текущую погоду, пришлите свою геолокацию.')


#  отправка текущей погоды по принятой геолокации
async def send_weather(message: Message):
    data = json.loads(message.json())
    print(json.dumps(data, indent=4))
    lat, lon = data['location']['latitude'], data['location']['longitude']
    weather = w._parse_weather(w.get_weather_forecast(lat, lon))
    await message.answer("Получаю информацию с ближайшей метеостанции...")
    await message.answer(
        f'Локация: {weather.city}\n'
        f'Температура за бортом: {weather.temp} градусов\n'
        f'Ощущается как: {weather.feels_temp} градусов\n'
        f'На небе: {weather.weather_type}\n'
        f'{weather.wind_dir} ветер со скоростью {weather.wind_mps} метров в секунду\n'
    )
    await message.answer_photo(photo=weather.icon)


#  регистрация хэндлеров
dp.message.register(start_command, Command('start'))
dp.message.register(help_command, Command('help'))
dp.message.register(send_dog, Command('dog'))
dp.message.register(send_piza, Command('piza'))
dp.message.register(weather_command, Command('weather'))
dp.message.register(send_weather, F.location)


@dp.message()
async def copy_messsage(message: Message):
    try:
        #print(message.model_dump_json(indent=4, exclude_none=True))
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип не поддерживается')


if __name__ == '__main__':
    dp.run_polling(bot)
