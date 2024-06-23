import pandas as pd
from enum import Enum
import io
import requests

_EXCHANGE_LIST = ['nyse', 'nasdaq', 'amex']

_SECTORS_LIST = set(['Consumer Non-Durables', 'Capital Goods', 'Health Care',
       'Energy', 'Technology', 'Basic Industries', 'Finance',
       'Consumer Services', 'Public Utilities', 'Miscellaneous',
       'Consumer Durables', 'Transportation'])


# headers and params used to bypass NASDAQ's anti-scraping mechanism in function __exchange2df
headers = {
    'authority': 'old.nasdaq.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://github.com/shilewenuw/get_all_tickers/issues/2',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'AKA_A2=A; NSC_W.TJUFEFGFOEFS.OBTEBR.443=ffffffffc3a0f70e45525d5f4f58455e445a4a42378b',
}

def params(exchange):
    return (
        ('letter', '0'),
        ('exchange', exchange),
        ('render', 'download'),
    )

def params_region(region):
    return (
        ('letter', '0'),
        ('region', region),
        ('render', 'download'),
    )

# I know it's weird to have Sectors as constants, yet the Regions as enums, but
# it makes the most sense to me
class Region(Enum):
    AFRICA = 'AFRICA'
    EUROPE = 'EUROPE'
    ASIA = 'ASIA'
    AUSTRALIA_SOUTH_PACIFIC = 'AUSTRALIA+AND+SOUTH+PACIFIC'
    CARIBBEAN = 'CARIBBEAN'
    SOUTH_AMERICA = 'SOUTH+AMERICA'
    MIDDLE_EAST = 'MIDDLE+EAST'
    NORTH_AMERICA = 'NORTH+AMERICA'

class SectorConstants:
    NON_DURABLE_GOODS = 'Consumer Non-Durables'
    CAPITAL_GOODS = 'Capital Goods'
    HEALTH_CARE = 'Health Care'
    ENERGY = 'Energy'
    TECH = 'Technology'
    BASICS = 'Basic Industries'
    FINANCE = 'Finance'
    SERVICES = 'Consumer Services'
    UTILITIES = 'Public Utilities'
    DURABLE_GOODS = 'Consumer Durables'
    TRANSPORT = 'Transportation'


# get tickers from chosen exchanges (default all) as a list
def get_tickers(NYSE=True, NASDAQ=True, AMEX=True):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__exchange2list('nyse'))
    if NASDAQ:
        tickers_list.extend(__exchange2list('nasdaq'))
    if AMEX:
        tickers_list.extend(__exchange2list('amex'))
    return tickers_list


def get_tickers_filtered(mktcap_min=None, mktcap_max=None, sectors=None,country=None):
    tickers_list = []
    for exchange in _EXCHANGE_LIST:
        tickers_list.extend(__exchange2list_filtered(__exchange2df(exchange,country), mktcap_min=mktcap_min, mktcap_max=mktcap_max, sectors=sectors))
        break
    return tickers_list


def get_biggest_n_tickers(top_n,minPrice=0, sectors=None,Tilist='all_tickers.csv'):
    df = pd.DataFrame()
    for exchange in _EXCHANGE_LIST:
        temp = __exchange2df(exchange,country=None,Tilist=Tilist)
        df = pd.concat([df, temp])
        break
        
    df = df.dropna(subset={'Market Cap'})
    df = df[~df['Symbol'].str.contains("\.|\^",na=False)]

    if sectors is not None:
        if isinstance(sectors, str):
            sectors = [sectors]
        if not _SECTORS_LIST.issuperset(set(sectors)):
            raise ValueError('Some sectors included are invalid')
        sector_filter = df['Sector'].apply(lambda x: x in sectors)
        df = df[sector_filter]

    def cust_filter(mkt_cap):
        mkt_cap=str(mkt_cap)
        if 'M' in mkt_cap:
            return float(mkt_cap[1:-1])
        elif 'B' in mkt_cap:
            return float(mkt_cap[1:-1]) * 1000
        else:
            return float(mkt_cap) / 1e6

    df['Market Cap'] = df['Market Cap'].apply(cust_filter)
    df['Last Sale']=df['Last Sale'].str.removeprefix('$').replace(',', '', regex=False).astype(float)
    df['NoShares']=df['Market Cap']/df['Last Sale']
    df=df[df['Last Sale']>minPrice]

    df = df.sort_values('Market Cap', ascending=False)
    if top_n > len(df):
        raise ValueError('Not enough companies, please specify a smaller top_n')
    print('Minimum market cap='+str(df.iloc[top_n,5]))
    df =df.set_index('Symbol')
    return df.iloc[:top_n][['NoShares','Last Sale']]


