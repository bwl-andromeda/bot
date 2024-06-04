from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import CommandStart
from bot.handlers.msg import message_for_start, message_for_menu
from bot.keyboards.kb import kb_start, main_menu_kb
from aiogram.fsm.context import FSMContext
from bot.fsm.registration import Reg
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.orm_operations import add_user,get_user
from database.models.engine import session_maker
import re

router = Router()


def check_full_name(full_name):
    pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$'

    if re.match(pattern, full_name):
        return True
    else:
        return False


def check_phone_number(phone_number):
    pattern = r'^\+7\d{10}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False


@router.message(CommandStart())
async def start(message: Message):
    """
    Команда /start
    """
    if message.chat.type == "private":
        async with session_maker() as session:
            user = await get_user(session, message.from_user.id)
            if user:
                await message.reply(message_for_menu, reply_markup=main_menu_kb.as_markup(resize_keyboard=True, one_time_keyboard=True))
            else:
                await message.reply(message_for_start, reply_markup=kb_start)


@router.callback_query(F.data == "teacher")
async def start_teacher(call: CallbackQuery, state: FSMContext):
    await call.answer('Ты выбрал роль преподавателя!', show_alert=False)
    await state.update_data(tg_id=call.message.from_user.id,
                            role='teacher')
    await state.set_state(Reg.fio)
    await call.message.answer(f'Принял!\nВведи пожалуйста свое ФИО в формате: "Фамилия Имя Отчество"')


@router.message(Reg.fio)
async def teacher_fio(message: Message, state: FSMContext):
    if not check_full_name(message.text):
        await message.answer('Неверно введено ФИО, попробуй еще раз!')
    else:
        await state.update_data(fio=message.text,
                                tg_username=f'@{message.from_user.username}',)
        await state.set_state(Reg.phone)
        await message.answer(f'Принял!\nВведи пожалуйста свой номер телефона в формате:\n+7(999)999-99-99 или +79998887766')


@router.message(Reg.phone)
async def teacher_phone(message: Message, state: FSMContext):
    if not message.text.startswith('+7') and not check_phone_number(message.text):
        await message.answer('Неверно введен номер телефона, попробуй еще раз!')
    else:
        await state.update_data(phone=message.text)
        data = await state.get_data()
        async with session_maker() as session:
            await add_user(session, data)
            await message.answer(f'Принял, регистрация прошла успешно!\nФИО: {data['fio']}\nНомер телефона: {data['phone']}',
                             reply_markup=main_menu_kb.as_markup(resize_keyboard=True, one_time_keyboard=True))
            await state.clear()


@router.callback_query(F.data == 'student')
async def start_student(call: CallbackQuery, state: FSMContext):
    await call.answer('Ты выбрал роль ученика!', show_alert=False)
    await state.update_data(tg_id=call.message.from_user.id,
                            tg_username=f'@{call.message.from_user.username}',
                            role='student')
    await state.set_state(Reg.fio)
    await call.message.answer('Принял!\nВведи пожалуйста свое ФИО в формате: "Фамилия Имя Отчество"')


@router.message(Reg.fio)
async def student_fio(message: Message, state: FSMContext):
    if not check_full_name(message.text):
        await message.answer('Неверно введено ФИО, попробуй еще раз!')
    else:
        await state.update_data(fio=message.text)
        await state.set_state(Reg.phone)
        await message.answer('Принял!\nВведи пожалуйста свой номер телефона в формате:\n+7(999)999-99-99 или '
                             '+79998887766')


@router.message(Reg.phone)
async def student_phone(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text.startswith('+7') and not check_phone_number(message.text):
        await message.answer('Неверно введен номер телефона, попробуй еще раз!')
    else:
        await state.update_data(phone=message.text)
        data = await state.get_data()
        async with session_maker() as session:
            await add_user(session, data)
            await message.answer(f'Принял, регистрация прошла успешно!\nФИО: {data["fio"]}\nНомер телефона: {data["phone"]}',
                                 reply_markup=main_menu_kb.as_markup(resize_keyboard=True, one_time_keyboard=True))
            await state.clear()
