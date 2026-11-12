"""글 다듬기와 한 줄 요약.

DeepSeek 채팅 API에 글자를 보내고, 돌아온 문장을 그대로 돌려준다.
DeepSeek은 OpenAI와 같은 요청 형식을 쓴다. 주소와 모델 이름만 다르다.
키는 코드에 적지 않는다. 서버를 켜기 전에 터미널에서
$env:DEEPSEEK_API_KEY = "키" 를 넣는다.
"""

import json
import os
from urllib import error, request

# deepseek-chat이 일반 대화용 모델이다. 바꾸려면 DEEPSEEK_MODEL 환경 변수를 넣는다.
_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
_URL = "https://api.deepseek.com/chat/completions"


class AIError(Exception):
    """화면에서 그대로 보여 줄 수 있는 AI 호출 실패."""


def polish(content):
    """맞춤법과 문장을 다듬은 본문만 돌려준다. 의미는 유지한다."""
    return _ask(
        "다음 글의 맞춤법과 문장을 자연스럽게 다듬어라. "
        "의미는 바꾸지 말고, 다듬은 본문만 출력하라.",
        content,
    )


def summarize(title, content):
    """제목과 본문을 보고 한국어 한 문장으로 요약한다."""
    return _ask(
        "다음 게시글을 한국어 한 문장으로 요약하라. "
        "따옴표나 머리말 없이 요약 문장만 출력하라.",
        f"제목: {title}\n내용: {content}",
    )


def _ask(instruction, text):
    """instruction은 AI에게 시키는 일이고, text는 사용자가 쓴 글이다."""
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if api_key == "":
        raise AIError("DEEPSEEK_API_KEY가 없습니다. 키를 넣은 뒤 서버를 다시 켜세요.")

    # 너무 긴 글은 앞부분만 보낸다. 한 요청이 끝없이 커지지 않게 하려는 제한이다.
    payload = {
        "model": _MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": text[:4000]},
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    call = request.Request(
        _URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(call, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AIError(f"AI 요청이 거절되었습니다. ({exc.code}) {detail[:180]}") from exc
    except error.URLError as exc:
        raise AIError("AI 서버에 연결하지 못했습니다.") from exc

    try:
        answer = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise AIError("AI 응답에서 문장을 찾지 못했습니다.") from exc
    if answer == "":
        raise AIError("AI가 빈 문장을 돌려줬습니다.")
    return answer
