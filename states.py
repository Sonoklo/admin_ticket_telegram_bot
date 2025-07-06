from aiogram.fsm.state import StatesGroup,State

class Problem(StatesGroup):
    problem_info = State()