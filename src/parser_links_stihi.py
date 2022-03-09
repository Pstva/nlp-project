# записывает все стихи для введенного года и месяцев

import requests
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


# вовзращает html-страницу
def get_html(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return None



# находит ссылки на все страницы со стихами в данный день
def get_all_pages_links(html, url):    
    pages_links = []
    soup = BeautifulSoup(html, 'html.parser')
    pages_part = soup.find("div", class_="nounline")
    if pages_part:
        pages = pages_part.find_all("a")
        for page in pages:
            link = page.get("href")
            pages_links.append(f'https://www.stihi.ru{link}'.strip())
            return pages_links
    return [url]
    
    
# генератор, возвращает ссылки на все стихи со всех страниц за определенный день  
def get_all_links(pages_links, year, month, day):
    for page_link in pages_links:
        html = get_html(page_link)
        if html is None:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        anonses = soup.find("div", class_="anonses")
        if anonses:
            _ = anonses.extract()  # убираем авторские анонсы - стихи за другие года
        uls = soup.find_all("ul", type="square")
        for ul in uls:
            lis = ul.find_all("li")
            for li in lis:
                a = li.find('a', class_='poemlink').get('href')
                # а тут еще раз убираем авторские анонсы, если они помечены тем же тегом
                if a.startswith(f'/{year}/{month}/{day}'):
                    yield "https://www.stihi.ru" + a


# достает стих и его название, дату публикации, имя автора и ссылку на страницу автора, пишет в csv-файл
def extract_poem(url, file_to_write):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        div_part = soup.find('div', class_="text")
        if div_part:
            text = div_part.text
            author = soup.find("div", class_="titleauthor").find("a").text
            author_link = 'https://www.stihi.ru' + soup.find("div", class_="titleauthor").find("a").get("href")
            title = soup.find("h1").text
            d = {'url': url,  'author': author, 'author_link': author_link, 'title': title.strip(), 'text': text.strip()}
            write_csv(d, file_to_write)
    
    
# записывает стих в csv-файл
def write_csv(data, file_to_write):
    with open(file_to_write, 'a') as f:
        writer = csv.writer(f, lineterminator="\r")
        writer.writerow((data['url'],
                         data['author'],
                         data['author_link'],
                         data['title'],
                         data['text']))
                    
                
# парсит все стихи за день из определенной рубрики                               
def parse_one_day(year, month, day, topic_n, output_file):
    link = f'https://www.stihi.ru/poems/list.html?topic={topic_n}&year={year}&month={month}&day={day}'
    first_topic_html = get_html(link)
    if first_topic_html:    
        all_pages = get_all_pages_links(first_topic_html, link)
        all_links = get_all_links(all_pages, year, month, day)
        for poem_link in all_links:
            try:
                extract_poem(poem_link, output_file)
            except UnicodeError:
                continue
    
    
# парсит все стихи за год из определенной рубрики 
def parse_year(year, topic_n, output_file):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if int(year) % 4 == 0:
        days_in_months[1] = 29
    for month_n in tqdm(range(12)):
        for day in range(1, days_in_months[month_n] + 1):
            month = month_n + 1
            parse_one_day(year, f'{month:02}', f'{day:02}', topic_n, output_file)


def main(args):
    print(f'parsing {args.year} year, {args.topic} topic')
    parse_year(args.year, args.topic, args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", required=True)
    parser.add_argument("-t", "--topic", required=True)
    parser.add_argument("-o", "--output-file", required=True)
    args = parser.parse_args()
    main(args)
    
