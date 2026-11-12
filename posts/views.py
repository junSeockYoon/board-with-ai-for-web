"""화면 하나당 함수 하나.

브라우저 요청이 urls.py에서 여기 함수로 도착한다.
함수는 request(요청 정보)를 받고, HTML 응답이나 다른 주소로 보내는 응답을 돌려준다.

글 읽기와 쓰기는 아래 SQL 문장을 MySQL의 posts_post 테이블에 직접 보낸다.
%s 자리는 사용자가 입력한 값이 들어가는 칸이다.
문장 안에 값을 이어 붙이지 않고 %s로 넘기면, 입력 내용이 SQL 명령으로 해석되지 않는다.

쓰는 도구:
- render: 템플릿 HTML을 채워 200 응답으로 돌려준다.
- redirect: 브라우저에게 "이 주소로 다시 요청하라"고 시킨다. 등록 후 목록으로 보낼 때 쓴다.
- Http404: 글을 못 찾으면 404 페이지를 띄운다.
"""

from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from .ai import AIError, polish, summarize
from .models import Post

# 목록과 상세가 같은 칸을 읽으므로 SELECT 문장을 한 번만 적는다.
_SELECT_POSTS = """
    SELECT id, title, author, content, created_at
    FROM posts_post
"""


def _execute(sql, params=None):
    """SQL 한 문장을 실행하고, 조회 결과 행을 리스트로 돌려준다.

    INSERT, UPDATE, DELETE처럼 돌려줄 행이 없으면 빈 리스트다.
    connection은 settings.py의 MySQL 연결이다.
    """
    with connection.cursor() as cursor:
        # execute의 두 번째 인자가 %s 자리를 채운다.
        cursor.execute(sql, params or [])
        if cursor.description is None:
            return []
        return cursor.fetchall()


def _as_post(row):
    """SELECT 결과 한 줄을 템플릿이 읽는 Post 객체로 만든다.

    행 순서는 _SELECT_POSTS의 칸 순서와 같다.
    MySQL은 시각을 시간대 없이 저장한다. Django 설정은 그 값을 UTC로 본다.
    """
    post_id, title, author, content, created_at = row
    if created_at is not None and timezone.is_naive(created_at):
        created_at = timezone.make_aware(created_at, timezone.UTC)
    return Post(
        id=post_id,
        title=title,
        author=author,
        content=content,
        created_at=created_at,
    )


def _get_post(post_id):
    """번호가 post_id인 글 한 건을 조회한다. 없으면 404다."""
    rows = _execute(_SELECT_POSTS + " WHERE id = %s", [post_id])
    if not rows:
        raise Http404("글을 찾을 수 없습니다.")
    return _as_post(rows[0])


def _posted_fields(request):
    """폼에서 제목, 작성자, 내용을 꺼내고 빈 값을 검사한다.

    글쓰기와 수정이 같은 칸을 쓰므로 검사를 이 함수 한곳에 둔다.
    돌려주는 네 값은 제목, 작성자, 내용, 에러 문장 리스트다.
    에러가 없으면 마지막 리스트는 비어 있다.
    """
    # request.POST는 폼의 name 속성을 키로 하는 값 모음이다.
    # .get(키, "")은 그 칸이 없어도 빈 문자열을 준다.
    # strip()은 앞뒤 공백을 지운다. 공백만 입력한 경우를 빈 값으로 본다.
    title = request.POST.get("title", "").strip()
    author = request.POST.get("author", "").strip()
    content = request.POST.get("content", "").strip()
    errors = []
    if title == "":
        errors.append("제목을 입력하세요.")
    if author == "":
        errors.append("작성자를 입력하세요.")
    if content == "":
        errors.append("내용을 입력하세요.")
    return title, author, content, errors


def post_list(request):
    """글 목록 화면. 주소: /

    ORDER BY created_at DESC는 작성일이 늦은 글이 위로 오게 정렬한다.
    DESC는 내림차순이다. 같은 시각이면 번호가 큰 글이 위다.
    """
    rows = _execute(
        _SELECT_POSTS
        + """
        ORDER BY created_at DESC, id DESC
        """
    )
    posts = [_as_post(row) for row in rows]
    return render(request, "posts/list.html", {"posts": posts})


