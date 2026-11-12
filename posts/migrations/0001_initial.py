"""Post 테이블을 만드는 첫 마이그레이션.

`python manage.py migrate`가 이 파일을 읽어 board 데이터베이스에
posts_post 테이블을 만든다. 모델 필드를 나중에 바꾸면 0002 파일이 추가된다.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="제목")),
                ("author", models.CharField(max_length=50, verbose_name="작성자")),
                ("content", models.TextField(verbose_name="내용")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성일"),
                ),
            ],
        ),
    ]
