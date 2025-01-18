from schemas import Article, TranslatedArticle
from typing import List
import asyncio
import aiosqlite
from config import ARTICLE_TABLE, TRANSLATION_TABLE, IMAGE_TABLE


class DB:
    
    @staticmethod
    async def init_db():
        async with aiosqlite.connect('database.db') as conn:
            await asyncio.gather(conn.execute(ARTICLE_TABLE), conn.execute(TRANSLATION_TABLE), conn.execute(IMAGE_TABLE))
    
    
    @staticmethod
    async def get_article_ids() -> List[int]:
        async with aiosqlite.connect('database.db') as conn:
            result = await conn.execute_fetchall("""select id from article""")
        return [int(record[0]) for record in result]


    @staticmethod
    async def insert_article(art: Article):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute( """
                                insert into article (id, title, author, timestamp, url, description, content)
                                values (?, ?, ?, ?, ?, ?, ?)
                                """, (art.id, art.title, art.author, art.timestamp, art.url, art.description, art.content))
            await conn.commit()
        

    @staticmethod
    async def insert_image(art_id: int, url: str):
       async with aiosqlite.connect('database.db') as conn:
            await conn.execute( """
                                insert into image (article_id, url)
                                values (?, ?)
                                """, (art_id, url))
            await conn.commit()


    @staticmethod
    async def get_translation(id: int) -> TranslatedArticle:
        async with aiosqlite.connect('database.db') as conn:
            cursor = await conn.execute("""select * from translation where id = ?""", (id,))
            record = await cursor.fetchone()
        if not record:
            print(record)
            raise ValueError(f'No article with id = {id} in the database')
        id, title, author, description, content = record
        return TranslatedArticle(id=id, 
                       title=title, 
                       author=author,
                       description=description,
                       content=content
                       )
    
    
    @staticmethod
    async def get_article_images(id: int) -> List[str]:
        async with aiosqlite.connect('database.db') as conn:
            records = await conn.execute_fetchall("""select url from image where article_id = ?""", (id,))
        return [record[0] for record in records]
    
    
    @staticmethod
    async def get_article(id: int) -> Article:
        async with aiosqlite.connect('database.db') as conn:
            cursor = await conn.execute("""select * from article where id = ?""", (id,))
            record = await cursor.fetchone()
        if not record:
            async with aiosqlite.connect('database.db') as conn:
                print(await conn.execute_fetchall("""select * from article"""))
            raise ValueError(f'No article with id = {id} in the database')
        id, title, author, timestamp, url, description, content = record
        return Article(id=id, 
                       title=title, 
                       author=author, 
                       timestamp=timestamp, 
                       url=url,
                       description=description,
                       content=content
                       )
        
      
    @staticmethod  
    async def insert_translated_article(art: TranslatedArticle):
        async with aiosqlite.connect('database.db') as conn:
            await conn.execute( """insert into translation (id, title, author, description, content)
                                values (?, ?, ?, ?, ?)
                                """, (art.id, art.title, art.author, art.description, art.content))
            await conn.commit()