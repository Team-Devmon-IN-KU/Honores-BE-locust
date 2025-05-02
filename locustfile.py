import requests
from locust import HttpUser, TaskSet, task, between
import random
from dotenv import load_dotenv
import os

# ✅ 전역 세션/토큰 저장소
SESSIONS = []
CSRF_TOKENS = []
# .env 파일을 현재 디렉토리에서 로드
load_dotenv()
# HOST = "http://localhost:8080"  # 서버 주소
HOST = os.getenv("SLAVE_HOST")

def init_tokens(user_id, user_pw):
    with requests.Session() as session:
        # CSRF 토큰 가져오기
        csrf_res = session.get(f"{HOST}/api/v1/csrf-token")
        csrf_json = csrf_res.json()
        csrf_token = csrf_json.get("token")
        csrf_header_name = csrf_json.get("headerName")

        # 로그인
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            csrf_header_name: csrf_token
        }
        login_res = session.post(
            f"{HOST}/api/v1/auth/login",
            data={"username": user_id, "password": user_pw},
            headers=headers
        )
        print(login_res)
        session_cookie = session.cookies.get("SESSION")

        return {
            "csrf_token": csrf_token,
            "csrf_header_name": csrf_header_name,
            "session": session_cookie
        }

def setup_users():
    for i in range(3):
        creds = f"performTUser{i+1}"
        result = init_tokens(creds, creds)
        SESSIONS.append(result["session"])
        CSRF_TOKENS.append({
            "token": result["csrf_token"],
            "header": result["csrf_header_name"]
        })

# ✅ 테스트 실행 전 세션 준비
setup_users()

"""1. CSRF 토큰 발급 (GET) /api/v1/csrf-token"""
class GetCSRF(TaskSet):
    name = "1. CSRF 토큰 발급 (GET) /api/v1/csrf-token"
    @task
    def get_csrf_token(self):
        self.client.get("/api/v1/csrf-token", name=self.name)
"""2. 주차장 리스트 불러오기 (GET) /api/v1/parkingzone/list"""
class GetParkingZoneList(TaskSet):
    name = "2. 주차장 리스트 불러오기 (GET) /api/v1/parkingzone/list"
    @task
    def get_parking_list(self):
        latitude = random.uniform(33.0, 38.5)
        longitude = random.uniform(126.0, 130.0)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "page": 0
        }

        self.client.get("/api/v1/parkingzone/list", params=params, name=self.name)
"""3. 주차장 사용 이력 리스트 불러오기 (GET) /api/v1/parking/history"""
class GetParkingHistoryList(TaskSet):
    name = "3. 주차장 사용 이력 리스트 불러오기 (GET) /api/v1/parking/history"
    @task
    def get_parking_list(self):
        # startTime과 endTime에 None을 적절히 설정
        params = {
            "page": 0,
            "number": 10,
            "startTime": None,  # Python에서는 None 사용
            "endTime": None     # Python에서는 None 사용
        }

        # API 호출
        self.client.get("/api/v1/parkingzone/list", params=params, name=self.name)
"""4. 주차장 북마크 설정 및 해제 반복"""
class ParkingBookMarkPostAndDelete(TaskSet):
    targetParkingZoneId = random.randint(14, 30)
    @task
    def post_then_delete_bookmark(self):
        body = {
            "parkingZoneId": self.targetParkingZoneId
        }

        # 1. POST 요청
        post_response = self.client.post("/api/v1/parking/parkingzone/bookmark", json=body, name="post_bookmark_post")
        # print("📥 POST 응답:", post_response.text)

        # 2. DELETE 요청 (POST 성공 여부와 무관하게 진행)
        delete_response = self.client.delete("/api/v1/parking/parkingzone/bookmark", json=body, name="delete_bookmark")
        # print("📤 DELETE 응답:", delete_response.text)

"""5. 회원 알람 불러오기 (GET) /api/v1/alarmAll"""
class GetAlarmsList(TaskSet):
    name = "5. 회원 알람 불러오기 (GET) /api/v1/alarmAll"
    @task
    def get_alarms(self):
        randCategory = ["INOUT", "RESERVE", "PAYMENT"]
        parm = {
            "page": random.randint(0, 2),
            "category" : random.choice(randCategory),
        }

        self.client.get("/api/v1/alarmAll", params=parm, name=self.name)

"""6. 읽지않은알림확인 (GET) /api/v1/alarmUnread"""
class GetAlarmUnread(TaskSet):
    name = "6. 읽지않은알림확인 (GET) /api/v1/alarmUnread"
    @task
    def get_alarm_unread(self):
        self.client.get("/api/v1/alarmUnread", name=self.name)

