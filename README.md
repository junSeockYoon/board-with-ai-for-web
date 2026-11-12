# 게시판

Django로 만든 간단한 게시판입니다. 글 목록을 보고, 글을 읽고, 새 글을 등록할 수 있습니다.

글은 MySQL의 `board` 데이터베이스에 저장됩니다. 테이블 이름은 `posts_post`이고, 서버를 재시작해도 글은 남습니다.

## 기능

- 글 목록: 최신 글이 위에 표시됩니다.
- 글 보기: 제목을 누르면 작성자, 작성일, 내용을 볼 수 있습니다.
- 글쓰기: 제목, 작성자, 내용을 입력해 등록합니다. 빈 값은 거부하고 입력한 내용을 다시 보여 줍니다.

## 요구 사항

- Python 3.12 이상
- Django 6.1.3, mysqlclient 2.3.1 (`requirements.txt`)
- MySQL Server 8.4 이상. Django 6은 MySQL 8.0을 받지 않습니다.
- MySQL에 `board`라는 데이터베이스가 있어야 합니다. 글자 집합은 `utf8mb4`입니다.

```sql
CREATE DATABASE board
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

## 실행

접속 계정과 비밀번호는 `config/settings.py`와 환경 변수로 나뉩니다. 계정은 설정 파일의 `USER`이고, 비밀번호는 터미널에서만 넣습니다. 비밀번호를 `settings.py`에 적지 않습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:MYSQL_PASSWORD = "MySQL-비밀번호"
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

`migrate`는 `posts_post` 테이블이 없으면 만듭니다. 이미 있으면 그냥 넘어갑니다.

브라우저에서 http://127.0.0.1:8000/ 을 엽니다.

PowerShell이 `Activate.ps1` 실행을 막으면, 위처럼 `.venv\Scripts\python.exe`를 직접 쓰면 됩니다.

## 주소

| 경로 | 설명 |
| --- | --- |
| `/` | 글 목록 |
| `/posts/new/` | 글쓰기 |
| `/posts/<번호>/` | 글 보기 |

## 폴더 구조

프로젝트는 설정 패키지 `config`와 게시판 앱 `posts`로 나뉩니다. `manage.py`가 개발 서버를 띄울 때 `config`의 설정을 읽고, 화면 요청은 `posts`가 처리합니다.

```
board/
├── manage.py              개발 서버를 실행하는 진입점
├── requirements.txt       Django와 MySQL 드라이버 버전
├── config/                프로젝트 설정
│   ├── settings.py        설치된 앱, 언어, MySQL 접속 정보
│   ├── urls.py            최상위 주소를 posts 앱으로 연결
│   ├── wsgi.py            배포용 WSGI 진입점
│   └── asgi.py            배포용 ASGI 진입점
└── posts/                 게시판 앱
    ├── apps.py            앱 등록 정보
    ├── models.py          글 테이블 설계 (Post)
    ├── views.py           목록, 상세, 글쓰기, 수정, 삭제
    ├── urls.py            게시판 주소
    ├── admin.py           관리자 화면 등록 자리. 관리자 앱은 아직 꺼져 있음
    ├── tests.py           테스트 자리
    ├── migrations/        테이블을 만드는 기록
    │   └── 0001_initial.py
    └── templates/posts/   화면 HTML
        ├── base.html      공통 레이아웃
        ├── list.html      글 목록
        ├── detail.html    글 보기
        └── form.html      글쓰기 폼
```

요청은 이렇게 흐릅니다. 브라우저가 주소를 치면 `config/urls.py`가 `posts/urls.py`로 넘기고, `views.py`가 `Post` 모델을 통해 MySQL에서 글을 읽어 템플릿에 넣습니다. 글쓰기도 같은 경로로 `posts_post` 테이블에 행을 추가한 뒤 목록으로 돌아갑니다.

`.venv`는 이 프로젝트용 파이썬 패키지가 설치되는 가상환경입니다. `__pycache__`는 파이썬이 실행하면서 만드는 캐시라 직접 수정하지 않습니다.

파이썬 문법을 처음 보는 설명은 `python-basics.md`에 있습니다.
