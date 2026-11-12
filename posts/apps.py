"""게시판 앱을 Django에 알리는 설정.

INSTALLED_APPS에 'posts'라고만 적어도 Django는 이 파일의 PostsConfig를 찾는다.
앱 이름과, 나중에 모델을 만들 때 쓸 기본 키 형식을 적는다.
"""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    # Post 모델의 id 칸을 큰 정수(BigAutoField)로 자동 생성한다.
    default_auto_field = "django.db.models.BigAutoField"
    # 앱 이름. INSTALLED_APPS에 적은 'posts'와 같아야 한다.
    name = "posts"
