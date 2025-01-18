# HLTV_newsbot_monolith
 Телеграм бот, который берёт новости с HLTV.org, переводит их на русский язык с помощью Gigachat и постит в [телеграм канал](https://t.me/HLTV_newsbot_dev).
 
![hltv logo](HLTV_tg_bot_monolith/logo.jpg)

# Составляющие:
1. *Fetcher* - selenium + undetected_chromedriver + selenium_stealth + BeautifulSoup
2. *Translator* - GigaChat
3. *TG_bot* - aiogram
4. *ArticleDB* - SQLite
