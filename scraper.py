import requests
import lxml.html as html
import os 
import datetime

from requests.models import Response

XPATH_LINK_TO_ARTICLE = '//h3[@class = "title-container"]//a[@class = "title page-link" and starts-with(@href,"/")]/@href'
XPATH_TITLE = '//h1[@class = "titulo"]/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="modulos"]/p[@class = "contenido"]/text()'
HOME_URL = 'https://www.eltiempo.com'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                #elimina caracteres que puedan generar conflicto en el nombre del archivo
                title = title.replace('\"', '')
                title = title.replace('/', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')   
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            #me permite obtener el contenido de la pagina en forma de String
            #el decorde me permite obtener caracteres especiales como la ñ
            home = response.content.decode('utf-8')
            #transformo la pagina que obtuve en forma de string en html
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                notice_link = HOME_URL + link
                parse_notice(notice_link, today)    
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()