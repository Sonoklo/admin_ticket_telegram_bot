from aiogram.utils.keyboard import InlineKeyboardBuilder

def tickets_keyb(tickets):
    keyb = InlineKeyboardBuilder()
    for ticket in tickets:
        keyb.button(text = str(ticket.id), callback_data=f"id.{str(ticket.id)}")
    keyb.adjust(5)
    return keyb.as_markup()