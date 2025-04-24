from locust import HttpUser, TaskSet, task, between
import random
class PartyBehavior(TaskSet):

    testUserID = "testUserID"
    testUserPW = "testUserPW"
    latitude = random.uniform(33.0, 38.5)  # 한국의 위도 범위
    longitude = random.uniform(126.0, 130.0)  # 한국의 경도 범위
    def on_start(self):
        """시작 시 로그인하여 세션 및 CSRF 토큰 확보"""
        # 1. CSRF 토큰 얻기
        csrf_get_response = self.client.get("/api/v1/csrf-token")
        if csrf_get_response.status_code == 200:
            csrf_response_json = csrf_get_response.json()
            csrf_token = csrf_response_json.get("token")
            csrf_header_name = csrf_response_json.get("headerName")

            # CSRF 토큰을 동적으로 헤더에 추가
            self.client.headers.update({csrf_header_name: csrf_token})
            # print("\n=== CSRF TOKEN RESPONSE ===")
            # print("Status Code:", csrf_get_response.status_code)
            # print("Headers:", csrf_get_response.headers)
            # print("Cookies:", csrf_get_response.cookies)
            # print("Response Text:", csrf_get_response.text)
            # print("===========================\n")

        """시작 시 로그인 요청을 보내고 응답 전체 출력"""

        login_response = self.client.post(
            "/api/v1/auth/login",
            data={
                "username": self.testUserID,
                "password": self.testUserPW
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print("\n=== LOGIN RESPONSE ===")
        print("Status Code:", login_response.status_code)
        print("Headers:", login_response.headers)
        print("Cookies:", login_response.cookies)
        print("Response Text:", login_response.text)
        print("======================\n")

        # 3. Set-Cookie에서 SESSION 추출 및 설정
        set_cookie_header = login_response.headers.get('Set-Cookie', '')
        for cookie_item in set_cookie_header.split(','):
            if 'SESSION=' in cookie_item:
                session_value = cookie_item.strip().split('SESSION=')[-1].split(';')[0]
                self.client.cookies.set('SESSION', session_value)
                print(f"✔ 세션 쿠키 설정 완료: SESSION={session_value}")
    @task(name="GET /api/v1/parkingzone/list")
    def get_parking_list(self):
        # 랜덤한 위도 및 경도 값 생성 (한국 내에서)


        # 쿼리 파라미터로 요청
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "page": 0
        }

        # API 호출
        response = self.client.get("/api/v1/parkingzone/list", params=params)

class WebsiteUser(HttpUser):
    tasks = [PartyBehavior]
    wait_time = between(1, 3)  # 요청 간 대기 시간
    host = "http://localhost:8080"  # 로컬 서버 URL
    # host = "https://gyural.shop:8080"  # 로컬 서버 URL
    # host = "https://3.34.146.211.nip.io"