"""7. 주차장 이용상태 불러오기 (GET) /api/v1/parking/me"""
class GetCurrentParkingInfo(TaskSet):
    name = "7. 주차장 이용상태 불러오기 (GET) /api/v1/parking/me"
    @task
    def get_current_parking_info(self):
        self.client.get("/api/v1/parking/me", name=self.name)

"""8. 정산시작 (GET) /api/v1/pakring/paymentInfo"""
class GetCurrentParkingBeforePayment(TaskSet):
    name = "8. 정산시작 (GET) /api/v1/pakring/paymentInfo"
    @task
    def get_current_parking_before_payment(self):
        self.client.get(f"/api/v1/pakring/paymentInfo", name = self.name)

"""9. 로그인한 사용자 이름 가져오기 (GET) /api/v1/mypage/username"""
class GetMyPageUsername(TaskSet):
    name = "9. 로그인한 사용자 이름 가져오기 (GET) /api/v1/mypage/username"
    @task
    def get_mypage_username(self):
        self.client.get("/api/v1/mypage/username", name=self.name)

"""10. 로그인한 사용자 정보 수정 (PUT) /api/v1/mypage/info"""
class PutMyPageInfo(TaskSet):
    name = "10. 로그인한 사용자 정보 수정 (PUT) /api/v1/mypage/info"
    @task
    def get_mypage_info(self):
        body = {
            "email" : "devmon@devmon",
            "phoneNumber" : "01011111111"
        }
        self.client.put(f"/api/v1/mypage/info", name=self.name, json=body)

"""11. 로그인한 사용자 비밀번호 변경 (PUT) /api/v1/mypage/info/password"""
class PutMemberPassword(TaskSet):
    name = "11. 로그인한 사용자 비밀번호 변경 (PUT) /api/v1/mypage/info/password"
    @task
    def put_member_password(self):
        body = {"password" : f"performTUser{self.user.user_id}"}
        self.client.put(f"/api/v1/mypage/info/password", name=self.name, json=body)
class UserBehavior(TaskSet):
    tasks = []
    tasks.append(GetCSRF) #1. CSRF 토큰 발급 (GET) /api/v1/csrf-token
    tasks.append(GetParkingZoneList) #2. 주차장 리스트 불러오기 (GET) /api/v1/parkingzone/list
    # 3. 주차장 사용 이력 리스트 불러오기 (GET) /api/v1/parking/history
    # tasks.append(GetParkingHistoryList) --> 에러 발견🔥🔥🔥
    tasks.append(ParkingBookMarkPostAndDelete) #4. 주차장 북마크 설정 및 해제 반복
    tasks.append(GetAlarmsList) # 5. 회원 알람 불러오기 (GET) /api/v1/alarmAll
    tasks.append(GetAlarmUnread) # 6. 읽지않은알림확인 (GET) /api/v1/alarmUnread
    tasks.append(GetCurrentParkingInfo) # 7. 주차장 이용상태 불러오기 (GET) /api/v1/parking/me
    tasks.append(GetCurrentParkingBeforePayment) # 8. 정산시작 (GET) /api/v1/pakring/paymentInfo
    tasks.append(GetMyPageUsername)  # 9. 로그인한 사용자 이름 가져오기 (GET) /api/v1/mypage/username
    tasks.append(PutMyPageInfo) # 10. 로그인한 사용자 정보 수정 (PUT) /api/v1/mypage/info
    # tasks.append(PutMemberPassword) # 11. 로그인한 사용자 비밀번호 변경 (PUT) /api/v1/mypage/info/password

class WebsiteUser(HttpUser):
    user_id = None
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    # host = "http://localhost:8080"
    load_dotenv()
    # 환경 변수 SLAVE_HOST를 가져옴
    host = os.getenv("SLAVE_HOST")
    print(host)

    def on_start(self):
        # ✅ 세션만 미리 발급받은 리스트에서 랜덤 선택
        idx = random.randint(0, 2)
        session = SESSIONS[idx]
        self.user_id = idx + 1  # ✅ 여기서 유저 ID 저장
        # ✅ 세션 설정
        self.client.cookies.set("SESSION", session)

        # ✅ CSRF 새로 발급
        csrf_res = self.client.get("/api/v1/csrf-token")
        csrf_json = csrf_res.json()
        csrf_token = csrf_json.get("token")
        csrf_header_name = csrf_json.get("headerName")

        # ✅ 헤더에 CSRF 설정
        self.client.headers.update({csrf_header_name: csrf_token})
