import matplotlib.pyplot as plt
import prettymaps
import  logging
from aiogram import Bot, Dispatcher, executor, types
import time
import random
import datetime

API_TOKEN = '5776852478:AAGmV-7refAgBdv7KH7-3jLjmphatpB7bZ4'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def sendhelp(message: types.Message):
    await message.answer('Привет! Этот бот использует библиотеку (prettymaps)[https://github.com/marceloprates/prettymaps]. '
                         'Ты можешь отправить координаты или название местности в виде "Volzhsky, Volgograd Oblast, Russia" и'
                         'получить приятную картиночку этого места!'
                         'Команды: '
                         '/start - приветственное сообщение'
                         '/drawmap - сгенерировать карту')

@dp.message_handler(commands=['drawmap'])
async def draw_map(message: types.Message, pRadius: types.Message):
    await message.reply("Я начал генерировать Вашу карту")
    plot = prettymaps.plot(
        message.text[8:],
        circle=True,
        radius=int(pRadius),
        layers={
            "green": {
                "tags": {
                    "landuse": "grass",
                    "natural": ["island", "wood"],
                    "leisure": "park"
                }
            },
            "forest": {
                "tags": {
                    "landuse": "forest"
                }
            },
            "water": {
                "tags": {
                    "natural": ["water", "bay"]
                }
            },
            "parking": {
                "tags": {
                    "amenity": "parking",
                    "highway": "pedestrian",
                    "man_made": "pier"
                }
            },
            "streets": {
                "width": {
                    "motorway": 5,
                    "trunk": 5,
                    "primary": 4.5,
                    "secondary": 4,
                    "tertiary": 3.5,
                    "residential": 3,
                }
            },
            "building": {
                "tags": {"building": True},
            },
        },
        style={
            "background": {
                "fc": "#F2F4CB",
                "ec": "#dadbc1",
                "hatch": "ooo...",
            },
            "perimeter": {
                "fc": "#F2F4CB",
                "ec": "#dadbc1",
                "lw": 0,
                "hatch": "ooo...",
            },
            "green": {
                "fc": "#D0F1BF",
                "ec": "#2F3737",
                "lw": 1,
            },
            "forest": {
                "fc": "#64B96A",
                "ec": "#2F3737",
                "lw": 1,
            },
            "water": {
                "fc": "#a1e3ff",
                "ec": "#2F3737",
                "hatch": "ooo...",
                "hatch_c": "#85c9e6",
                "lw": 1,
            },
            "parking": {
                "fc": "#F2F4CB",
                "ec": "#2F3737",
                "lw": 1,
            },
            "streets": {
                "fc": "#2F3737",
                "ec": "#475657",
                "alpha": 1,
                "lw": 0,
            },
            "building": {
                "palette": [
                    "#FFC857",
                    "#E9724C",
                    "#C5283D"
                ],
                "ec": "#2F3737",
                "lw": 0.5,
            }
        }
    )
    plt.savefig("Map.png")

    await message.answer_photo(types.InputFile("Map.png"))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)