import asyncio
from parser import Parser
from translator import translate
from bot import NewsBot
from external import DB
from utils import extract_id_from_url
import logging


bot = NewsBot()


def enable_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter('%(levelname)s - %(message)s')
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


async def process_article(id: int):
    await translate(id)
    await bot.post_message(id)


async def fetch(parser: Parser):
    while not parser.check_connection():
            logging.error('Cannot reach HLTV.org! Retrying in 5 seconds...')
            await asyncio.sleep(5)
            continue
        
    parser.accept_cookies()
    
    logging.info('Fetching news...')
    parsed_news = set(await DB.get_article_ids())
    news = [url for url in parser.get_news() 
            if '#' not in url
            and extract_id_from_url(url) not in parsed_news]
    logging.info(f'Suitable news found: {len(news)}')
    
    for url in news:
        logging.info(f'Parsing {url}')
        try:
            art, images = parser.parse_article(url)
            logging.info(f'Succefully parsed {url}')
            await DB.insert_article(art)
            for img_url in images:
                await DB.insert_image(art.id, img_url)
            logging.info(f'Inserted article with id = {art.id}')
        except Exception as e:
            logging.error('Parsing failed. Reason:', e)
            continue
        
        id = await translate(art.id)
        if id is not None:
            await bot.post_message(id)
        
    logging.info(f'All news parsed. Sleeping...')


async def main():
    await asyncio.gather(fetch(parser=Parser()), asyncio.sleep(600))


if __name__ == '__main__':
    enable_logging()
    asyncio.run(DB.init_db())
    while True:
        asyncio.run(main())
        