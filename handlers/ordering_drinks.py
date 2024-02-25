from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_drinks_vkus = ["Кислый", "Сладкий", "Горький", "Кисло-сладкий"]
available_drinks_sizes = ["Водка", "Джин", "Ром", "Текила", "Виски"]



class OrderDrinks(StatesGroup):
    choosing_drinks_name = State()
    choosing_drinks_size = State()


@router.message(Command("drinks"))
async def cmd_drinks(message: Message, state: FSMContext):
    await message.answer(
        text="Какой коктейль по вкусу желаете?",
        reply_markup=make_row_keyboard(available_drinks_vkus)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderDrinks.choosing_drinks_name)

# Этап выбора блюда #


@router.message(OrderDrinks.choosing_drinks_name, F.text.in_(available_drinks_vkus))
async def drinks_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drinks=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите на каком алкоголе:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )
    await state.set_state(OrderDrinks.choosing_drinks_size)



# В целом, никто не мешает указывать стейты полностью строками
# Это может пригодиться, если по какой-то причине
# ваши названия стейтов генерируются в рантайме (но зачем?)
@router.message(StateFilter("OrderDrinks:choosing_drinks_name"))
async def drinks_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого напитка.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_drinks_vkus)
    )

# Этап выбора размера порции и отображение сводной информации #
@router.message(OrderDrinks.choosing_drinks_size, F.text.in_(available_drinks_sizes))
async def drinks_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали коктейль {message.text.lower()} порцию {user_data['chosen_drinks']}.\n"
             f"Тут пока ничего!: ",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderDrinks.choosing_drinks_size)
async def drinks_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )