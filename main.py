import logging
import asyncio
from aiogram import types
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, BotCommand, FSInputFile, URLInputFile, BufferedInputFile
from config_reader import config
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

big_button_1 = InlineKeyboardButton(
    text='Режим работы ✅',
    callback_data='big_button_1_pressed'
)

big_button_2 = InlineKeyboardButton(
    text='Акции',
    callback_data='big_button_2_pressed'
)

big_button_3 = InlineKeyboardButton(
    text='Школа барменов',
    callback_data='big_button_3_pressed'
)

back_button = types.InlineKeyboardButton(
    text='Назад',
    callback_data='back_button_pressed'
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2],
                     [big_button_3]])

keyboard_opt = InlineKeyboardMarkup(
    inline_keyboard=[[back_button]])


url_button_1 = InlineKeyboardButton(
    text='Вконтакте',
    url='https://vk.com/vlastbar'
)

url_button_2 = InlineKeyboardButton(
    text='Телеграм',
    url='https://web.telegram.org/a/#1368428868'
)

keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1]]
)

keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_2]]
)
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Приветствую тебя юный подаван\n'
             'Для того чтобы использовать бота есть кнопки\n'
             'Да прибудет с тобой сила!\n\n',
        reply_markup=keyboard
    )

@dp.message(Command("album"))
async def cmd_album(message: Message):
    album_builder = MediaGroupBuilder(
        caption="Афиша мероприятий 📆"
    )
    album_builder.add_photo(
        media="https://i.ibb.co/Fs73STN/2.jpg"
    )
    album_builder.add_photo(
        media="https://i.ibb.co/v46fYry/1.jpg"
    )
    await message.answer_media_group(
        media=album_builder.build()
    )

@dp.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    keyboard_opt = types.InlineKeyboardMarkup()
    keyboard_opt.add(back_button)
    if callback.message.text != 'Режим работы:':
        await callback.message.edit_text(
            text='Сегодня заведение работает до 00:00',
            reply_markup=callback.message.reply_markup)
    await callback.answer(
        text='Сегодня на смене: Иван. Так что бегом в бар!',
        show_alert=True
    )

@dp.callback_query(lambda c: c.data == 'back_button_pressed')
async def process_back_button_press(callback: CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(big_button_1)
    await callback.message.edit_text("Выберите действие:", reply_markup=keyboard)

@dp.callback_query(F.data == 'big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    if callback.message.text != 'Акции':
        await callback.message.edit_text(
            text='Акции',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer(
        text='К сожалению в данный момент у нас не проводиться акций, '
             'но мы все равно с радостью тебя ждем в нашем баре!',
        show_alert=True
    )


@dp.callback_query(F.data == 'big_button_3_pressed')
async def process_button_3_press(callback: CallbackQuery):
    if callback.message.text != 'Школа барменов':
        await callback.message.edit_text(
            text='🔥Курс бармена 2024🔥\n\n'
                 '🤔Пока все ищут барменов, вместо того чтобы учить и направлять, я решил снова запустить❗️КУРС❗️\n\n'
                 '📌Что будет ?\n\n',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Записаться на курс", url="http://yourwebsite.com")
                ]
            ])
        )

    await callback.answer(
        text='Записаться на курс вы можете по ссылке',
        show_alert=True
    )

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Главное меню'),
        BotCommand(command='/contacts',
                   description='Мы в социальных сетях'),
        BotCommand(command='/album',
                   description='Афиша мероприятий 📆'),
        BotCommand(command='/contacts1',
                   description='Заказать телеграм бота')
    ]

    async def main():
        await bot.start_polling()
        await asyncio.sleep(3600)
        await bot.stop_polling()

    await bot.set_my_commands(main_menu_commands)

# @dp.message(Command("help"))
# @dp.message(CommandStart(
#     deep_link=True, magic=F.args == "help"
# ))
# async def cmd_start_help(message: Message):
#     await message.answer("Список команд:\n\n"
#                          "/start - Начальное приветствие\n"
#                          "/help - Справка бота(команды)\n"
#                          "/hello - Приветствие бота\n\n"
#                          "Список команд для группы:\n\n"
#                          "/dice - Брость кубик\n"
#                          "/basketball - Бросить баскетбольный мяч"
#                          )

@dp.message(Command("contacts"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "contacts"
))
async def cmd_contacts(message: Message):
    await message.answer("Обязательно подпишитесь на нас в социальных сетях\n\n"
                         "Это помогает развитию проекта!\n\n"
                         )
    await message.answer(text='Мы в социальных сетях',
        reply_markup=keyboard1)


@dp.message(Command("contacts1"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "contacts1"
))
async def cmd_contacts1(message: Message):
    await message.answer("Связаться с автором\n\n"
                         "Это помогает развитию проекта!\n\n"
                         )
    await message.answer(text='Заказать телеграм бота',
        reply_markup=keyboard2)

@dp.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)
    await message.answer("Нормально ты стелишь!")


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.callback_query
    dp.run_polling(bot, allowed_updates=[])
