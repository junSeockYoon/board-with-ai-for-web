"""자동 테스트가 들어갈 자리.

`python manage.py test`를 실행하면 Django가 이 파일의 TestCase 클래스를 찾아 실행한다.
아직 테스트 메서드는 없다. 글을 추가하는 동작을 검사하고 싶을 때
test_ 로 시작하는 메서드를 추가한다.
"""

# TestCase는 테스트 하나하나를 담는 클래스의 부모다. 아직 자식 클래스는 없다.
from django.test import TestCase
