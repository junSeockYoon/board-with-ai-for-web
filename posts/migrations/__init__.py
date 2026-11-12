"""마이그레이션 패키지.

마이그레이션은 모델 변경(필드 추가 등)을 데이터베이스에 반영하는 파일이다.
`python manage.py makemigrations`를 실행하면 이 폴더에 0001_initial.py 같은 파일이 생긴다.
이 __init__.py가 있어야 Django가 migrations 폴더를 패키지로 인식한다.
지금은 모델이 없어서 마이그레이션 파일은 아직 없다.
"""
