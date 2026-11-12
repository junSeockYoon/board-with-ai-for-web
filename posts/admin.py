"""관리자 화면(/admin/)에 모델을 올리는 자리.

Django 관리자 화면에서 글을 등록·수정하려면 여기에 모델을 등록한다.
글 모델 Post는 만들어져 있다. 관리자 화면 앱은 아직 켜지 않았다.
관리자 화면을 쓸 때 아래처럼 등록한다.

    from .models import Post
    admin.site.register(Post)
"""

# admin은 지금 코드에서 쓰이지 않는다. 위 예시처럼 등록할 때 사용한다.
from django.contrib import admin
