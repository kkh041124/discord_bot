import requests
from bs4 import BeautifulSoup
import pandas as pd

resp=requests.get('https://www.seoultech.ac.kr/service/info/notice/')
html=resp.text
soup=BeautifulSoup(html,'html.parser')
news=soup.select('.body_tr a')

title=[]
url=[]

news

for n in news:
    title.append(n.text.strip())
    url.append(n['href'].strip())
df=pd.DataFrame()
df['제목']=title
df['URL']=url

print(df)