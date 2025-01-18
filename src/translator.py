from gigachat import GigaChat
from schemas import TranslatedArticle
from external import DB
from config import CENSOR, PROMPT
from secret import TOKEN


async def translate(id: int) -> int | None:
    art = await DB.get_article(id)
    
    with GigaChat(credentials=TOKEN, verify_ssl_certs=False, timeout=600) as giga:
        full_text = '\n\n'.join((art.title, art.description, art.content))
        response = giga.chat(f"{PROMPT}\n{full_text}")
        if CENSOR in response.choices[0].message.content:
            print(f'Gigachat censorship on article with id = {id}')
            return None
    
    blocks = response.choices[0].message.content.split('\n\n', maxsplit=2)
    if len(blocks) != 3:
        title, description, content = '', '', response.choices[0].message.content
    else:
        title, description, content = blocks
    translation = TranslatedArticle(id=art.id, title=title, author=art.author, description=description, content=content)
    await DB.insert_translated_article(translation)
    return id
    