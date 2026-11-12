"""프로젝트 전체 설정.

Django는 서버가 켜질 때 이 파일을 한 번 읽는다.
여기 있는 대문자 변수들이 설정이다. 소문자로 쓰면 Django가 무시한다.
게시판 화면 로직은 posts 앱에 있고, 이 파일은 "어떤 앱을 켜고, 화면을 어떻게 찾을지"만 정한다.
"""

import os
from pathlib import Path

# 이 파일(config/settings.py)에서 두 단계 위가 프로젝트 루트(board 폴더)다.
# parent 한 번: config 폴더, parent 두 번: board 폴더.
# 나중에 파일 경로가 필요하면 BASE_DIR / '파일명'처럼 이어 붙인다.
BASE_DIR = Path(__file__).resolve().parent.parent

# 쿠키 서명 등에 쓰는 비밀 문자열이다.
# 이 값이 밖으로 새면 다른 사람이 서명을 위조할 수 있으므로, 실제 서비스에서는 코드에 적지 않는다.
# 지금 값은 연습용으로 자동 생성된 것이다.
SECRET_KEY = 'django-insecure-0qz0xvm-c40e(qyl+^)$&&g&r*v*2*(jldic7kdywituk5067d'

# True면 에러가 났을 때 노란 디버그 화면을 보여 준다. 개발 중에만 켠다.
# 실제 서비스에서 True로 두면 설정과 코드가 방문자에게 노출된다.
DEBUG = True

# DEBUG가 False일 때, 여기 적힌 도메인으로 들어온 요청만 받는다.
# 비어 있으면 localhost 개발 서버만 허용하는 상태다.
ALLOWED_HOSTS = []


# 켜 둘 앱 목록. Django는 이 목록에 있는 앱의 models.py, templates 폴더 등을 찾는다.
# django.contrib.staticfiles: CSS, 이미지 같은 정적 파일을 서빙하는 기본 앱.
# posts: 이 프로젝트의 게시판 앱.
# 회원(auth), 관리자(admin) 화면은 아직 쓰지 않는다.
# 글 테이블만 있으면 되므로 게시판 앱만 켠다.
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'posts',
]

# 미들웨어는 뷰 함수 앞뒤에서 모든 요청에 공통으로 실행되는 처리 단계다.
# 위에서 아래 순서로 요청이 들어가고, 응답은 역순으로 빠져나온다.
MIDDLEWARE = [
    # HTTPS 관련 보안 헤더를 붙인다.
    'django.middleware.security.SecurityMiddleware',
    # URL 끝에 슬래시가 빠졌을 때 붙여서 다시 보내는 등, 주소 정규화를 한다.
    'django.middleware.common.CommonMiddleware',
    # 글쓰기 같은 POST 요청에 CSRF 토큰이 있는지 검사한다. form.html의 csrf_token과 짝이다.
    'django.middleware.csrf.CsrfViewMiddleware',
    # 이 사이트가 다른 사이트의 iframe 안에 끼워지는 것을 막아 클릭 가로채기를 줄인다.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 최상위 주소록 파일. 'config.urls'는 config/urls.py다.
ROOT_URLCONF = 'config.urls'

# HTML 템플릿을 어떻게 찾을지 정한다.
TEMPLATES = [
    {
        # Django 기본 템플릿 엔진을 쓴다. {{ 변수 }}, {% 태그 %} 문법이 이 엔진 것이다.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 프로젝트 공용 템플릿 폴더. 지금은 비어 있고, 각 앱의 templates 폴더를 쓴다.
        'DIRS': [],
        # True면 INSTALLED_APPS 안의 templates 폴더를 자동으로 찾는다.
        # 그래서 posts/templates/posts/list.html을 "posts/list.html"이라는 이름으로 연다.
        'APP_DIRS': True,
        'OPTIONS': {
            # 템플릿에 항상 넣어 주는 값. request가 있어야 {% url %} 등이 안정적으로 동작한다.
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

# 배포용 WSGI 입구. 연습 중 runserver는 이 값을 참고만 한다.
WSGI_APPLICATION = 'config.wsgi.application'


# Supabase PostgreSQL에 접속한다.
# HOST, PORT, NAME, USER는 Connect 창의 값이다.
# 비밀번호는 이 파일에 적지 않는다. 서버를 켜기 전에 터미널에서
# $env:SUPABASE_DB_PASSWORD = "비밀번호" 로 넣어 두면 os.environ이 그 값을 읽는다.
# sslmode는 Supabase가 암호 연결만 받기 때문에 필요하다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('SUPABASE_DB_PASSWORD', ''),
        'HOST': 'db.kyqxluwbewenznojuidf.supabase.co',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}


# 비밀번호 규칙. 지금은 회원가입이 없지만, startproject가 만들어 준 기본값이다.
# 나중에 회원 기능을 넣을 때 이 목록의 검사를 사용한다.
AUTH_PASSWORD_VALIDATORS = [
    {
        # 아이디와 너무 비슷한 비밀번호를 막는다.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 너무 짧은 비밀번호를 막는다. 기본은 8자 이상이다.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # "password"처럼 흔히 쓰이는 비밀번호를 막는다.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # 숫자로만 된 비밀번호를 막는다.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 언어와 시간. 오류 메시지와 날짜 형식의 기본 언어를 한국어로 둔다.
LANGUAGE_CODE = 'ko-kr'

# 시간대를 서울로 둔다. USE_TZ가 True면 Django는 내부적으로 UTC를 쓰고 표시할 때 이 시간대로 바꾼다.
TIME_ZONE = 'Asia/Seoul'

# 번역 기능을 켠다.
USE_I18N = True

# 시간대 인식 날짜(timezone-aware datetime)를 사용한다.
USE_TZ = True


# 정적 파일(CSS, 이미지, JS)의 주소 접두사.
# 예: static/style.css 파일은 브라우저에서 /static/style.css 로 요청한다.
# 이 프로젝트는 CSS를 base.html 안에 직접 적어서, 아직 별도 정적 파일은 없다.
STATIC_URL = 'static/'


# 메일 보내는 방법. console은 실제로 보내지 않고 터미널에 내용만 출력한다.
# 이 게시판은 아직 메일을 보내지 않아서 쓰이지 않는다.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
