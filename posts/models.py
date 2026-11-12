"""글 테이블의 설계.

모델 클래스 하나가 MySQL 테이블 하나가 된다.
Post는 board 데이터베이스 안의 posts_post 테이블이다.
칸(필드)은 아래에 적은 클래스 속성이고, 실제 테이블은
`python manage.py migrate`를 실행할 때 만들어진다.
"""

from django.db import models


class Post(models.Model):
    """게시글 한 건.

    id 칸은 Django가 자동으로 붙인다. 1, 2, 3처럼 증가하는 번호이고
    상세 주소 /posts/1/ 의 1이 이 값이다.
    """

    # max_length는 이 칸에 들어갈 수 있는 최대 글자 수다.
    title = models.CharField("제목", max_length=200)
    author = models.CharField("작성자", max_length=50)
    # TextField는 긴 본문용이다. 길이 제한을 따로 두지 않는다.
    content = models.TextField("내용")
    # auto_now_add=True면 글을 처음 저장하는 시각을 Django가 넣는다.
    # 수정할 때는 이 값이 바뀌지 않는다.
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        """관리 도구나 에러 화면에서 이 글을 제목으로 표시한다."""
        return self.title
