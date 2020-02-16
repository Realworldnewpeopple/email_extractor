import requests
import re
from bs4 import BeautifulSoup
import pandas as pd  

allLinks = [];mails=[]
with open('links.txt', 'r') as f:
    x = f.read().splitlines()
print(x)

for url in x:
    try:
        response = requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        links = [a.attrs.get('href') for a in soup.select('a[href]') ]
    except:
        continue
    for i in links:
        try:
            if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i):
                if(i.startswith("http") or i.startswith("https") or i.startswith("www")):
                    allLinks.append(i)
                else:
                    newurl=url[:-1]+i
                    allLinks.append(newurl)
        except:
            continue

def findMails(soup):
    for name in soup.find_all('a'):
        if(name is not None):
            emailText=name.text
            match=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',emailText))
            if('@' in emailText and match==True):
                emailText=emailText.replace(" ",'').replace('\r','')
                emailText=emailText.replace('\n','').replace('\t','')
                if(len(mails)==0)or(emailText not in mails):
                    print(emailText)
                mails.append(emailText)
                
for link in allLinks:
    try:
        if(link.startswith("http") or link.startswith("https") or link.startswith("www")):
            r=requests.get(link)
            data=r.text
            soup=BeautifulSoup(data,'html.parser')
            findMails(soup)
    except:
        continue


mails=set(mails)
if(len(mails)==0):
    print("NO MAILS FOUND")
else:
    df = pd.DataFrame(mails)
    df.to_csv('file1.csv',index=False)