from aiogram import Router, Bot
from aiogram.filters import Command
from database.models.all_models import User
from aiogram.types import Message
from aiogram import F
from database.models.engine import session_maker
from database.models.orm_operations import get_user

router = Router()


@router.message(F.text.lower() == 'профиль' or Command('profile'))
async def view_profile(message: Message, bot: Bot):
    async with session_maker() as session:
        user = await get_user(session, message.from_user.id)
        user_photo_profile = await bot.get_user_profile_photos(user_id=message.from_user.id)
        if user is None:
            await message.answer("Профиль не найден. Вы точно прошли регистрацию?")
        elif user.role == 'teacher' and user_photo_profile:
            photo = user_photo_profile.photos[0][-1]
            await message.answer_photo(photo.file_id, caption=f"Профиль преподавателя:\nФИО: {user.fio}\nТелефон: {user.phone}")
        else:
            photo_student = user_photo_profile.photos[0][-1]
            await message.answer_photo(photo_student.file_id, caption=f"Профиль ученика:\nФИО: {user.fio}\nТелефон: {user.phone}")
