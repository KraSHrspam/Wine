from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import collections
import pandas
import argparse

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

today_date = datetime.datetime.now().year
foundation_date = 1920
company_age = today_date - foundation_date


def calculate_company_age():
    delta_new = company_age % 100
    if 21 > delta_new > 4:
        return "лет"
    delta_new = company_age % 10
    if delta_new == 1:
        return "год"
    elif 1 < delta_new < 5:
        return "года"
    return "лет"


parser = argparse.ArgumentParser(
    description='Запускает сайт с сортами вин. Автоматически заполняет название, цену, картинку, скидку и сорт винограда (Если он есть) напитка по таблице Excel.'
)
parser.add_argument(
    '-w', '--wines',
    default='wine.xlsx',
    help='Путь до таблицы с винами.'
)
args = parser.parse_args()


wine_raw_excel_data = pandas.read_excel(args.wines, keep_default_na=False)
wines_excel_data = wine_raw_excel_data.to_dict(orient="records")
template = env.get_template("template.html")
wines = collections.defaultdict(list)

for wine in wines_excel_data:
    wines[wine["Категория"]].append(wine)

rendered_page = template.render(
    age=company_age,
    years=calculate_company_age(),
    wines=wines
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
