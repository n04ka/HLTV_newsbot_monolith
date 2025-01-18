HLTV_URL = 'https://www.hltv.org/'
DATE_FORMAT = '%d-%m-%Y %H:%M'
CENSOR = 'Что-то в вашем вопросе меня смущает. Может, поговорим на другую тему?'
PROMPT = """Ты - профессиональный переводчик на русский язык.
Тебе будет дан текст, который необходимо перевести на русский язык, сохранив исходное форматирование текста.
В ответе необходимо отдать перевод в формате, приведенном ниже.
Если в запросе есть имена и никнеймы игроков, термины из киберспорта или игры Counter Strike, то их переводить не нужно.
Если в запросе необходимо поставить пробелы и слова слеплены вместе, то такой кусок слепленного текста переводить не нужно.
Если в тексте поставлена неправильно пунктуация, то исправь ее.
Твоя задача сделать такой перевод, чтобы лингвист считал его лингвистически приемлемым.
ВАЖНО! В своем ответе НЕ ОТВЕЧАЙ НА ЗАПРОС! В ответе нужно написать !только !перевод, без указания названия языка и любой другой дополнительной информации.
"""
ARTICLE_TABLE = """
                create table if not exists article (
                    id          INTEGER PRIMARY KEY,
                    title       TEXT DEFAULT NULL,
                    author		TEXT DEFAULT NULL,
                    timestamp	TIMESTAMP DEFAULT NULL,
                    url     	TEXT DEFAULT NULL,
                    description	TEXT DEFAULT NULL,
                    content    	TEXT DEFAULT NULL
                );
                """
TRANSLATION_TABLE = """
                    create table if not exists translation (
                        id          INTEGER PRIMARY KEY,
                        title       TEXT DEFAULT NULL,
                        author		TEXT DEFAULT NULL,
                        description	TEXT DEFAULT NULL,
                        content    	TEXT DEFAULT NULL
                    );
                    """
IMAGE_TABLE =   """
                create table if not exists image (
                    id          SERIAL,
                    article_id	INTEGER REFERENCES article (id),
                    url			TEXT
                );
                """