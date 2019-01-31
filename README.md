파이썬(3.6) 크롤러

비디오 Rails 데이터 적재

1. 설정 정보를 config.json 으로 작성 후 config/ 에 복사
{
  "language": "en",
  "parser_threads":  1,
  "domain": "http://www.google.com",
  "proxy": "",
  "redis": {
    "address": "127.0.0.1",
    "port": `123,
    "db": 0,
    "password": "hehehehe"
  },
  "database": {
    "address": "127.0.0.1",
    "port": 3306,
    "db": "mynameisbingo",
    "user": "root",
    "password": "mypassword"
  },
  "download_cover": false
}

2. 패키지 설치

pip install -r requirements.txt

3. 테스트

$ python test/test_main.py

4. 실행

$ python beefarm.py





