"""프로젝트의 최상위 주소록.

브라우저가 요청한 주소의 첫 관문이다.
여기서는 모든 주소를 posts 앱의 주소록(posts/urls.py)에 넘긴다.
게시판 주소가 늘어나도 이 파일은 보통 그대로 두고, posts/urls.py만 고친다.
"""

# path: 주소 하나와 처리할 함수를 짝짓는 도구.
# include: 다른 앱의 urls.py를 이어서 불러오는 도구.
from django.urls import include, path

# urlpatterns는 Django가 반드시 찾는 이름이다. 이름을 바꾸면 동작하지 않는다.
# 위에서부터 차례로 비교하고, 먼저 맞는 규칙만 사용한다.
urlpatterns = [
    # ''는 주소의 맨 앞(http://127.0.0.1:8000/ 의 / 다음)을 뜻한다.
    # include('posts.urls')는 "나머지를 posts/urls.py에게 맡긴다"는 뜻이다.
    # 예: /posts/new/ 도 일단 여기로 들어온 뒤 posts/urls.py에서 다시 나뉜다.
    path('', include('posts.urls')),
]
