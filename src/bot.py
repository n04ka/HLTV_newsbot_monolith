from aiogram import Bot
from aiogram.exceptions import TelegramNetworkError
from telebot.util import smart_split
from external import DB
import asyncio
from secret import API_KEY, DEV_CHANNEL_ID


class NewsBot:
    
    def __init__(self) -> None:
        self.bot = Bot(API_KEY)


    async def post_message(self, id: int) -> None:
        art, images = await asyncio.gather(DB.get_translation(id), DB.get_article_images(id))
        text = f'<strong>⚡{art.title}⚡</strong>\n<i>{art.description}</i>\n\n{art.content}\n\n<i>Автор: {art.author}</i>'
        caption, *other = smart_split(text, chars_per_string=1024)
        splitted_text = smart_split(''.join(other), chars_per_string=4000)
        
        while True:
            try:
                await self.bot.send_photo(DEV_CHANNEL_ID, photo=images[0] if images else 'logo.jpg', caption=caption, parse_mode='html')
                break
            except TelegramNetworkError:
                pass
            
        for part in splitted_text:
            while True:
                try:
                    await self.bot.send_message(DEV_CHANNEL_ID, text=part, parse_mode='html')
                    break
                except TelegramNetworkError:
                    pass


