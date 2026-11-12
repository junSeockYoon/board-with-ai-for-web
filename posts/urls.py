"""게시판 주소록.

config/urls.py가 모든 요청을 여기로 넘긴다.
urlpatterns는 위에서부터 비교하고, 먼저 일치한 규칙 하나만 실행한다.

각 path의 세 부분:
- 첫 인자: 주소 패턴. 맨 앞에 슬래시는 적지 않는다.
- 두 번째: 그 주소로 들어오면 실행할 함수 (views.py).
- name: 템플릿에서 {% url '이름' %}으로 주소를 만들 때 쓰는 별명.
  주소 문자열이 바뀌어도 템플릿의 이름을 그대로 둘 수 있다.
"""

from django.urls import path

# 같은 폴더(posts)의 views.py를 불러온다. 점(.)은 "현재 패키지"라는 뜻이다.
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/  → 글 목록
    path("", views.post_list, name="post_list"),
    # http://127.0.0.1:8000/posts/new/  → 글쓰기
    # <int:...> 는 숫자만 받으므로 "new"는 아래 상세 주소와 겹치지 않는다.
    path("posts/new/", views.post_create, name="post_create"),
    # http://127.0.0.1:8000/posts/1/  → 1번 글
    # <int:post_id>는 숫자를 받아 뷰 함수의 post_id 인자로 넘겨 준다.
    # 숫자가 아닌 값(예: /posts/abc/)은 이 규칙에 맞지 않아 404가 된다.
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    # http://127.0.0.1:8000/posts/1/edit/  → 1번 글 수정
    # 상세 주소는 슬래시에서 끝나므로 /edit/ 까지 있는 주소와 겹치지 않는다.
    path("posts/<int:post_id>/edit/", views.post_update, name="post_update"),
    # http://127.0.0.1:8000/posts/1/delete/  → 1번 글 삭제 확인
    path("posts/<int:post_id>/delete/", views.post_delete, name="post_delete"),
]
