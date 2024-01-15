import urllib.request
import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd
import numpy as np
import os


def get_daily_snp500_first():
    url = "https://www.gurufocus.com/economic_indicators/150/sp-500-dividend-yield"
    response = requests.get(url)
    html_content = response.text.replace('<!---->', '')

    date = ''
    value = ''
    soup = BeautifulSoup(html_content, 'html.parser')
    table_element = soup.find_all('table', attrs={'class': 'data-table normal-table'}, recursive=True)
    if table_element:
        date = table_element[0].find('tr', attrs={'id': '0'}).get_text(strip=True)
        value_element = table_element[1].find('tr', attrs={'id': '0'})
        value = value_element.find('td', {'data-column': 'Value'}).find('span').get_text(strip=True)
    else:
        print("Table element not found.")

    return date, value


def get_daily_snp500_second():
    url = "https://www.multpl.com/s-p-500-dividend-yield/table/by-year"
    response = requests.get(url)
    html_content = response.text

    value = ''
    soup = BeautifulSoup(html_content, 'html.parser')
    table_element = soup.find('table', attrs={'id': 'datatable'})
    if table_element:
        tr_element = table_element.find('tr', attrs={'class': 'odd'})
        td_element = tr_element.find_all('td', recursive=True)
        td_element[1].find('abbr').decompose()
        value = td_element[1].get_text(strip=True)
    else:
        print("Table element not found.")

    return value


def get_tip():
    period1 = datetime.datetime.now() - datetime.timedelta(days=365)
    period1.timetuple()
    period1 = str(round(time.mktime(period1.timetuple())))

    period2 = str(round(time.time()))

    file_url = "https://query1.finance.yahoo.com/v7/finance/download/TIP?period1=" + period1 + \
               "&period2=" + period2 + "&interval=1d&events=history&includeAdjustedClose=true"
    urllib.request.urlretrieve(file_url, 'tip.csv')

    df = pd.read_csv('tip.csv')

    # TIP 물가연동채 13612U 모멘텀이 마이너스인 경우 방어 자산으로 전환 (1달은 21일)
    # 13612U 모멘텀 =((p0/p1–1)+(p0/p3–1)+(p0/p6–1)+(p0/p12–1))/4
    p0 = df['Close'][0]
    p1 = df['Close'][len(df) - 1 - (21 * 1)]
    p3 = df['Close'][len(df) - 1 - (21 * 3)]
    p6 = df['Close'][len(df) - 1 - (21 * 6)]
    p12 = df['Close'][len(df) - 1]

    tip_momentum_13612u = ((p0 / p1 - 1) + (p0 / p3 - 1) + (p0 / p6 - 1) + (p0 / p12 - 1)) / 4
    tip_momentum_13612u = np.trunc(tip_momentum_13612u * 1000000) / 1000000
    tip_momentum_13612u = format(tip_momentum_13612u, '.6f')

    tip_momentum_12sva = df['Close'][0] / np.mean(df['Close']) - 1
    tip_momentum_12sva = np.trunc(tip_momentum_12sva * 1000000) / 1000000
    tip_momentum_12sva = format(tip_momentum_12sva, '.6f')

    try:
        os.remove('tip.csv')
        print(f"tip.csv 파일이 삭제되었습니다.")
    except OSError as e:
        print(f"파일 삭제 실패: {e}")

    return tip_momentum_13612u, tip_momentum_12sva


def get_bil():
    period1 = datetime.datetime.now() - datetime.timedelta(days=183)
    period1.timetuple()
    period1 = str(round(time.mktime(period1.timetuple())))
    period2 = str(round(time.time()))

    file_url = "https://query1.finance.yahoo.com/v7/finance/download/BIL?period1=" + period1 + "&period2=" + period2 + \
               "&interval=1d&events=history&includeAdjustedClose=true"
    urllib.request.urlretrieve(file_url, 'bil.csv')

    df = pd.read_csv('bil.csv')
    bil_mean = np.mean(df['Close'])
    bil_momentum = bil_mean - df['Close'][0]
    bil_momentum = np.trunc(bil_momentum * 1000000) / 1000000
    bil_momentum = format(bil_momentum, '.6f')

    try:
        os.remove('bil.csv')
        print(f"bil.csv 파일이 삭제되었습니다.")
    except OSError as e:
        print(f"파일 삭제 실패: {e}")

    return bil_momentum


def get_tlt():
    period1 = datetime.datetime.now() - datetime.timedelta(days=183)
    period1.timetuple()
    period1 = str(round(time.mktime(period1.timetuple())))
    period2 = str(round(time.time()))

    file_url = "https://query1.finance.yahoo.com/v7/finance/download/TLT?period1=" + period1 + "&period2=" + period2 + \
               "&interval=1d&events=history&includeAdjustedClose=true"
    urllib.request.urlretrieve(file_url, 'tlt.csv')

    df = pd.read_csv('tlt.csv')
    tlt_mean = np.mean(df['Close'])
    tlt_momentum = tlt_mean - df['Close'][0]
    tlt_momentum = np.trunc(tlt_momentum * 1000000) / 1000000
    tlt_momentum = format(tlt_momentum, '.6f')

    try:
        os.remove('tlt.csv')
        print(f"tlt.csv 파일이 삭제되었습니다.")
    except OSError as e:
        print(f"파일 삭제 실패: {e}")

    return tlt_momentum


def get_pdbc():
    period1 = datetime.datetime.now() - datetime.timedelta(days=183)
    period1.timetuple()
    period1 = str(round(time.mktime(period1.timetuple())))
    period2 = str(round(time.time()))

    file_url = "https://query1.finance.yahoo.com/v7/finance/download/PDBC?period1=" + period1 + "&period2=" + period2 +\
               "&interval=1d&events=history&includeAdjustedClose=true"
    urllib.request.urlretrieve(file_url, 'pdbc.csv')

    df = pd.read_csv('pdbc.csv')
    pdbc_mean = np.mean(df['Close'])
    pdbc_momentum = pdbc_mean - df['Close'][0]
    pdbc_momentum = np.trunc(pdbc_momentum * 1000000) / 1000000
    pdbc_momentum = format(pdbc_momentum, '.6f')

    try:
        os.remove('pdbc.csv')
        print(f"pdbc.csv 파일이 삭제되었습니다.")
    except OSError as e:
        print(f"파일 삭제 실패: {e}")

    return pdbc_momentum


def init():
    current_directory = os.getcwd()
    print(f"현재 작업 디렉토리: {current_directory}")

    file_dir = f'{current_directory}/data'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    date, snp500_value_first = get_daily_snp500_first()
    snp500_value_second = get_daily_snp500_second()
    tip_momentum_13612u, tip_momentum_12sva = get_tip()
    bil_momentum = get_bil()
    tlt_momentum = get_tlt()
    pdbc_momentum = get_pdbc()

    with open(f'{file_dir}/result.csv', 'a', encoding='utf-8') as file:
        file.write(f'{date},{snp500_value_first},{snp500_value_second},{tip_momentum_13612u},{tip_momentum_12sva},'
                   f'{bil_momentum},{tlt_momentum},{pdbc_momentum}\n')


if __name__ == '__main__':
    init()
