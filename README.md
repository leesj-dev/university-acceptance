# university-acceptance
* 진학사어플라이 및 유웨이어플라이로부터 정보를 크롤링하여 대입 원서 접수의 실시간 경쟁률을 웹사이트에 호스팅하며, 변경 사항이 감지되었을 때 메일로 변경내역을 전송합니다. 크롤링 주기는 10분이며, 매시 정각부터 10분 단위의 시간에 진행합니다.
* 현재는 Python을 이용한 크롤링만 지원하고 있으며, 이 경우 컴퓨터에서 계속 코드를 실행시켜야만 사용할 수 있습니다. Javascript를 이용하여, 컴퓨터에서 코드를 직접 실행하지 않아도 웹페이지에서 client-side rendering을 하는 방안은 추후 개발할 계획입니다.


## How to Use
#### 1. env 설정
* git을 clone한 다음, `pip install -r requirements.txt`를 터미널에 입력하여 필요한 라이브러리들을 설치합니다.
* `backend` 폴더에 `.env` 파일을 생성하고 아래 내용을 넣습니다. `id`에는 NAVER 아이디 (@naver.com 포함), `pw`에는 비밀번호를 넣습니다. (`215`번 줄을 수정하면 다른 이메일 도메인도 사용할 수 있습니다.)
```
id = YOUR_EMAIL_ID@naver.com
pw = YOUR_EMAIL_PASSWORD
```

#### 2. 학과 설정
* `backend` 폴더의 `main.py` (lxml으로 크롤링) 또는 `selenium(deprecated).py` (Selenium으로 크롤링)을 엽니다. lxml 방식이 약 3배 더 빠르므로, 가급적이면 `main.py`를 이용해주세요.
* `selenium(deprecated).py`를 사용하려면, `requirements.txt`에 아래를 추가해야 합니다.
```
selenium==4.4.3
webdriver_manager==3.8.3
```
* `main.py` 기준으로, `96`번 줄에는 경쟁률을 모니터링할 학과를 넣고,  `100` ~ `128` 번 줄에는 링크 및 XPath을 넣습니다. 기본적으로 진학사는 진학사끼리, 유웨이는 유웨이끼리 형식이 거의 같으나 일부 예외가 있으므로 **반드시 확인 후 넣어주세요**.

‘고려대 학업우수 의예과’를 예로 들어보겠습니다.
* 경쟁률을 표시하는 링크를 넣습니다.
```
PAGE_5 = 'http://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKcGZUZg=='
```

* 해당 학과의 경쟁률이 표시되는 부분을 DevTools에서 XPath로 가져오고, 그 뒤에 `/td`를 넣습니다. `//*[@id="Tr_0151_000950000"]/td`

* 모집 인원, 지원자 수, 경쟁률이 몇 번째 `td`에 있는지를 list 형태로 넣습니다. 이때  `[5]/font/b`와 같이 경로가 뒤에 추가로 더 들어갈 수도 있으니 상황에 맞추어 조정해주면 됩니다.

* 마지막으로, 페이지 상단에 뜨는 기준 시각을 가져옵니다. 일반적으로 진학사는 `//*[@id="RatioTime"]`, 유웨이는 `//*[@id="ID_DateStr"]/label`입니다.

* 이를 종합하면 다음과 같습니다. `(학교 또는 학과의 영문명) = Department(XPath, [모집 인원 경로, 지원자 수 경로, 경쟁률 경로], 기준 시각 경로)`
```
korea = Department('//*[@id="Tr_0151_000950000"]/td', ['[3]', '[4]', '[5]/font/b'], '//*[@id="ID_DateStr"]/label')
```

* 마지막으로 `107`번 줄에 입력했던 학과를 그대로 넣고, 학교 또는 학과의 영문명도 `list_generator` 오른쪽에 넣어줍니다.
```
df.loc['고려대 학업우수'] = korea.list_generator()
```

#### 3. 추가 기능 설정
* 지정한 엑셀 파일에 경쟁률 정보를 덮어쓸 수 있습니다. `paste_excel(df)` 함수에서 경로를 수정할 수 있습니다.
* 마지막 줄 `process(True, True)`에서 첫 번째 `True`는 메일 전송 기능을 활성화했다는 의미이고, 두 번째 `True`는 엑셀 수정 기능을 활성화했다는 의미입니다. `False`로 바꾸어 비활성화할 수 있습니다.

#### 4. push하기
* 우선 수동으로 Github에 한 번 push를 해줍니다.
* 이후  `Settings > Pages`에 들어가서 Github Pages를
활성화해줍니다.
* 마지막으로  `main.py`를 실행하면 자동으로 Github에 `index.html`이 주기적으로 push가 되며, 이후 Github Pages에서 호스팅이 완료됩니다. push한 html이 웹페이지에 반영되기까지는 약 1분 정도 소요됩니다.
* 웹사이트 예시 이미지
<img width="838" alt="예시" src="https://user-images.githubusercontent.com/104193215/190553223-42dd7ce5-1d97-4dbf-a426-3d3e41c43710.png">

