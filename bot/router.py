from time import sleep

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from utils import offers
from config import bot
from aiogram.filters import CommandStart
from .keyboard import main_kb
from .states import Offer


router = Router()

@router.callback_query(F.data.startswith('previous'))
async def print_previous(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    offer_idx = (await state.get_data())['offer_index']
    if offer_idx == 0:
        offer_idx = len(offers)
    try:
        sleep(0.5)
        await bot.edit_message_text(f'''
            Название: {offers[offer_idx-1][1]}
            __________________________________
            Описание: {offers[offer_idx-1][2]}
            __________________________________
            {offers[offer_idx-1][3]}
            __________________________________
            Ссылка: https://www.fl.ru{offers[0][4]}
            ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=main_kb())
    except TelegramBadRequest as e:
        if e == 'Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message':
            print('Слишком быстро')
            sleep(1)
            await bot.edit_message_text(f'''
                Название: {offers[offer_idx-1][1]}
                __________________________________
                Описание: {offers[offer_idx-1][2]}
                __________________________________
                {offers[offer_idx-1][3]}
                __________________________________
                Ссылка: https://www.fl.ru{offers[0][4]}
                ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=main_kb())
        elif e == 'Telegram server says - Bad Request: MESSAGE_TOO_LONG':
            print('Сообщение слишком большое, скипаю')
            for idx in range(2, len(offers)):
                try:
                    await bot.edit_message_text(f'''
                                    Название: {offers[offer_idx - idx][1]}
                                    __________________________________
                                    Описание: {offers[offer_idx - idx][2]}
                                    __________________________________
                                    {offers[offer_idx - idx][3]}
                                    __________________________________
                                    Ссылка: https://www.fl.ru{offers[0][4]}
                            ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id,
                                                reply_markup=main_kb())
                    break
                except:
                    continue

    finally:
        await state.update_data(offer_index=offer_idx - 1)


@router.callback_query(F.data.startswith('next'))
async def print_previous(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    offer_idx = (await state.get_data())['offer_index']
    if offer_idx == len(offers) - 1:
        offer_idx = -1
    try:
        sleep(0.5)
        await bot.edit_message_text(f'''
            Название: {offers[offer_idx+1][1]}
            __________________________________
            Описание: {offers[offer_idx+1][2]}
            __________________________________
            {offers[offer_idx+1][3]}
            __________________________________
            Ссылка: https://www.fl.ru{offers[0][4]}
    ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=main_kb())
    except TelegramBadRequest as e:
        if e == 'Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message':
            print('Слишком быстро')
            sleep(1)
            await bot.edit_message_text(f'''
                Название: {offers[offer_idx+1][1]}
                __________________________________
                Описание: {offers[offer_idx+1][2]}
                __________________________________
                {offers[offer_idx+1][3]}
                __________________________________
                Ссылка: https://www.fl.ru{offers[0][4]}
        ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=main_kb())
        elif e == 'Telegram server says - Bad Request: MESSAGE_TOO_LONG':
            print('Сообщение слишком большое, скипаю')
            for idx in range(2, len(offers)):
                try:
                    await bot.edit_message_text(f'''
                                    Название: {offers[offer_idx + idx][1]}
                                    __________________________________
                                    Описание: {offers[offer_idx + idx][2]}
                                    __________________________________
                                    {offers[offer_idx + idx][3]}
                                    __________________________________
                                    Ссылка: https://www.fl.ru{offers[0][4]}
                            ''', message_id=callback.message.message_id, chat_id=callback.message.chat.id,
                                                reply_markup=main_kb())
                    break
                except:
                    continue
    finally:
        await state.update_data(offer_index=offer_idx + 1)


@router.message(CommandStart())
async def print_offers(message: Message, state: FSMContext):
    msg = await message.answer('Подождите немного...')
    await bot.edit_message_text(f'''
Название: {offers[0][1]}
__________________________________
Описание: {offers[0][2]}
__________________________________
{offers[0][3]}
__________________________________
Ссылка: https://www.fl.ru{offers[0][4]}
    ''', reply_markup=main_kb(), message_id=msg.message_id, chat_id=message.chat.id)
    await state.set_state(Offer.offer_index)
    await state.update_data(offer_index=offers[0][0])