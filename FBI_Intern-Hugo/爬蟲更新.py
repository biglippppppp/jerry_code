import json
import requests
import time
import re
import os
import warnings
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import urllib


""" 初始化 """
# 忽略不安全連線警告
warnings.simplefilter('ignore', InsecureRequestWarning)

# 使用header偽裝成edge瀏覽器下瀏覽行為
headers = {'content-type': 'text/html; charset = UTF-8', 
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'
          }
''' config'''
pages = 5
brands = [['石二鍋',['餐廳']],['春水堂',['飲料店',"餐廳"]],['星巴克',['飲料店','咖啡店']],['摩曼頓',['運動運品店']]]
tag_list = ["飲料店", "餐廳", "書店", "百貨公司"]
keywords = ['品牌']
sleep_time = 5
fp_output = r'C:/Users/User/OneDrive/桌面Dell/富邦/result_{}_{}.json'
fp_job_status = r'C:/Users/User/OneDrive/桌面Dell/富邦/job_status_{}_{}.json'

def timer(func):
    def wrapper(*args, **kwargs):
        tic = time.time()
        value = func(*args, **kwargs)
        print('Time consumed: {} sec.'.format(time.time()-tic))
        return value
    return wrapper



class Merchant:
    def __init__(self, name, keyword, page):
        self.name = name
        self.page = page
        self.keyword = keyword
        self.get_html()
        self.parse_attr()
        
    
    def get_html(self):
        url = 'https://google.com/search?q="{}"+{}&start={}'.format(urllib.parse.quote(self.name), self.keyword, (self.page-1)*10)
        count = 0
        
        while count < 3:
            try:
                result = requests.get(url, verify=False, auth=('user', 'pass'), headers=headers)
                if result.status_code == 200:
                    self.html = result.text
                    break
                elif result.status_code == 429:
                    count = count+1
                    time.sleep(10*60)
            except:
                time.sleep(sleep_time)
                count = count+1
        else:
            raise ConnectionError('Cannot get the html')
    
    def parse_attr(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.soup = soup
        
        self.top_address = [element.text for element in soup.findAll('div', {'class':'sXLaOe'})]
        
        self.title_list = [element.find('h3').text for element in soup.findAll('div', {'class':'yuRUbf'})]
        self.summary_list = [element.text for element in soup.findAll('div', {'class':'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})]

    
    def to_dict(self, drop_html=True):
    
        result = {
                    'name' : self.name,
                    'top_address' : self.top_address,
                    'title_list' : self.title_list,
                    'summary_list' : self.summary_list,
                 }
        if not drop_html:
            result['html'] = self.html
        return result



sleep_time = 5 #每一頁要隔五秒
start_time = time.time()
tic = time.time()
toc = time.time()

for i, keyword in enumerate(keywords):
    if i != 0:
        time.sleep(30) #大量的話要久一點
    for page in range(1,pages+1,1):

        result = list()
        job_status = {'fail_list' : [], 'success_list' : [], 'todo': [sublist[0] for sublist in brands], 'done_count': 0}

        for brand in job_status['todo']:
            
            if time.time()-tic < sleep_time:
                time.sleep(sleep_time)
                
            tic = time.time()
            
            try:
                result.append(Merchant(brand, keyword, page).to_dict())
                job_status['success_list'].append(brand)
                
            except:
                job_status['fail_list'].append(brand)
            job_status['done_count'] += 1

            if job_status['done_count'] % 100 == 0: 
                
                print('Jobs done: {}\nTime consumed: {:.1f}\nTotal time consumed: {:.1f}'.format(job_status['done_count'], time.time()-toc, time.time()-start_time))
                print('Success count: {} Fail count: {}'.format(len(job_status['success_list']), len(job_status['fail_list'])))
                print('===========================================================================')
                toc = time.time()

        with open(fp_output.format(keyword, page), 'w') as f:
             f.write(json.dumps(result))
        with open(fp_job_status.format(keyword, page), 'w') as f:
            json.dump(job_status, f)
            
        print('Keyword: {}, page: {} done.'.format(keyword, page))
        print('===========================================================================')



#把爬下來的資料變成df
def create_summary_df(keyword_list:list, brands:list, pages:list):
    """
    input: keyword_list
           brand : 所有品牌的list(多維)，[0]為特店名，[1]為那個特店的label(list)
           pages : 搜尋頁數
    output:組合而成df
    """
    summary_df = pd.DataFrame()
    for keyword in keyword_list:
        for brand_index in range(len(brands)):
            for page in range(pages):
                with open(f'../result_{keyword}_{page+1}.json') as f:
                    data = json.load(f)
                for i in data[brand_index]["summary_list"]:
                    #去掉標點符號、日期
                    i = re.sub(r'\W', "", i)
                    i = re.sub(r'\d+年\d+月\d+日', "", i)
                tmp_df = pd.DataFrame({"summary":data[brand_index]["summary_list"]})
                tmp_df['name'] = [data[brand_index]["name"]] * len(tmp_df)
                tmp_df["category"] = [brands[brand_index][1]] * len(tmp_df)
                tmp_df["keyword"] = [keyword] * len(tmp_df)
                summary_df = pd.concat([summary_df,tmp_df])
    return summary_df
summary_df = create_summary_df(keywords, brands, pages)

#看這個特店的標籤是否有在所有label中，建立一個新cloumn
for tag in tag_list:
    summary_df[tag] = summary_df.apply(lambda row: tag in row['category'], axis=1)
summary_df = summary_df.reset_index(drop=True)
summary_df
        
