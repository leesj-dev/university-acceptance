from lxml import html
from email.mime.text import MIMEText
from git import Repo
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import requests
import smtplib
import time
import os
import xlwings

# 초기 설정
load_dotenv()
id = os.getenv('id')
pw = os.getenv('pw')

class Department:
    def __init__(self, page, path, plist, timestamp):
        if '/tbody' in path:  # lxml은 tbody를 간주하지 않으므로, 전처리로 없애야 함
            path = path.replace('/tbody', '')

        self.page = page
        self.accepted_path = path + plist[0]
        self.sent_path = path + plist[1]
        self.rate_path = path + plist[2]
        self.timestamp = timestamp
        self.tree = html.fromstring(requests.get(self.page).content)

    # 모집 인원
    def accepted(self):
        return self.tree.xpath(self.accepted_path)[0].text

    # 지원자 수
    def sent(self):
        return self.tree.xpath(self.sent_path)[0].text

    # 경쟁률
    def rate(self):
        return self.tree.xpath(self.rate_path)[0].text

    # 기준 시각
    def time(self):
        time_string = self.tree.xpath(self.timestamp)[0].text

        # 유웨이
        if '분' in time_string:
            time_string = time_string.split('분', 1)[0] + '분'
            time_string = time_string.replace('2022년 ', '')
            time_string = time_string.replace('월 ', '/')
            time_string = time_string.replace('일', '')
            time_string = time_string.replace('시 ', ':')
            time_string = time_string.replace('분', '')

        # 진학사
        elif '오전' in time_string or '오후' in time_string:
            time_string = time_string.split('현', 1)[0]
            time_string = time_string.replace('2022-', '')
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

            time_string = time_string[0 : loc1] + new_time + ':' + time_string[loc2 + 1 : len(time_string) - 1]

        # else: 접수완료 (최종현황)
        return time_string

    def list_generator(self):
        item_list = [self.accepted(), self.sent(), self.rate(), self.time()]
        return item_list

# 크롤링
def get_info():
    col = ['모집 인원', '지원자 수', '경쟁률', '기준 시각']
    ind = ['울산대 지역인재', '부산대 지역인재', '경희대 네오르네상스', '한양대 일반', '고려대 학업우수', '아주대 ACE']
    con = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    df = pd.DataFrame(con, columns=col, index=ind)

    # PAGE_1: 울산대 지역인재 (유웨이)
    page1 = 'http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg=='
    ulsan = Department(page1, '//*[@id="Tr_02B02034_002080000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['울산대 지역인재'] = ulsan.list_generator()

    # PAGE_2: 부산대 지역인재 (진학사)
    page2 = 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html'
    pusan = Department(page2, '//*[@id="SelType4F"]/table/tbody/tr[29]/td', ['[3]', '[4]', '[5]'], '//*[@id="RatioTime"]')
    df.loc['부산대 지역인재'] = pusan.list_generator()

    # PAGE_3: 경희대 네오르네상스 (유웨이)
    page3 = 'http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY='
    kyunghee = Department(page3, '//*[@id="Tr_01312_000700000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['경희대 네오르네상스'] = kyunghee.list_generator()

    # PAGE_4: 한양대 일반 (진학사)
    page4 = 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html'
    hanyang = Department(page4, '//*[@id="SelType4B"]/table/tbody/tr[23]/td', ['[3]', '[4]', '[5]'], '//*[@id="RatioTime"]')
    df.loc['한양대 일반'] = hanyang.list_generator()

    # PAGE_5: 고려대 학업우수 (유웨이)
    page5 = 'http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg=='
    korea = Department(page5, '//*[@id="Tr_0151_000950000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
    df.loc['고려대 학업우수'] = korea.list_generator()

    # PAGE_6: 아주대 ACE (진학사)
    page6 = 'http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html'
    ajou = Department(page6, '//*[@id="SelType402"]/table/tbody/tr[21]/td', ['[2]', '[3]', '[4]'], '//*[@id="RatioTime"]')
    df.loc['아주대 ACE'] = ajou.list_generator()

    return df


# push할 HTML
def push_html(df):
    html_text = '''<head>
    <meta name="viewport" content="width=device-width" initial-scale="1" charset="UTF-8" />
    <title>실시간 경쟁률</title>
    <link rel="stylesheet" href="styles.css">
    </head>
    <body>
    <h1>실시간 경쟁률</h1>
    '''

    html_body = df.to_html().replace(' style="text-align: right;"', '')
    html_body = html_body.replace('table border="1"', 'table')
    html_final = html_text + html_body + '</body>'

    with open('index.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_final)

    repo = Repo()
    repo.index.add('index.html')
    repo.index.commit('automatic update')
    repo.remotes.origin.push()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('push 완료 [' + current_time + ']')


# 엑셀에 붙여넣음
def paste_excel(df):
    df_excel = df.drop(columns=['모집 인원'])
    ws = xlwings.Book(os.getcwd() + '/backend/수시 원서.xlsx').sheets('Sheet1')
    ws.range('J2:L7').options(pd.DataFrame, index=False, header=False).value = df_excel


def process(mail_tf, excel_tf):

    # 최초 실행
    df_before = get_info()
    push_html(df_before)

    if excel_tf is True:
        paste_excel(df_before)

    while True:
        # 최소 업데이트 주기는 10분 단위임
        min = int(datetime.now().strftime("%M")[-1])
        sec = int(datetime.now().strftime("%S"))
        total_sec = 600 - 60 * min - sec
        time.sleep(total_sec + 10)  # 여유를 주기 위해, 10초 정도 추가

        df_after = get_info()

        # 기준 시각이 바뀔 때: push는 무조건 해야 함
        if not df_before.equals(df_after):
            push_html(df_after)

            if excel_tf is True:
                paste_excel(df_after)

            if mail_tf is True:
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

process(True, True)