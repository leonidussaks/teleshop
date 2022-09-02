from aiogram import Bot, Dispatcher, executor, types
from config import Config as conf

bot = Bot(token=conf.token)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text=conf.shop, callback_data="shop"),
        types.InlineKeyboardButton(text=conf.payment, callback_data="payment"),
        types.InlineKeyboardButton(text=conf.about, url=conf.about_url),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(conf.hello, reply_markup=keyboard)

@dp.callback_query_handler(text="shop")
async def send_random_value(call: types.CallbackQuery):
    await call.message.reply(conf.shop)

@dp.callback_query_handler(text="payment")
async def send_random_value(call: types.CallbackQuery):
    await call.message.reply(conf.payment)

    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)