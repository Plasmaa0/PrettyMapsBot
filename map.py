import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

import keyboard

import matplotlib.pyplot as plt
import prettymaps
import time
import random
import datetime

API_TOKEN = '5776852478:AAGmV-7refAgBdv7KH7-3jLjmphatpB7bZ4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


user_preset = {}
user_frame = {}
user_radius = {}
default_settings = {'barcelona', True, 1100}


# Сделать кнопки для выбора пресета
# Сделать возможность вводить координаты и радиус
# Сделать ответ на неожиданное поведение
# Сделать выбор рамочки


@dp.message_handler(commands=['start'])
async def sendhelp(message: types.Message):
    await message.answer(
        'Привет! Этот бот использует библиотеку prettymaps.\n'
        'Ты можешь отправить координаты или название местности через запятую на английском.'
        'получить приятную картиночку этого места!\n\n'
        'Команды: \n'
        '/start         - приветственное сообщение \n'
        '/configure_map - настроить и сгенерировать карту \n'
        '/preset        - выбрать пресет \n'
        '/radius        - выбрать радиус \n'
        '/map           - быстрая генерация карты с дефолтными и/или сохраненными настройками'
        '/frame         - выбрать рамку \n\n'
        'prettymaps lib: https://github.com/marceloprates/prettymaps')


@dp.message_handler(commands=['drawmap'])
async def draw_map(message: types.Message):
    await message.answer("Вы можете ответить на сообщения, чтобы настроить следующие параметры.")
    await message.reply("Выберите пресет", reply_markup=keyboard.SELECT_PRESET)
    await message.reply("Выберите рамку", reply_markup=keyboard.SELECT_FRAME)
    await message.reply("Введите радиус (eg.: r_1100)")
    await message.reply("Введите координаты места (eg: l_)")


@dp.message_handler(lambda message: message.text.startswith('theme_'), commands=['preset'])
async def preset(message: types.Message):
    theme_name = message.text.split('_')[1]
    user_preset[message.from_user.id] = theme_name


@dp.message_handler(lambda message: message.text.startswith('frame_'), commands=['frame'])
async def frame(message: types.Message):
    frame_choice = message.text.split('_')[1]
    user_frame[message.from_user.id] = True if (frame_choice == "circle") else False


@dp.message_handler(lambda message: message.text.startswith('r_'))
async def radius(message: types.Message):
    user_radius[message.from_user.id] = int(message.text.split('_')[1])


@dp.message_handler(lambda message: message.text.startswith('l_'))
async def map(message: types.Message):
    await message.answer("Карта генерируется...")
    plot = prettymaps.plot(
        message.text.split('_')[1],
        circle=user_frame[message.from_user.id] if (user_frame[message.from_user.id] is not None) else default_settings[
            1],
        radius=user_radius[message.from_user.id] if (user_frame[message.from_user.id] is not None) else
        default_settings[2],
        preset=user_preset[message.from_user.id] if (user_frame[message.from_user.id] is not None) else
        default_settings[0],
    )
    plt.savefig(f"map_{message.from_user.id}.png")
    await message.answer_photo(types.InputFile(f"map_{message.from_user.id}.png"))


# @dp.message_handler(commands=[''])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
