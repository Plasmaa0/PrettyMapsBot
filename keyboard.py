from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


# BTN_SLCT_PRST = KeyboardButton('Select Preset', callback_data='select preset')
# BTN_SLCT_FRM = KeyboardButton('Select Frame', callback_data='select frame')
#
# BTN_BARCELONA = KeyboardButton('barcelona', callback_data='theme_barcelona')
# BTN_BARCELONA_PLOTTER = KeyboardButton('barcelona-plotter', callback_data='theme_barcelona-plotter')
# BTN_CB_BF_F = KeyboardButton('cb-bf-f', callback_data='theme_cb-bf-f')
# BTN_DEFAULT = KeyboardButton('default', callback_data='theme_default')
# BTN_HEERUGOWAARD = KeyboardButton('macao', callback_data='theme_macao')
# BTN_MINIMAL = KeyboardButton('minimal', callback_data='theme_minimal')
# BTN_TIJUCA = KeyboardButton('tijuca', callback_data='theme_tijuca')
#
# BTN_CIRCLE = KeyboardButton('circle', callback_data='frame_circle')
# BTN_SQUARE = KeyboardButton('square', callback_data='frame_square')
#
# SELECT_PRESET = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите пресет").add(BTN_BARCELONA).add(BTN_BARCELONA_PLOTTER).\
#                                        add(BTN_CB_BF_F).add(BTN_DEFAULT).add(BTN_HEERUGOWAARD).\
#                                        add(BTN_MINIMAL).add(BTN_TIJUCA)
# SELECT_FRAME = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите рамку").add(BTN_CIRCLE).add(BTN_SQUARE)
