import logging
import os

from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from keyboard import make_row_keyboard

import matplotlib.pyplot as plt
import prettymaps

API_TOKEN = '5776852478:AAGmV-7refAgBdv7KH7-3jLjmphatpB7bZ4'
API_TOKEN_MY = '1812123829:AAGZAY9C87xBolIsuNoFWWpezFXnZkUsvX4'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
user_preset = {}
user_frame = {}
user_radius = {}
default_settings = {'barcelona', True, 1100}

themes = ['barcelona', 'default', 'macao', 'minimal', 'tijuca']
frames = ['circle', 'square']


# Сделать кнопки для выбора пресета
# Сделать возможность вводить координаты и радиус
# Сделать ответ на неожиданное поведение
# Сделать выбор рамочки

class Form(StatesGroup):
    began = State()
    radius = State()
    preset = State()
    frame = State()
    place = State()


@router.message(Command('start'))
async def sendhelp(message: types.Message):
    await message.answer(
        'Привет! Этот бот использует библиотеку prettymaps.\n'
        'Ты можешь отправить координаты или название местности через запятую на английском.'
        'получить приятную картиночку этого места!\n\n')
    # 'Команды: \n'
    # '/start         - приветственное сообщение \n'
    # '/configure_map - настроить и сгенерировать карту \n'
    # '/preset        - выбрать пресет \n'
    # '/radius        - выбрать радиус \n'
    # '/map           - быстрая генерация карты с дефолтными и/или сохраненными настройками'
    # '/frame         - выбрать рамку \n\n'
    # 'prettymaps lib: https://github.com/marceloprates/prettymaps')


@router.message(Command('drawmap'))
async def draw_map(message: types.Message, state: FSMContext):
    # await message.answer("Вasdы можете ответить на сообщения, чтобы настроить следующие параметры.")
    await state.set_state(Form.began.state)
    await message.reply("Выберите пресет", reply_markup=make_row_keyboard(themes))
    # await message.reply("Введите координаты места (eg: l_)")


@router.message(Command('stop'))
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply('состояние бота сброшено')


@router.message(Form.began)
async def theme_select(message: types.Message, state: FSMContext):
    if message.text in themes:
        user_data = await state.get_data()
        user_data['preset'] = message.text
        await state.set_data(user_data)
        await state.set_state(Form.frame.state)
        await message.reply("Выберите рамку", reply_markup=make_row_keyboard(frames))
    else:
        await message.reply('плохая тема, выбери из предложенных')


@router.message(Form.frame)
async def frame_select(message: types.Message, state: FSMContext):
    if message.text in frames:
        user_data = await state.get_data()
        user_data['frame'] = message.text
        await state.set_data(user_data)
        await state.set_state(Form.radius.state)
        await message.reply("Выберите радиус. Можно написать свой!",
                            reply_markup=make_row_keyboard([str(i) for i in range(100, 1001, 200)]))
    else:
        await message.reply('плохая рамка, выбери из предложенных')


@router.message(Form.radius)
async def radius_select(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        user_data['radius'] = int(message.text)
    except:
        await message.reply('введи число! например 100')
    else:
        await state.set_data(user_data)
        await state.set_state(Form.place.state)
        await message.reply("Выберите место")


@router.message(Form.place)
async def place_select(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    place = message.text
    gen_msg = await message.reply('начинаю генерацию')
    try:
        print(place,
              user_data['frame'] == 'circle',
              int(user_data['radius']),
              user_data['preset'], )
        plot = prettymaps.plot(
            place,
            circle=user_data['frame'] == 'circle',
            radius=int(user_data['radius']),
            preset=user_data['preset'],
        )
    except Exception as e:
        if 'Nominatim could not geocode query' in str(e):
            await gen_msg.delete()
            await message.reply('Не могу понять, что это за место. Введи место еще раз.')
            return
        await message.reply('что-то пошло не так. может быть были введены плохие данные? попробуй еще раз')
        print(e)
    else:
        plt.savefig(f"map_{message.from_user.id}.png")
        await message.answer_photo(photo=types.FSInputFile(f"map_{message.from_user.id}.png"), caption=place)
        await gen_msg.delete()
        os.remove(f"map_{message.from_user.id}.png")
    await state.clear()


@router.message()
async def unknown(message: types.Message):
    await message.answer('Напиши /drawmap чтобы начать генерацию')


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
