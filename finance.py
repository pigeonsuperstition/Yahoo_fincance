##input: name,start_date,end_date
##outpit: the price of the stock in that period of time
import requests
from bs4 import BeautifulSoup
import csv
import time
def get_soup(html):
    try:
        print('正在请求: '+html)
        response = requests.get(html,timeout=5).text
        soup = BeautifulSoup(response,'lxml')
        return soup
    except:
        print('请求'+html+'失败,即将重试')
        get_soup(html)
def get_csv(soup,end_date):
    l = {}
    for tr in (soup.select('tr')):
        temp_l = []
        for span in (tr.select('span')):
            temp_l.append(span.get_text())
        if temp_l[0]!='Date' and temp_l[0]!='*Close price adjusted for splits.' :
            dt_obj = time.strptime(temp_l[0], '%b %d, %Y')
            t = time.strftime('%Y-%m-%d', dt_obj)
            if end_date<=t:
                l[t]=temp_l[1:]
            else:return l
    return l
def get_html(name,end_date,start_date,frequency):
    url1 = 'https://finance.yahoo.com/quote/'+name+'/history?'
    url2 = 'period1='+str(end_date)+'&'
    url3 = 'period2='+str(start_date)+'&interval=1d&filter=history&frequency='+frequency
    return url1+url2+url3
def get_date(name,start_date,frequency,interval=125):
    end_date = start_date-(interval-1)*86400
    return end_date
def get_all(name,start_date,end_date,frequency,interval=125):
    start_date = time.strptime(str(start_date),"%Y-%m-%d")
    start_date = int(time.mktime(start_date))
    end_date2 = time.strptime(str(end_date), "%Y-%m-%d")
    end_date2 = int(time.mktime(end_date2))
    timing = (start_date-end_date2)/86400
    if timing%125>0:
        timing = timing//125+1
    else:
        timing = timing//125
    i = 0
    data={}
    while i<timing:
        end_date2=get_date(name,start_date,frequency,interval)
        html = get_html(name,end_date2,start_date,frequency)
        soup = get_soup(html)
        data.update(get_csv(soup,end_date))
        start_date = end_date2-86400
        i+=1
    return data
def write_to_csv(ID,data):
    filename='CsvFileFor'+ID+'.csv'
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    for i in data:
        writer.writerow([i]+data[i])
def get_finance_and_write2csv(name,start_date,end_date,frequency='1d'):
    data = get_all(name,start_date,end_date,frequency)
    write_to_csv(name, data)
if __name__ == '__main__':
    get_finance_and_write2csv('AAPL','2018-03-06','2017-03-07')
