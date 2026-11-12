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
# Vercel에서는 대시보드 환경 변수 DJANGO_SECRET_KEY로 넣는다. 코드에는 적지 않는다.
# 변수가 없으면 아래 연습용 값을 쓴다. 이 값은 이미 공개된 상태라 배포에는 쓰면 안 된다.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-0qz0xvm-c40e(qyl+^)$&&g&r*v*2*(jldic7kdywituk5067d',
)

# True면 에러가 났을 때 노란 디버그 화면을 보여 준다. 개발 중에만 켠다.
# Vercel은 배포할 때 VERCEL=1 이라는 값을 넣어 준다. 그때는 디버그 화면을 끈다.
DEBUG = os.environ.get('VERCEL') != '1'

# 이 목록에 있는 주소로 들어온 요청만 받는다.
# .vercel.app 은 그 주소로 끝나는 Vercel 배포 주소를 모두 허용한다.
# 로컬 연습은 localhost 와 127.0.0.1 이다.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS',
        '.vercel.app,localhost,127.0.0.1',
    ).split(',')
    if host.strip()
]

# 글쓰기 폼은 "이 사이트가 보낸 요청인지"를 검사한다.
# https://*.vercel.app 은 Vercel이 만들어 준 https 주소를 허용한다는 뜻이다.
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        'https://*.vercel.app',
    ).split(',')
    if origin.strip()
]

# Vercel은 방문자와 Django 사이에 서 있다. 방문자는 https로 접속하지만,
# Django에게는 앞단이 http처럼 보일 수 있다. 이 헤더를 믿어야 폼 검사가 통과한다.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


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
# 비밀번호는 이 파일에 적지 않는다. 로컬에서는 서버를 켜기 전에
# $env:SUPABASE_DB_PASSWORD = "비밀번호" 로 넣는다.
# 아래 HOST, PORT, USER 기본값은 집 컴퓨터에서 직접 붙는 주소(5432)다.
# Vercel은 이 직접 주소가 막히는 경우가 많아서, 대시보드에는 Supabase Connect 창의
# Transaction pooler 값을 환경 변수로 넣는다.
#   SUPABASE_DB_HOST  예: aws-0-ap-southeast-2.pooler.supabase.com
#   SUPABASE_DB_PORT  6543
#   SUPABASE_DB_USER  postgres.프로젝트아이디
#   SUPABASE_DB_PASSWORD
# sslmode는 Supabase가 암호 연결만 받기 때문에 필요하다.
# CONN_MAX_AGE 0 은 요청마다 연결을 새로 연다는 뜻이다. 서버리스에서 옛 연결을 붙잡지 않으려고 쓴다.
# DISABLE_SERVER_SIDE_CURSORS 는 pooler(6543)에서도 글 조회가 되도록 서버 커서를 끈다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('SUPABASE_DB_NAME', 'postgres'),
        'USER': os.environ.get('SUPABASE_DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('SUPABASE_DB_PASSWORD', ''),
        'HOST': os.environ.get(
            'SUPABASE_DB_HOST',
            'db.kyqxluwbewenznojuidf.supabase.co',
        ),
        'PORT': os.environ.get('SUPABASE_DB_PORT', '5432'),
        'CONN_MAX_AGE': 0,
        'DISABLE_SERVER_SIDE_CURSORS': True,
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
# STATIC_ROOT는 배포할 때 Django가 정적 파일을 모아 두는 폴더다.
# Vercel은 이 값이 있으면 빌드 중에 collectstatic 을 실행한다.
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# 메일 보내는 방법. console은 실제로 보내지 않고 터미널에 내용만 출력한다.
# 이 게시판은 아직 메일을 보내지 않아서 쓰이지 않는다.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
