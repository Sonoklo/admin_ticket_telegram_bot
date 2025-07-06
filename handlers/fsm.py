from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart
from states import Problem 
from database.db import create_user,get_admin
from keyboards.reply import admin_keyb

router = Router()

@router.message(CommandStart())
async def start_action(message: Message, state: FSMContext ):
    if get_admin(message.from_user.id) is None:
        await state.set_state(Problem.problem_info)
        await message.answer(text = "Распишите подробно вашу проблему, администратор вам поможет")
    else:
        await message.answer(text = "Админ панель", reply_markup=admin_keyb())

@router.message(Problem.problem_info)
async def start_ticket(message: Message, state: FSMContext):
    await message.answer(text = "Тикет создан, ждите подключения администратора")
    create_user(message.from_user.id, message.text)
    await state.clear()


    
