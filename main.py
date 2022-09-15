from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
from git import Repo
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import smtplib
import time
import os

# 초기 설정
load_dotenv()
id = os.getenv('id')
pw = os.getenv('pw')

chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


class Department:
    def __init__(self, path, plist, timestamp):
        self.path = path
        self.plist = plist
        self.accepted_path = path + plist[0]
        self.sent_path = path + plist[1]
        self.rate_path = path + plist[2]
        self.timestamp = timestamp

    # 모집 인원
    def accepted(self):
        return driver.find_element(By. XPATH, self.accepted_path).text

    # 지원자 수
    def sent(self):
        return driver.find_element(By. XPATH, self.sent_path).text

    # 경쟁률
    def rate(self):
        return driver.find_element(By. XPATH, self.rate_path).text

    # 기준 시각
    def time(self):
        time_string = driver.find_element(By. XPATH, self.timestamp).text

        # 유웨이
        if '분' in time_string:
            time_string = time_string.split('분', 1)[0] + '분'
            time_string = time_string.replace('년 ', '/')
            time_string = time_string.replace('월 ', '/')
            time_string = time_string.replace('일', '')
            time_string = time_string.replace('시 ', ':')
            time_string = time_string.replace('분', '')

        # 진학사
        elif '오전' in time_string or '오후' in time_string:
            time_string = time_string.split('현', 1)[0]
            time_string = time_string.replace('-', '/')

            if '오전' in time_string:
                loc1 = time_string.find('오전')
                loc2 = time_string.find(':')
                if int(time_string[loc1 + 3 : loc2]) == 12:
                    new_time = '00'

                elif int(time_string[loc1 + 3 : loc2]) < 10:
                    new_time = '0' + time_string[loc1 + 3 : loc2]

                else:
                    new_time = time_string[loc1 + 3 : loc2]

            elif '오후' in time_string:
                loc1 = time_string.find('오후')
                loc2 = time_string.find(':')
                if int(time_string[loc1 + 3 : loc2]) == 12:
                    new_time = '12'

                else:
                    new_time = str(int(time_string[loc1 + 3 : loc2]) + 12)

            time_string = time_string[0 : loc1] + new_time + ':' + time_string[loc2 + 1 : len(time_string)]

        return time_string


def list_generator(department):
    item_list = [department.accepted(), department.sent(), department.rate(), department.time()]
    return item_list

iterations = 1
while iterations < 6:
    driver.execute_script('window.open("about:blank", "_blank");')
    iterations = iterations + 1

tabs = driver.window_handles

# 크롤링
def get_info():
    col = ['모집 인원', '지원자 수', '경쟁률', '기준 시각']
    ind = ['울산대 지역인재', '부산대 지역인재', '경희대 네오르네상스', '한양대 일반', '고려대 학업우수', '아주대 ACE']
    con = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    df = pd.DataFrame(con, columns=col, index=ind)

    # TAB_0: 울산대 지역인재
    driver.switch_to.window(tabs[0])
    driver.get('http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==')
    ulsan = Department('//*[@id="Tr_02B02034_002080000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['울산대 지역인재'] = list_generator(ulsan)

    # TAB_1: 부산대 지역인재
    driver.switch_to.window(tabs[1])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html')
    pusan = Department('//*[@id="SelType4F"]/table/tbody/tr[29]/td', ['[3]', '[4]', '[5]'], '//*[@id="RatioTime"]')
    df.loc['부산대 지역인재'] = list_generator(pusan)

    # TAB_2: 경희대 네오르네상스
    driver.switch_to.window(tabs[2])
    driver.get('http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=')
    kyunghee = Department('//*[@id="Tr_01312_000700000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['경희대 네오르네상스'] = list_generator(kyunghee)

    # TAB_3: 한양대 일반
    driver.switch_to.window(tabs[3])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html')
    hanyang = Department('//*[@id="SelType4B"]/table/tbody/tr[23]/td', ['[3]', '[4]', '[5]'], '//*[@id="RatioTime"]')
    df.loc['한양대 일반'] = list_generator(hanyang)

    # TAB_4: 고려대 학업우수
    driver.switch_to.window(tabs[4])
    driver.get('http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==')
    korea = Department('//*[@id="Tr_0151_000950000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['고려대 학업우수'] = list_generator(korea)

    # TAB_5: 아주대 ACE
    driver.switch_to.window(tabs[5])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html')
    ajou = Department('//*[@id="SelType402"]/table/tbody/tr[21]/td', ['[2]', '[3]', '[4]'], '//*[@id="RatioTime"]')
    df.loc['아주대 ACE'] = list_generator(ajou)

    return df


# push할 HTML
def push_html(df):
    html_text = '''<head>
    <meta name="viewport" content="width=device-width" charset="UTF-8" http-equiv="refresh" content="60" />
    <title>실시간 경쟁률</title>
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

    html_body = df.to_html().replace(' style="text-align: right;"', '')
    html_body = html_body.replace('table border="1"', 'table')
    html_final = html_text + html_body + '</body>'

    with open('index.html', 'w') as html_file:
        html_file.write(html_final)

    repo = Repo()
    repo.index.add('index.html')
    repo.index.commit('automatic update')
    repo.remotes.origin.push()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('push 완료 [' + current_time + ']')


# 최초 실행
df_before = get_info()
push_html(df_before)

while True:
    time.sleep(60)
    df_after = get_info()

    # 기준 시각이 바뀔 때: push는 무조건 해야 함
    if not df_before.equals(df_after):
        push_html(df_after)

        # 지원자 수가 바뀔 때만 메일을 보내야 함
        df_before_rmvtime = df_before.drop(columns=['기준 시각'])
        df_after_rmvtime = df_after.drop(columns=['기준 시각'])

        if not df_before_rmvtime.equals(df_after_rmvtime):
            df_diff = df_before_rmvtime.compare(df_after_rmvtime, align_axis=1, keep_shape=False, keep_equal=False)
            changes = []
            message = '원서 접수 경쟁률이 변경되었습니다.\n'

            for index, row in df_diff.iterrows():
                changes.append([index, row[('지원자 수', 'self')], row[('지원자 수', 'other')], row[('경쟁률', 'self')], row[('경쟁률', 'other')]])

            for item in changes:
                message += item[0] + " - 지원자 수: <b>" + item[1] + "</b>명 → <b>" + item[2] + "</b>명 / 경쟁률: <b>" + item[3] + "</b> → <b>" + item[4] + "</b>\n"

            # 메일 전송
            msg = MIMEText(message, 'html')
            msg["Subject"] = '경쟁률 변경 감지'
            msg["From"] = id
            msg["To"] = id

            with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
                smtp.login(id, pw)
                smtp.sendmail(id, id, msg.as_string())

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('메일 전송 완료 [' + current_time + ']')

    df_before = df_after