def get_tickers_by_region(region, mktcap_min=None, mktcap_max=None, country=None):
    if region in Region:
        #response = requests.get('blob:https://old.nasdaq.com/screening/companies-by-region.aspx', headers=headers,                                params=params_region(region))
        #data = io.StringIO(response.text)
        df = pd.read_csv('Europ_tickers.csv', sep=",")
        #df = pd.read_csv(data, sep=",")
        if country!=None:
            df=df[df['Country']==country]
        #df.to_csv("Alltickers1.csv")
        return __exchange2list_filtered(df,mktcap_min,mktcap_max)
    else:
        raise ValueError('Please enter a valid region (use a Region.REGION as the argument, e.g. Region.AFRICA)')

def __exchange2df(exchange,country,Tilist='all_tickers.csv'):
    #response = requests.get('blob:https://www.nasdaq.com/3c801a62-9221-49be-9ec7-80a8e0c3a40a', headers=headers)
    #print(response.url)
    #data = io.StringIO(response.text)
    df = pd.read_csv(Tilist, sep=",")
    if country!=None:
        df=df[df['Country']==country]
    #df = pd.read_csv(data, sep=",")
    #df.to_csv("Alltickers2.csv")
    return df

# def __exchange2list(exchange):
#     df = __exchange2df(exchange)
#     # removes weird tickers
#     df_filtered = df[~df['Symbol'].str.contains("\.|\^")]
#     return df_filtered['Symbol'].tolist()

# market caps are in millions
def __exchange2list_filtered(df, mktcap_min=None, mktcap_max=None, sectors=None):
    df = df.dropna(subset={'Market Cap'})
    df = df[~df['Symbol'].str.contains("\.|\^",na=False)]

    if sectors is not None:
        if isinstance(sectors, str):
            sectors = [sectors]
        if not _SECTORS_LIST.issuperset(set(sectors)):
            raise ValueError('Some sectors included are invalid')
        sector_filter = df['Sector'].apply(lambda x: x in sectors)
        df = df[sector_filter]

    def cust_filter(mkt_cap):
        mkt_cap=str(mkt_cap)
        if 'M' in mkt_cap:
            return float(mkt_cap[1:-1])
        elif 'B' in mkt_cap:
            return float(mkt_cap[1:-1]) * 1000
        else:
            return float(mkt_cap) / 1e6
    df['Market Cap'] = df['Market Cap'].apply(cust_filter)
    if mktcap_min is not None:
        df = df[df['Market Cap'] > mktcap_min]
    if mktcap_max is not None:
        df = df[df['Market Cap'] < mktcap_max]
    return df['Symbol'].tolist()


# save the tickers to a CSV
def save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv'):
    tickers2save = get_tickers(NYSE, NASDAQ, AMEX)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)

def save_tickers_by_region(region, filename='tickers_by_region.csv'):
    tickers2save = get_tickers_by_region(region)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)


if __name__ == '__main__':

    # tickers of all exchanges
    tickers = get_tickers()
    print(tickers[:5])

    # tickers from NYSE and NASDAQ only
    tickers = get_tickers(AMEX=False)

    # default filename is tickers.csv, to specify, add argument filename='yourfilename.csv'
    save_tickers()

    # save tickers from NYSE and AMEX only
    save_tickers(NASDAQ=False)

    # get tickers from Asia
    tickers_asia = get_tickers_by_region(Region.ASIA)
    print(tickers_asia[:5])

    # save tickers from Europe
    save_tickers_by_region(Region.EUROPE, filename='EU_tickers.csv')

    # get tickers filtered by market cap (in millions)
    filtered_tickers = get_tickers_filtered(mktcap_min=500, mktcap_max=2000)
    print(filtered_tickers[:5])

    # not setting max will get stocks with $2000 million market cap and up.
    filtered_tickers = get_tickers_filtered(mktcap_min=2000)
    print(filtered_tickers[:5])

    # get tickers filtered by sector
    filtered_by_sector = get_tickers_filtered(mktcap_min=200e3, sectors=SectorConstants.FINANCE)
    print(filtered_by_sector[:5])

    # get tickers of 5 largest companies by market cap (specify sectors=SECTOR)
    top_5 = get_biggest_n_tickers(5)
    print(top_5)