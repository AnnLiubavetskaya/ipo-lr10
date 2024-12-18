import json
import requests
from bs4 import BeautifulSoup

# URL страницы, которую нужно получить
url = "https://quotes.toscrape.com/"

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем, что запрос прошел успешно (статус код 200)
if response.status_code == 200:
    # Получаем HTML-код страницы
    soup = BeautifulSoup(response.text, "html.parser")
    allQuote = soup.findAll('div', class_='quote')
    json_list = []
    jsonFile = open("data.json", "w", encoding='utf-8')
    count = 0
    for quote in allQuote:
        count += 1
        text = quote.find('span', class_='text')
        author = quote.find('small', class_='author')
        if text is not None and author is not None:
            json_list.append({"Quote": f"{text.text}", "Author" : f"{author.text}"})
        print(f'{count}. Quote: {text.text}; Author: {author.text};')
    json.dump(json_list, jsonFile, indent=4, ensure_ascii=False)


        
else:
    print(f"Ошибка {response.status_code}: Не удалось получить страницу.")