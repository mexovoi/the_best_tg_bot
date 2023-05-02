import asyncio
from bs4 import BeautifulSoup
import requests
import threading

import data.parsing_data as ps


async def update_cbr():
    cbr_resp = requests.get(ps.cbr_url)
    bs_cbr = BeautifulSoup(cbr_resp.text, "lxml")
    #избавиться от вылета из-за исключений
    indexes = bs_cbr.find_all('div', 'main-indicator_value')
    indexes_keys = ['Цель по инфляции', 'Инфляция за', 'Ключевая ставка', 'Ставка RUONIA']
    indexes_value_dates = bs_cbr.find_all('div', 'main-indicator_text')
    if (len(indexes_value_dates) == 0):
        ps.indexes_info = [indexes_keys[i] + " 🆘. Мы скоро решим эту проблему." for i in range(len(indexes_keys))]
        #print(ps.indexes_info)

        ps.bax_rates_info.append("🆘")
        ps.bax_rates_info.append("🆘")
        ps.euro_rates_info.append("🆘")
        ps.euro_rates_info.append("🆘")
    else:
        indexes_keys[1] += " " + indexes_value_dates[1].find('a').text.strip()
        indexes_keys[2] += " " + indexes_value_dates[2].find('a').text.strip()
        indexes_keys[3] += " " + indexes_value_dates[3].text.strip()
        ps.indexes_info = [indexes_keys[i] + ": " + indexes[i].text.strip() for i in range(len(indexes_keys))]
        #print(ps.indexes_info)

        rates_info = bs_cbr.find_all('div', 'col-md-2 col-xs-9 _right mono-num')
        ps.bax_rates_info.append(rates_info[2].text.strip())  # Вчера
        ps.bax_rates_info.append(rates_info[3].text.strip())  # Позавчера
        ps.euro_rates_info.append(rates_info[0].text.strip())  # Вчера
        ps.euro_rates_info.append(rates_info[1].text.strip())  # Позавчера

    #print(ps.euro_rates_info)
    #print(ps.bax_rates_info)
    #print('####################################################')


async def update_invest_ideas():
    invest_resp = requests.get(ps.invest_url)
    bs_invest = BeautifulSoup(invest_resp.text, 'lxml')

    invest_ideas = bs_invest.find_all('div', 'idea-item___3a4SC')
    for i in invest_ideas:
        values = [k.text.strip() for k in i.find_all('p', 'typo___oYDNK secondary-font___1x6NP bold___3ON5R')]
        ps.invest_ideas_info[values[0].strip()] = tuple(["Срок начала " + values[1][:-5] + str(int(values[1][-4:]) - 1),
                                                         "Срок конца " + values[1],
                                                         'Потенциальная доходность ' + values[2]])
        #print(values[0].strip(), ps.invest_ideas_info[values[0].strip()])

    #print('####################################################')


async def update_msc_stocks():
    stocks_msc_resp = requests.get(ps.stocks_msc_url)
    bs_stocks_msc = BeautifulSoup(stocks_msc_resp.text, 'lxml')

    stocks_table_ru = bs_stocks_msc.find('table', 'simple-little-table trades-table')

    for row in stocks_table_ru.find_all('tr')[1:]:
        values = row.find_all('td')
        ps.stocks_msc_info[tuple([values[2].text.strip(), values[3].text.strip()])] = tuple(
            [values[7].text.strip(), values[8].text.strip(), values[9].text.strip(), values[10].text.strip(),
             values[11].text.strip(), values[12].text.strip(), values[13].text.strip(), values[14].text.strip(),
             values[15].text.strip()])
        # (name, ticker) = (price, delta day, объем, delta week, delta month, ytd, delta year, капитализация млрд rub, капитализация млрд dollar)
        #print(tuple([values[2].text.strip(), values[3].text.strip()]),
        #      ps.stocks_msc_info[tuple([values[2].text.strip(), values[3].text.strip()])])

    #print('####################################################')


async def update_goods_and_crypto():
    goods_and_crypto_resp = requests.get(ps.goods_and_crypto_url)
    bs_goods_and_crypto = BeautifulSoup(goods_and_crypto_resp.text, 'lxml')

    tables_on_site = bs_goods_and_crypto.find_all('table', 'simple-little-table trades-table')
    goods_table = tables_on_site[0]
    crypto_table = tables_on_site[3]

    for row in goods_table.find_all('tr')[1:]:
        values = row.find_all('td')
        ps.goods_info[values[0].text.strip()] = tuple([values[2].text.strip(), values[3].text.strip()])
        #print(values[0].text.strip(), ps.goods_info[values[0].text.strip()])

    for row in crypto_table.find_all('tr')[1:]:
        values = row.find_all('td')
        ps.crypto_info[values[0].text.strip()] = tuple([values[2].text.strip(), values[3].text.strip()])
        #print(values[0].text.strip(), ps.crypto_info[values[0].text.strip()])


async def update_spb_stocks():
    page = 1

    while True:
        stocks_spb_resp = requests.get(ps.stocks_spb_url + str(page))
        page += 1

        bs_stocks_spb = BeautifulSoup(stocks_spb_resp.text, 'lxml')

        stocks_table_spb = bs_stocks_spb.find('table', 'simple-little-table trades-table')

        stocks_found_spb = stocks_table_spb.find_all('tr')

        if (len(stocks_found_spb) <= 1):
            break

        for row in stocks_table_spb.find_all('tr')[1:]:
            values = row.find_all('td')
            ps.stocks_spb_info[tuple([values[2].text.strip(), values[3].text.strip()])] = tuple(
                [values[6].text.strip(), values[7].text.strip(), values[8].text.strip(), values[9].text.strip(),
                 values[10].text.strip(), values[11].text.strip(), values[12].text.strip()])
            # (name, ticker) = (price, delta day, sales volume, delta week, delta month, ytd, delta year)
            #print(tuple([values[2].text.strip(), values[3].text.strip()]),
            #      ps.stocks_spb_info[tuple([values[2].text.strip(), values[3].text.strip()])])


async def update_economic_news():
    economic_news_resp = requests.get(ps.economic_news_irl)
    bs_economic_news = BeautifulSoup(economic_news_resp.text, 'lxml')

    economic_news = bs_economic_news.find_all('div', 'item item_image-mob js-category-item')

    for new in economic_news:
        message_tag = new.find('span', 'item__title rm-cm-item-text')
        message = ""
        strings_message = list(message_tag.stripped_strings)
        for k in range(len(strings_message)):
            message += strings_message[k]
            if k + 1 < len(strings_message):
                if strings_message[k + 1][0].isupper():
                    message += "\n"
                else:
                    message += " "

        ps.economic_news_info[message] = new.a['href']
        #print(message, ps.economic_news_info[message])


async def update_all():
    await update_cbr()
    await update_economic_news()
    await update_msc_stocks()
    await update_spb_stocks()
    await update_invest_ideas()
    await update_goods_and_crypto()