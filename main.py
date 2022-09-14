from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from git import Repo
import pandas as pd
import time

repo = Repo()
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
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

col = ['정원', '지원자 수', '경쟁률']
ind = ['울산대', '부산대', '경희대', '한양대', '고려대', '아주대']
con = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
df = pd.DataFrame(con, columns=col, index=ind)


iterations = 1
while iterations < 6:
    driver.execute_script('window.open("about:blank", "_blank");')
    iterations = iterations + 1

tabs = driver.window_handles

while True:
    # TAB_1: 울산대
    driver.switch_to.window(tabs[0])
    driver.get('http://ratio.uwayapply.com/Sl5KVzgmQzpKZiUmOiZKcGZUZg==')
    ulsan = Department('//*[@id="Tr_02B02034_002080000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['울산대'] = list_generator(ulsan)

    # TAB_2: 부산대
    driver.switch_to.window(tabs[1])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio12100301.html')
    pusan = Department('//*[@id="SelType4F"]/table/tbody/tr[29]/td', ['[3]', '[4]', '[5]'])
    df.loc['부산대'] = list_generator(pusan)

    # TAB_3: 경희대
    driver.switch_to.window(tabs[2])
    driver.get('http://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSnBmVGY=')
    kyunghee = Department('//*[@id="Tr_01312_000700000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['경희대'] = list_generator(kyunghee)

    # TAB_4: 한양대
    driver.switch_to.window(tabs[3])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11640191.html')
    hanyang = Department('//*[@id="SelType4B"]/table/tbody/tr[23]/td', ['[3]', '[4]', '[5]'])
    df.loc['한양대'] = list_generator(hanyang)

    # TAB_5: 고려대
    driver.switch_to.window(tabs[4])
    driver.get('http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg==')
    korea = Department('//*[@id="Tr_0151_000950000"]/td', ['[3]', '[4]', '[5]/font/b'])
    df.loc['고려대'] = list_generator(korea)

    # TAB_6: 아주대
    driver.switch_to.window(tabs[5])
    driver.get('http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11040291.html')
    ajou = Department('//*[@id="SelType402"]/table/tbody/tr[21]/td', ['[2]', '[3]', '[4]'])
    df.loc['아주대'] = list_generator(ajou)

    print(df)
    print('\n')
    html_text = '''<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300&display=swap" rel="stylesheet">
    <style>* {font-family: 'IBM Plex Sans KR', sans-serif;}</style>
    </head>
    <body>
    '''
    html_text = html_text + df.to_html() + '</body>'
    with open('index.html', 'w') as html_file:
        html_file.write(html_text)

    repo.index.add('index.html')
    repo.index.commit('automatic update')
    repo.remotes.origin.push()

    time.sleep(10)
