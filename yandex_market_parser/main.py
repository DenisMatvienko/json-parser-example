import requests
from bs4 import BeautifulSoup
import csv

""" Simple example with json data pars """


headers = {"Accept":"application/json, text/javascript, */*; q=0.01",
           "Accept-Encoding":"gzip, deflate, br","Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",""
           "Connection":"keep-alive",
           "Cookie":"spravka=dD0xNTc2MTgxMTUwO2k9MzEuMTM0LjE5MS4xNTE7dT0xNTc2MTgxMTUwNDk0MTMwMDMzO2g9YzRhNmYwZTJlNDY"
                    "xNGFhNTRiZjAyNGFlZjdlY2I5MmM=; i=c8m8x7OOMbgGwyghQicnmvRydXbvu8LqlsMjcf3mpvhUkqDzJmc8HpgtbKqu6k"
                    "AUbZfVgZukKE4058gSU2BC01EiHMA=; _ym_uid=1576181121106319950; mda=0; yandexuid=6927524791576181121;"
                    " yp=1891541121.yrts.1576181121#1891541121.yrtsi.1576181121#1578773156.ygu.1#1607865071."
                    "p_sw.1576329071#1577480195.szm.1_25%3A1536x864%3A1536x750#1576961795.ln_tp.01;"
                    " skid=9284437371576181156; visits=1576181156-1576438312-1576875394; cmp-merge=true;"
                    " reviews-merge=true; yandex_gid=2; yabs-frequency=/4/00020000000wolHT/j5ImSCWu87poFMt0E2S0/;"
                    " zm=m-white_bender.webp.css-https%3As3home-static_K0Q0oZhsq7a3-CW5bfauGUiWjq0%3Al;"
                    " _ym_d=1576181159; currentRegionId=2; currentRegionName=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82"
                    "-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3; categoryQA=1; ys=wprid.1576875394950100"
                    "-624358466674566908811235-man1-3526; _ym_wasSynced=%7B%22time%22%3A1576875398012%2C%22"
                    "params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; market_ys=1576875391175878"
                    "-819827222414667225500125-man1-5746; parent_reqid_seq=55812cc8d1ff9e120c1a55cccc"
                    "28fa96%2Ccde52a98bbbf3eac053f3e15fe7ab74f%2C4dc68cd599eaddc3300229f78efb62a1%2Cfbb774dc85261"
                    "5cc05d8dc181015281b; pof=%7B%22clid%22%3A%5B%22703%22%5D%2C%22mclid%22%3Anull%2C%22distr_type"
                    "%22%3Anull%2C%22vid%22%3Anull%2C%22opp%22%3Anull%7D; cpa-pof=%7B%22clid%22%3A%5B%22703%22%5D%"
                    "2C%22mclid%22%3Anull%2C%22distr_type%22%3Anull%2C%22vid%22%3Anull%2C%22opp%22%3Anull%7D;"
                    " uid=AABixV39NYLCigEABot4Ag==; js=1; dcm=1; _ym_isad=2; first_visit_time=2019-12-20T23%3A56%3A"
                    "37%2B03%3A00; ugcp=1; fonts-loaded=1; _ym_visorc_45411513=b; _ym_visorc_160656=b; yandexmarket=48",
           "Host":"market.yandex.ru",
           "Referer":"https://market.yandex.ru/catalog--dushevye-kabiny-i-ugolki/56372/list?text=%D0%B4%D1%83%D1%"
                     "88%D0%B5%D0%B2%D0%BE%D0%B5%20%D0%BE%D0%B1%D0%BE%D1%80%D1%83%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0"
                     "%B8%D0%B5&cvredirect=3&track=srch_visual&onstock=0&deliveryincluded=0&local-offers-"
                     "first=0&viewtype=list",
           "sk":"s6d890b48a8e065addbb6674b75b4268f",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
           "X-Requested-With":"XMLHttpRequest"}


def get_html(url):
    """ Get html"""
    r = requests.get(url, headers=headers)
    return r


def write_csv(data):
    """ Write file as wash_equipment.csv """
    with open('wash_equipment.csv', 'a') as f:
        order = ['name', 'url']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_articles(response):
    """ Loop items, get html data or json """
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['data']

    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('h3', class_='n-snippet-card2__title')
    return items


def get_page_data(items):
    """ Get text from items """
    for item in items:
        name = item.text.strip()
        url = item.find('a').get('href')

        data = {'name': name, 'url': url}
        write_csv(data)


def main():
    page = 1
    while True:
        url = 'https://market.yandex.ru/api/search?hid=91616&nid=56372&text=%D0%B4%D1%83%D1%88%D0%B5%D0%B2%D0%BE%' \
              'D0%B5%20%D0%BE%D0%B1%D0%BE%D1%80%D1%83%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5&track=srch' \
              '_ddl&onstock=0&deliveryincluded=0&local-offers-first=0&viewtype=list&page={}' \
              '&refererPageId=list'.format(str(page))
        print(url)
        articles = get_articles(get_html(url))
        if articles:
            get_page_data(articles)
            page += 1
        else:
            break


if __name__ == '__main__':
    main()