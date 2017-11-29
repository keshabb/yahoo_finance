#!/usr/bin/env python


import requests
import os
import sys
from bs4 import BeautifulSoup
import pandas as pd
import click


def get_summary(ticker):
    """ Get summary data of Ticker """
    SUMMARY = 'https://finance.yahoo.com/quote/{}'.format(ticker)
    page = requests.get(SUMMARY)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('tr')
    summary = {}
    for item in data:
        if item('td')[0].get_text() == '':
            continue
        summary.update({item('td')[0].get_text(): item('td')[1].get_text()})
    pd.set_option("display.colheader_justify","left")
    df = pd.Series(summary)
    click.echo(click.style("Summary", fg='red', bold=True, underline=True))
    click.echo("{}".format(df))
    click.pause(info='Press any key to continue ...', err=False)


def get_stats(ticker):
    """ Get statistics of ticker """

    STATS = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(ticker, ticker)
    page = requests.get(STATS)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('tr')
    stats = {}
    for item in data:
        if item('td')[0].get_text() == '':
            continue
        stats.update({item('td')[0].get_text(): item('td')[1].get_text()})
    df = pd.Series(stats)
    click.echo(click.style("Stats", fg='red', bold=True, underline=True))
    click.echo("{}".format(df))
    #print "{}: {}".format(item('td')[0].get_text(), item('td')[1].get_text())
    click.pause(info='Press any key to continue ...', err=False)


def get_profile(ticker):
    """ get company profile data """
    PROFILE = 'https://finance.yahoo.com/quote/{}/profile?p={}'.format(ticker, ticker)

    page = requests.get(PROFILE)
    soup = BeautifulSoup(page.content, 'html.parser')
    company_name = soup.find('h3', attrs={'class': "Mb(10px)"})
    company = soup.find('div', attrs={'class': "Mb(35px)"})
    click.echo(click.style("Profile", fg='red', bold=True, underline=True))
    profile = {}
    dic_key = []
    dic_val = []
    if company_name is not None:
        print company_name.get_text().encode('utf-8')
        company = soup.find('div', attrs={'class': "Mb(35px)"})
        info_2 = company.find('p', attrs={'class': "D(ib) Va(t)"})
        title = info_2.find_all('span')
        value = info_2.find_all('strong')
        for d in title:
            dic_key.append(d.get_text())
        for d in value:
            dic_val.append(d.get_text())
        comp_info = dict(zip(dic_key, dic_val))
        df = pd.Series(comp_info)
        print df
    data = soup.find_all('tr')
    name = []
    title = []
    pay = []
    age = []
    for item in data:
        if not item('td') or item('td')[0].get_text() == '':
            continue
        name.append(item('td')[0].get_text().strip().encode('utf-8'))
        title.append(item('td')[1].get_text().strip().encode('utf-8'))
        pay.append(item('td')[2].get_text().strip().encode('utf-8'))
        age.append(item('td')[4].get_text().strip().encode('utf-8'))
    profile.update({"Name": name, "Title": title, "Pay": pay, "Age": age})
    pd.set_option("display.colheader_justify","right")
    pd.set_option('display.width', 120)
    df = pd.DataFrame(profile)
    df.style.set_properties(**{'text-align': 'right'})
    print(df)
        #print "Name: {}, Title: {}, Pay: {}, Age: {}".format(item('td')[0].get_text().encode('utf-8'), 
        #      item('td')[1].get_text().encode('utf-8'), item('td')[2].get_text().encode('utf-8'), item('td')[4].get_text().encode('utf-8'))
    click.pause(info='Press any key to continue ...', err=False)


