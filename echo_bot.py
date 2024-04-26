from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
import tg_token as tok


BOT_TOKEN = tok.TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


#  обработка команды /start при запуске бота или ручном вводе команды в бот
@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        'Привет\nМеня зовут Марсек '
        '- я бот!\nНапиши мне что нибудь...'
        )


#  хэндлер обработки команды /help
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        'Я - эхо-бот! Отправь мне сообщение' 
        'и я в ответ продублирую его'
        )


@dp.message(Command('dog'))
async def send_dog(message: Message):
    image_response = requests.get('https://random.dog/woof.json').json()
    image = image_response['url']
    await message.answer_photo(photo=image)


#  обработка любых сообщений кроме start и help
@dp.message()
async def echo_message(message: Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
