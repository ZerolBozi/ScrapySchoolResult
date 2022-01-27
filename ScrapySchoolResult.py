import requests
from bs4 import BeautifulSoup

# 不依賴學校官網的成績查詢，減少輸入驗證碼的步驟，快速查詢期末成績
# 可依需求自行做修改

def login(account,password):
    d = dict()
    s = requests.session()
    s.headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'
    }

    res = s.get(url='https://m.nfu.edu.tw/login/login?id=links&page=index&authority=nfu')
    d['cookie'] = requests.utils.dict_from_cookiejar(res.cookies)
    for i in BeautifulSoup(res.text,"html.parser").find_all("input",type="hidden"):
        d[i['name']] = i['value']
    
    payload = {
        'id' : d['id'],
        'page' : d['page'],
        'startOver' : d['startOver'],
        'anticsrf' : d['anticsrf'],
        'authority' : d['authority'],
        'loginUser' : account,
        'loginPassword' : password,
        'agreeTerm' : 1,
        '登入' : '登入'
    }
    
    s.post(url="https://m.nfu.edu.tw/login/login",data=payload,cookies=d['cookie'],allow_redirects=True)
    res = s.get(url="https://m.nfu.edu.tw/scscore/",cookies=d['cookie'])
    bs = BeautifulSoup(res.text,"html.parser")
    resultes = bs.find_all('li',class_='result')
    print(f'學號：{account} 的期末成績')
    print('-------------------------------')
    for i in resultes:
        td = i.find_all('td')
        for j in td:
            print(j.text)
        print('-------------------------------')

if __name__ == "__main__":
    login('學號','密碼')