#!/usr/bin/env python
"""개발 서버를 켜는 시작 파일.

터미널에서 `python manage.py runserver`라고 치면 파이썬이 이 파일을 실행한다.
하는 일은 두 가지뿐이다.

1. Django에게 설정 파일이 `config/settings.py`라고 알려 준다.
2. 터미널에 적은 명령(runserver 등)을 Django에게 넘긴다.
"""

import os
import sys


def main():
    # 환경 변수는 프로그램 밖에서 넘겨 주는 설정값이다.
    # DJANGO_SETTINGS_MODULE은 "설정 파일을 어디서 읽을지"를 Django에 알려 준다.
    # 'config.settings'는 config 폴더의 settings.py를 뜻한다.
    # setdefault는 이 값이 이미 있을 때는 덮어쓰지 않는다.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        # 설정 위치를 지정한 뒤에 import해야 Django가 올바른 settings를 읽는다.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django 패키지를 못 찾으면 가상환경(.venv)을 켜지 않은 경우가 많다.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # sys.argv는 터미널에 입력한 단어 목록이다.
    # 예: python manage.py runserver -> ['manage.py', 'runserver']
    execute_from_command_line(sys.argv)


# 이 파일을 직접 실행할 때만 main()을 호출한다.
# 다른 파일에서 import할 때는 자동으로 실행되지 않는다.
if __name__ == '__main__':
    main()
