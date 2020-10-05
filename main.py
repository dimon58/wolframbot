import logging

from aiogram import Bot, Dispatcher, executor, types
from configs import TOKEN, end_phrases, start_phrases
from wolfram import natural_language_process, wolfram
from random import choice


API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(choice(start_phrases))
    try:
        r = await wolfram(message.text)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile(r), 'Solution')
        await message.answer_media_group(media=media)
        await message.answer(choice(end_phrases))
    except IndexError:
        await message.answer('Пошёл в жопу с такими запросами')

    await message.answer(await natural_language_process(message.text))


@dp.message_handler(commands=['wolfram'])
async def do_magic(message: types.Message):
    await message.answer('WIP')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