def get_financials(ticker):
    """ Get financial data """

    FINANCIALS = 'https://finance.yahoo.com/quote/{}/financials?p={}'.format(ticker, ticker)
    page = requests.get(FINANCIALS)
    soup = BeautifulSoup(page.content, 'html.parser')
 #   data = soup.find_all('tr')
    #income_statement = soup.find_all('h3', attrs={'class': "D(ib) Fz(20px) Fw(b)"})
    #income_statement = income_statement[0].get_text()
    click.echo(click.style("Income Statement", fg='red', bold=True, underline=True))
    table = soup.find('table', attrs={'class': "Lh(1.7) W(100%) M(0)"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        #if len(cols) == 1:
        #    print cols[0].get_text()
        #    continue
        #print "{} {} {}".format(row.get(row[0], '').get_text(), row.get(row[1], '').get_text(), row.get(row[2], '').get_text())
        #print "{} {} {}".format(row.get(row[0], ''), row.get(row[1], ''), row.get(row[2], ''))
        #for item in row:
        #    print "{}".format(item.get_text())
        cols = [ele.text.strip() for ele in cols] 
        data.append([ele for ele in cols if ele])
    pd.set_option("display.colheader_justify","left")
    income_data = pd.DataFrame(data=data, columns=['','','',''])
    #income_data.style.set_properties(**{'text-align': 'left'})
    print income_data
    #for row in data:
    #    print "{}".format(row)
#    for item in data:
#        if not item('td') or item('td')[0].get_text() == '':
#            continue
        #for i in item:
        #    print "Sub item: {}".format(i.get_text())
        #print "{}: {}".format(item('td')[0].get_text(), item('td')[1].get_text())
#        print "Item:{}, Item2: {}".format(item('td')[0].get_text(), item('td'))
    click.pause(info='Press any key to continue ...', err=False)


def get_balance_sheets(ticker):
    """ Get balance sheets """
    BALANCE_SHEET = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'.format(ticker, ticker)
    page = requests.get(BALANCE_SHEET)
    soup = BeautifulSoup(page.content, 'html.parser')
    #balance_sheet = soup.find_all('h3', attrs={'class': "D(ib) Fz(20px) Fw(b)"})
    #print("{}".format(balance_sheet[0].get_text()))
    click.echo(click.style("Balance Sheets", fg='red', bold=True, underline=True))
    table = soup.find('table', attrs={'class': "Lh(1.7) W(100%) M(0)"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    balancesheet_data = pd.DataFrame(data=data, columns=['','','',''])
    print balancesheet_data
    click.pause(info='Press any key to continue ...', err=False)


def get_cash_flow(ticker):
    """ Get cash flow """
    CASH_FLOW = 'https://finance.yahoo.com/quote/{}/cash-flow?p={}'.format(ticker, ticker)
    page = requests.get(CASH_FLOW)
    soup = BeautifulSoup(page.content, 'html.parser')
    #cashflow = soup.find_all('h3', attrs={'class': "D(ib) Fz(20px) Fw(b)"})
    #print("{}".format(cashflow[0].get_text()))
    click.echo(click.style("Cash Flow", fg='red', bold=True, underline=True))
    table = soup.find('table', attrs={'class': "Lh(1.7) W(100%) M(0)"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    cashflow_data = pd.DataFrame(data=data, columns=['','','',''])
    print cashflow_data
    click.pause(info='Press any key to continue ...', err=False)

def get_options(ticker):
    """ Get options data """
    OPTIONS = 'https://finance.yahoo.com/quote/{}/options?p={}'.format(ticker, ticker)

    page = requests.get(OPTIONS)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("Calls")
    table = soup.find('table', attrs={'class': "calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"})
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    options_call_data = pd.DataFrame(data=data)
    print options_call_data
    print("Puts")
    table = soup.find('table', attrs={'class': "puts table-bordered W(100%) Pos(r) list-options"})
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    options_put_data = pd.DataFrame(data=data)
    print options_put_data
    click.pause(info='Press any key to continue ...', err=False)


def get_holders(ticker):
    """ Get holders info """
    # More work not working
    HOLDERS = 'https://finance.yahoo.com/quote/{}/holders?p={}'.format(ticker, ticker)
    page = requests.get(HOLDERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    #holders = soup.find_all('h3', attrs={'class': "D(ib)"})
    #print("{}".format(holders[0].get_text()))
    click.echo(click.style("Holders", fg='red', bold=True, underline=True))
    table = soup.find('table', attrs={'class': "Lh(1.7) W(100%) M(0)"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    cashflow_data = pd.DataFrame(data=data)
    print cashflow_data
    data = soup.find_all('tr')
    for item in data:
        print "{}: {}".format(item('td')[0].get_text(), item('td')[1].get_text())
    click.pause(info='Press any key to continue ...', err=False)

def get_history(ticker):
    """ Get history """
    HISTORY = 'https://finance.yahoo.com/quote/{}/history?p={}'.format(ticker, ticker)
    data = []
    page = requests.get(HISTORY)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': "W(100%) M(0)"})
    thead = table.find('thead')
    thead_rows = thead.find_all('tr')
    for row in thead_rows:
        cols = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    table_body = table.find('tbody')
    tbody_rows = table_body.find_all('tr')
    for row in tbody_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    history_data = pd.DataFrame(data=data, columns=['','','','','','',''])

    print history_data
    click.pause(info='Press any key to continue ...', err=False)


def get_analysts(ticker):
    """ Get analyst info """
    # More work to do for analysts rating and average price for stock
    ANALYSTS = 'https://finance.yahoo.com/quote/{}/analysts?p={}'.format(ticker, ticker)
    page = requests.get(ANALYSTS)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        analysts_data = pd.DataFrame(data=data)
        print analysts_data
    click.pause(info='Press any key to continue ...', err=False)


@click.command()
@click.argument('symbol', nargs=1)
def get_info_yahoo(symbol):
    get_summary(symbol)
    get_stats(symbol)
    get_profile(symbol)
    get_financials(symbol)
    get_balance_sheets(symbol)
    get_cash_flow(symbol)
    get_options(symbol)
    #get_holders(symbol)
    get_history(symbol)
    get_analysts(symbol)


if __name__ == '__main__':
    sys.exit(get_info_yahoo())


