from aiogram import F, Router
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from keyboards.inline import tickets_keyb
from keyboards.reply import stop_dialog_keyb,admin_keyb
from database.db import (get_open_tickets,connect_admin_to_ticket,
                         get_user_ticket_by_user,get_admin,create_user,add_message_to_ticket,
                         get_user_id,close_ticket,get_ticket_by_id,
                         get_user_ticket_by_admin,get_admin_in_progres_ticket,get_user_ticket, ticket_close
                         )
from utils import parse_ticket_text

router = Router()

@router.message(F.text == "Тикеты")
async def tickets(message:types.Message):
    if get_admin(message.from_user.id):
        await message.answer(text = "*Тикеты без админа:*", reply_markup=tickets_keyb(get_open_tickets()), parse_mode=ParseMode.MARKDOWN_V2)

@router.callback_query(F.data.startswith("id."))
async def connect_admin_ticket(callback_query:types.CallbackQuery):
    ticket_id = callback_query.data.split("id.")[1]
    if ticket_close(ticket_id):
        connect_admin_to_ticket(ticket_id, callback_query.from_user.id)
        ticket_text = parse_ticket_text(ticket_id)
        await callback_query.message.answer(text=ticket_text, reply_markup=stop_dialog_keyb())

        ticket = get_ticket_by_id(ticket_id)
        user_id = get_user_id(ticket)
        await callback_query.bot.send_message(chat_id=user_id, text="_Админ подключился_", reply_markup=stop_dialog_keyb(), parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text == "Остановить диалог")
async def stop_dialog(message: types.Message):
    admin = get_admin(message.from_user.id)
    if admin is None:
        print("User user_id", {message.from_user.id})
        ticket = get_user_ticket_by_user(message.from_user.id)
        user_id = message.from_user.id
        admin_id = ticket.admin_id
    else:
        print("Admin user_id", {message.from_user.id})
        ticket_admin = get_admin_in_progres_ticket(message.from_user.id)
        ticket = get_user_ticket_by_admin(ticket_admin.user_id)
        user_id = get_user_id(ticket)
        admin_id = message.from_user.id
    admin_id = ticket.admin_id
    await message.bot.send_message(chat_id=user_id, text = "*Диалог завершен*", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)
    await message.bot.send_message(chat_id=admin_id, text = "*Диалог завершен*", reply_markup=admin_keyb(), parse_mode=ParseMode.MARKDOWN_V2)
    close_ticket(user_id,admin_id)

@router.message(F.text != "Остановить диалог")
async def user_new_messages(message: types.Message):
    admin = get_admin(message.from_user.id)
    if admin is None:
        ticket = get_user_ticket(message.from_user.id)
    else:
        ticket_admin = get_admin_in_progres_ticket(message.from_user.id)
        if ticket_admin:
            user_id = get_user_id(ticket_admin)
            print(f"User ID {user_id}")
            ticket = get_user_ticket_by_user(user_id)
        else:
            ticket = None
    if ticket is not None:
        user_id = get_user_id(ticket)
        admin_id = ticket.admin_id 
        print(ticket.status)
        if ticket.status == "in_progress":
            print(f"Admin id == {admin_id}")
            print(f"User id == {user_id}")
            if admin is None:
                await message.bot.send_message(chat_id=admin_id,text = message.text)
            if admin:
                await message.bot.send_message(chat_id=user_id,text = message.text)

            add_message_to_ticket(message.text, ticket, message.from_user.id)
        else:
            if ticket.status == "open":
                add_message_to_ticket(message.text, ticket, message.from_user.id)
    else:
        if admin is None:
            print(admin)
            create_user(message.from_user.id,message.text)
            await message.answer(text="*Тикет создан, ждите подключения администартора*", parse_mode=ParseMode.MARKDOWN_V2)

