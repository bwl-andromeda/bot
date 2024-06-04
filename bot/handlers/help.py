from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.kb import kb_for_help
from bot.handlers.msg import msg_for_help

router = Router()


@router.message(F.text.lower() == "обратная связь" or Command(commands=['help']))
async def help(message: Message):
    await message.answer(msg_for_help, reply_markup=kb_for_help)
