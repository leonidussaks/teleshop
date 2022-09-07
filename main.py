import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import Config as conf
from db import Shop, User
from aiogram.utils.callback_data import CallbackData

bot = Bot(token=conf.token)
shop = Shop()
dp = Dispatcher(bot)
pag_init = CallbackData('change_page','action', 'page')

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

def keyboard_shop(page):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    shop_data = shop.check_shop()[page*3-3:page*3]
    if len(shop_data) != 3:
        keyboard.row(types.InlineKeyboardButton(text="назад", callback_data=pag_init.new(action='back', page=page)))
    else:
        keyboard.row(types.InlineKeyboardButton(text="назад", callback_data=pag_init.new(action='back', page=page)), types.InlineKeyboardButton(text="вперед", callback_data=pag_init.new(action='forward', page=page)))
    for i in shop_data:
        keyboard.add(types.InlineKeyboardButton(i['header'], callback_data=i['id']))
    return keyboard
        
# показ товаров
@dp.callback_query_handler(text="shop")
async def open_shop(call: types.CallbackQuery):
    await call.message.reply('просмотр ассортимента', reply_markup=keyboard_shop(1))

@dp.callback_query_handler(pag_init.filter(action='forward'))
async def shop_forward(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data['page'])
    page += 1
    await bot.edit_message_text(f'вперед на страницу {page}',
                                call.from_user.id,
                                call.message.message_id,
                                reply_markup=keyboard_shop(page))
    
@dp.callback_query_handler(pag_init.filter(action='back'))
async def shop_back(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data['page'])
    if page == 1: return False
    page -= 1
    await bot.edit_message_text(f'обратно на страницу {page}',
                                call.from_user.id,
                                call.message.message_id,
                                reply_markup=keyboard_shop(page))

# обработка нажатий на кнопочку товара
@dp.callback_query_handler(lambda call: True)
async def open_item(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="добавить в корзину", callback_data="add_in_chest"))   
    await bot.answer_callback_query(call.id)
    shop_data = shop.check_shop()
    #подставляет id товара к call.data
    for i in shop_data:
        if call.data == str(i['id']):
            await call.message.reply(f"заголовок: {i['header']}\nописание товара:{i['text']}\nцена: {i['price']}", reply_markup=keyboard)
            
@dp.callback_query_handler(text="payment")
async def open_payment(call: types.CallbackQuery):
    await call.message.reply(conf.payment)

    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)