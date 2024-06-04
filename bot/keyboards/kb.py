from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
kb_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Преподаватель", callback_data='teacher')
    ],
    [
        InlineKeyboardButton(text='Ученик', callback_data='student')
    ]])


kb_for_help = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Телеграмм', url="https://t.me/bwl_andromeda")
    ],
    [
        InlineKeyboardButton(
            text='Вконтакте', url='https://vk.com/alone_wanderer_of_dark')
    ]
])


main_menu = ('Профиль', 'Мои группы', 'Статистика', 'Обратная связь')
main_menu_kb = ReplyKeyboardBuilder()
for i in main_menu:
    main_menu_kb.add(KeyboardButton(text=str(i)))
    main_menu_kb.adjust(3)
