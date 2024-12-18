import json
import requests
from bs4 import BeautifulSoup

# URL страницы, которую нужно получить
url = "https://quotes.toscrape.com/"
html_simple = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Таблица с фоном</title>
    <style>
        body {
            background: linear-gradient(45deg, #ff9a8b, #ff6a5c, #d26a8b);
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
            color: #fff;
        }
        table {
            width: 70%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            background-color: rgba(94, 173, 246, 0.8);
        }
        th, td {
            padding: 15px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #ff6a5c;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #8ebef6;
        }
        tr:hover {
            background-color: #ff9a8b;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #ffffff;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

    <h1>Quotes to Scrape</h1>
    <div style="display: flex; justify-content: center; align-items: ce;">
        <table>
        </table>
    </div>

</body>
</html>
"""

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
    jsonFile.close()

    parser = BeautifulSoup(html_simple, features="html.parser")
    jsonFile = json.load(open("data.json", "r", encoding="utf-8"))

    
    table = parser.table
    head_element = parser.new_tag("th")
    head_element.string = "Quotes"
    header_table = parser.new_tag("tr")
    header_table.append(head_element)
    head_element = parser.new_tag("th")
    head_element.string = "Author"
    header_table.append(head_element)
    table.append(header_table)
    for json_object in jsonFile:
        table_element_parent = parser.new_tag("tr")
        teacher_name = parser.new_tag("td")
        teacher_post = parser.new_tag("td")
        teacher_name.string = json_object['Quote']
        teacher_post.string = json_object['Author']
        table_element_parent.append(teacher_name)
        table_element_parent.append(teacher_post)
        table.append(table_element_parent)
    data_original = parser.new_tag("tr")
    data_text = parser.new_tag("th")
    data_text.string = "Оригинальный источник"
    data_original.append(data_text)
    data_text = parser.new_tag("th")
    link = parser.new_tag("a", href=url)
    link.string = "Перейти"
    data_text.append(link)
    data_original.append(data_text)
    table.append(data_original)
    with open("index.html", "w", encoding='utf-8') as index:
        index.write(parser.prettify(formatter="minimal"))
else:
    print(f"Ошибка {response.status_code}: Не удалось получить страницу.")