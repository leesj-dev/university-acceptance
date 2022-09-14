from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
from git import Repo
from dotenv import load_dotenv
import pandas as pd
import smtplib
import time
import os

load_dotenv()
id = os.getenv('id')
pw = os.getenv('pw')

chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

class Department:
    def __init__(self, path, plist):
        self.path = path
        self.plist = plist
        self.accepted_path = path + plist[0]
        self.sent_path = path + plist[1]
        self.rate_path = path + plist[2]

    def accepted(self):
        return driver.find_element(By. XPATH, self.accepted_path).text

    def sent(self):
        return driver.find_element(By. XPATH, self.sent_path).text

    def rate(self):
        return driver.find_element(By. XPATH, self.rate_path).text

def list_generator(item):
    item_list = [item.accepted(), item.sent(), item.rate()]
    return item_list

iterations = 1
while iterations < 6:
    driver.execute_script('window.open("about:blank", "_blank");')
    iterations = iterations + 1

tabs = driver.window_handles

def get_info():
    col = ['모집 인원', '지원자 수', '경쟁률']
    ind = ['울산대 지역인재', '부산대 지역인재', '경희대 네오르네상스', '한양대 일반', '고려대 학업우수', '아주대 ACE']
    con = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    df = pd.DataFrame(con, columns=col, index=ind)

    # TAB_1: 울산대 지역인재
    driver.switch_to.window(tabs[0])
    driver.get('http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==')
    ulsan = Department('//*[@id="Tr_02B02034_002080000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['울산대 지역인재'] = list_generator(ulsan)

    # TAB_2: 부산대 지역인재
    driver.switch_to.window(tabs[1])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html')
    pusan = Department('//*[@id="SelType4F"]/table/tbody/tr[29]/td', ['[3]', '[4]', '[5]'])
    df.loc['부산대 지역인재'] = list_generator(pusan)

    # TAB_3: 경희대 네오르네상스
    driver.switch_to.window(tabs[2])
    driver.get('http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=')
    kyunghee = Department('//*[@id="Tr_01312_000700000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['경희대 네오르네상스'] = list_generator(kyunghee)

    # TAB_4: 한양대 일반
    driver.switch_to.window(tabs[3])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html')
    hanyang = Department('//*[@id="SelType4B"]/table/tbody/tr[23]/td', ['[3]', '[4]', '[5]'])
    df.loc['한양대 일반'] = list_generator(hanyang)

    # TAB_5: 고려대 학업우수
    driver.switch_to.window(tabs[4])
    driver.get('http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==')
    korea = Department('//*[@id="Tr_0151_000950000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['고려대 학업우수'] = list_generator(korea)

    # TAB_6: 아주대 ACE
    driver.switch_to.window(tabs[5])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html')
    ajou = Department('//*[@id="SelType402"]/table/tbody/tr[21]/td', ['[2]', '[3]', '[4]'])
    df.loc['아주대 ACE'] = list_generator(ajou)

    return df


def push_html(df):
    html_text = '''<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300&display=swap" rel="stylesheet">
    <style>
    * {font-family: 'IBM Plex Sans KR', sans-serif;}
    td {text-align: center;}
    table {margin-left:auto; margin-right: auto;}
    table, td, th {border-collapse: collapse; border: 1px solid black; text-align: center;}
    td, th {padding: 5px 15px;}
    </style>
    </head>
    <body>
    <h1 style="font-size:30" align="center">실시간 경쟁률</h1>
    '''

    html_body = df.to_html().replace(' style="text-align: center;"', '')
    html_body = html_body.replace('table border="1"', 'table')
    html_final = html_text + html_body + '</body>'

    with open('index.html', 'w') as html_file:
        html_file.write(html_final)

    repo = Repo()
    repo.index.add('index.html')
    repo.index.commit('automatic update')
    repo.remotes.origin.push()

    print('Push Completed.')


df_before = get_info()
push_html(df_before)

while True:
    time.sleep(180)
    df_after = get_info()

    if df_before != df_after:
        push_html(df_after)

        msg = MIMEText('원서접수 경쟁률 변경이 감지되었습니다.')
        msg["Subject"] = '경쟁률 변경 감지'
        msg["From"] = id
        msg["To"] = id

        with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
            smtp.login(id, pw)
            smtp.sendmail(id, id, msg.as_string())

    df_before = df_after