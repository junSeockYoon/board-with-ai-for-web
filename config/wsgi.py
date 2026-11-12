"""배포할 때 웹 서버가 이 프로젝트를 부르는 입구 (WSGI).

지금처럼 `python manage.py runserver`로 연습할 때는 이 파일을 직접 쓰지 않는다.
Vercel은 이 파일의 application 변수를 찾아서 방문자 요청을 Django에 넘긴다.
WSGI는 한 번에 하나의 요청을 처리하는 전통적인 파이썬 웹 규격이다.
"""

import os

from django.core.wsgi import get_wsgi_application

# manage.py와 같이, 설정 파일 위치를 알려 준다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 웹 서버가 호출하는 함수. 이름은 application이어야 한다.
application = get_wsgi_application()