def post_detail(request, post_id):
    """글 하나 보는 화면. 주소: /posts/번호/

    post_id는 urls.py의 <int:post_id>에서 넘어온 정수다.
    WHERE id = %s 로 그 번호의 행만 찾는다.
    """
    post = _get_post(post_id)
    # 글을 열 때마다 본문을 한 문장으로 요약한다. 실패해도 글 본문은 그대로 보여 준다.
    summary = ""
    summary_error = ""
    try:
        summary = summarize(post.title, post.content)
    except AIError as exc:
        summary_error = str(exc)
    return render(
        request,
        "posts/detail.html",
        {"post": post, "summary": summary, "summary_error": summary_error},
    )


def post_create(request):
    """글쓰기 화면. 주소: /posts/new/

    같은 주소가 두 가지 요청을 받는다.
    - GET: 빈 폼을 보여 준다. 주소창에 입력하거나 링크를 누를 때.
    - POST: 등록 버튼을 눌러 폼 데이터가 서버로 올 때.

    검사에 실패하면 같은 폼을 다시 보여 주되, 입력한 값과 에러 문장을 같이 넘긴다.
    그래서 사용자가 다시 전부 치지 않아도 된다.
    """
    # GET으로 처음 열 때는 칸이 비어 있다.
    title = ""
    author = ""
    content = ""
    errors = []

    if request.method == "POST":
        title, author, content, errors = _posted_fields(request)
        # 문장 다듬기는 저장하지 않는다. 내용만 고쳐서 같은 폼에 다시 채운다.
        if request.POST.get("action") == "polish":
            errors = []
            if content == "":
                errors.append("다듬을 내용을 입력하세요.")
            else:
                try:
                    content = polish(content)
                except AIError as exc:
                    errors.append(str(exc))
        elif not errors:
            # 작성일은 이 시점을 UTC로 바꿔 넣는다. 화면에는 서울 시간으로 보인다.
            created_at = connection.ops.adapt_datetimefield_value(timezone.now())
            _execute(
                """
                INSERT INTO posts_post (title, author, content, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                [title, author, content, created_at],
            )
            # 등록에 성공하면 목록으로 보낸다.
            # 이름 "post_list"는 urls.py의 name과 같다.
            # POST 다음에 다른 주소로 보내는 이유: 사용자가 새로고침을 눌러도
            # 글이 한 번 더 등록되지 않게 하기 위해서다.
            return redirect("post_list")
        
    # GET이거나, POST였지만 에러가 있어서 redirect하지 못한 경우 폼을 그린다.
    return render(
        request,
        "posts/form.html",
        {
            "heading": "글쓰기",
            "submit_label": "등록",
            "show_polish": True,
            "errors": errors,
            "title": title,
            "author": author,
            "content": content,
        },
    )


def post_update(request, post_id):
    """글 수정 화면. 주소: /posts/번호/edit/

    글쓰기와 같이 GET은 폼을 보여주고, POST는 저장을 시도한다.
    차이는 새 행을 만들지 않고, 이미 있는 행의 칸만 바꾼다는 점이다.
    """
    # 없는 번호면 폼을 그리지 않고 404로 끝낸다.
    post = _get_post(post_id)
    # GET으로 열면 지금 저장된 글이 칸에 채워져 있다.
    title = post.title
    author = post.author
    content = post.content
    errors = []

    if request.method == "POST":
        title, author, content, errors = _posted_fields(request)
        if not errors:
            # created_at은 SET에 없으므로 처음 작성일이 유지된다.
            _execute(
                """
                UPDATE posts_post
                SET title = %s, author = %s, content = %s
                WHERE id = %s
                """,
                [title, author, content, post_id],
            )
            # 저장 후 그 글의 상세 화면으로 보낸다.
            # post_id= 는 urls.py의 <int:post_id> 자리에 들어갈 값이다.
            return redirect("post_detail", post_id=post_id)

    return render(
        request,
        "posts/form.html",
        {
            "heading": "글 수정",
            "submit_label": "저장",
            "errors": errors,
            "title": title,
            "author": author,
            "content": content,
        },
    )


def post_delete(request, post_id):
    """글 삭제 확인 화면. 주소: /posts/번호/delete/

    GET은 확인 화면만 보여 준다. 주소창에 입력하거나 링크를 눌러도 글은 지워지지 않는다.
    POST는 확인 버튼으로만 오므로, 그때 행을 삭제한다.
    """
    post = _get_post(post_id)
    if request.method == "POST":
        # 이 번호의 행만 지운다. 같은 번호는 다시 쓰이지 않는다.
        _execute("DELETE FROM posts_post WHERE id = %s", [post_id])
        return redirect("post_list")
    return render(request, "posts/delete.html", {"post": post})
