"""배포할 때 비동기 서버가 이 프로젝트를 부르는 입구 (ASGI).

이 게시판은 아직 채팅이나 실시간 기능이 없어서 연습 중에는 쓰이지 않는다.
ASGI는 요청을 동시에 여러 개 처리할 수 있는 규격이고,
파일 안의 application 변수를 서버가 찾는다.
"""

import os

from django.core.asgi import get_asgi_application

# manage.py와 같이, 설정 파일 위치를 알려 준다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 비동기 웹 서버가 호출하는 함수. 이름은 application이어야 한다.
application = get_asgi_application()
