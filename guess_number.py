from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import random

import tg_token

'''
Игра "Угадай число"
'''


#  инициируем бота и диспетчера
bot = Bot(tg_token.TOKEN)
dp = Dispatcher()

#  попытки доступные пользователю по умолчанию
ATTEMPTS = 5

#  данные о текущем пользователе
user_data = {'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0}


#  генерация случайного числа для игры
def get_random_number() -> int:
    return random.randint(1, 100)


#  хэндлер обрабатывает старт бота
@dp.message(CommandStart())
async def process_start(message: Message):
    await message.answer(
        'Привет\nДавай сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных команд'
        ' - отправьте команду /help'
    )


#  хэндлер высвечивает подсказку по help
@dp.message(Command('help'))
async def command_help(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


#  хэндлер будет срабатывать на команду stat
@dp.message(Command('stat'))
async def command_stat(message: Message):
    await message.answer(
        f'Всего игр сыграно: {user_data["total_games"]}\n'
        f'Игр выиграно: {user_data["wins"]}\n'
        f'Проиграно: {user_data["total_games"] - user_data["wins"]}'
    )


#  хэндлер обработки команды cancel
@dp.message(Command('cancel'))
async def command_cancel(message: Message):
    if user_data['in_game']:
        user_data['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом.'
        )

    else:
        await message.answer(
            'Мы и так не играем.'
            'Есть желание сыграть?'
        )


#  хэндлер обработки согласия на игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем',
                                'игра', 'хочу сыграть']))
async def pos_answer(message: Message):
    if not user_data['in_game']:
        user_data['in_game'] = True
        user_data['secret_number'] = get_random_number()
        user_data['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )

    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


#  хэндлер обработки чисел, отправляемых пользователем
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def number_answer(message: Message):
    if user_data['in_game']:
        if int(message.text) == user_data['secret_number']:
            user_data['in_game'] = False
            user_data['total_games'] += 1
            user_data['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user_data['secret_number']:
            user_data['attempts'] -= 1
            await message.answer('Мое число меньше')
            await message.answer(f'У вас осталось {user_data['attempts']} попыток')
        elif int(message.text) < user_data['secret_number']:
            user_data['attempts'] -= 1
            await message.answer('Мое число больше')
            await message.answer(f'У вас осталось {user_data['attempts']} попыток')
        if user_data['attempts'] == 0:
            user_data['in_game'] = False
            user_data['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user_data["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )

    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


#  хэндлер обработки любых сообщений
@dp.message()
async def any_message(message: Message):
    if user_data['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )

    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    print('Бот запущен')
    dp.run_polling(bot)
