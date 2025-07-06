from aiogram.utils.keyboard import ReplyKeyboardBuilder

def admin_keyb():
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Тикеты")
    keyb.adjust(1)
    return keyb.as_markup()

def stop_dialog_keyb():
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Остановить диалог")
    keyb.adjust(1)
    return keyb.as_markup()