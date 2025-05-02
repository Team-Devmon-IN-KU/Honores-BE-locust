# 🛠 Locust 수행 방법 A to Z
 
## 1. Git 저장소 클론하기
먼저 프로젝트를 로컬로 클론합니다. 터미널에서 아래 명령어를 입력해 주세요.

```bash
git pull <저장소 URL>
```
## 2. 파이썬 설치 (로컬에 파이썬이 없다면)

로컬에 파이썬이 설치되지 않았다면, Python 공식 웹사이트에서 최신 버전을 다운로드하고 설치하세요.

## 3. 가상환경 만들기

프로젝트 디렉토리로 이동한 후, 아래 명령어로 가상환경을 생성합니다.
해당 부분은 인터넷에서 "IDE별 가상환경 세팅 하기" 예) "파이참 가상환경 세팅하기" 검색하시면 쉽게 찾을 수 있습니다. 

가상환경을 만들면 .venv라는 폴더가 생성되고, 터미널에 (venv)가 표시됩니다.

예시:
![](https://res.cloudinary.com/dhabktrg9/image/upload/v1746183304/rjmstwq5juce9xsikvmh.png)

## 4. 의존성 패키지 설치

프로젝트에서 사용되는 의존성 패키지들을 requirements.txt 파일을 통해 설치합니다.

```bash
pip install -r requirements.txt
```

## 5. .env파일에 host주소 명시하기
```env
SLAVE_HOST = https://test/test/
```

## 6. 프로젝트 실행하기

이제 locustfile.py를 실행하여 로컬에서 프로젝트를 실행할 수 있습니다. 아래 명령어로 실행하세요.


```bash
locust -f locustfile.py
```

## 하나도 빠짐없이 해야합니다!!!

# 끝!!🥲