import random
import string
from typing import TypedDict

from database import *

from flask import Request, Response


class Submission(TypedDict):
    user: str
    votes: List[str]


class Comment(TypedDict):
    user: str
    body: str
    date: int


def create_session(request: Request) -> Optional[Response]:
    if get_user_session(request) is not None:
        return
    r = Response()
    r.set_cookie('user_id', str(random.randint(0, 10 ** 10)))
    r.status_code = 302
    r.headers.set('Location', request.url)
    return r


def get_user_session(request: Request) -> Optional[str]:
    return request.cookies.get('user_id')


def get_user_signature(database: Database, user: str) -> Optional[str]:
    return database.open_table('signatures')[user]


def get_username(database: Database, request: Request) -> Optional[str]:
    return database.open_table('logins').get_key(get_user_session(request))


def get_all_submissions(database: Database) -> List[Submission]:
    return database.open_table('submissions').get_key_object('all', [])


def get_user_submission(database: Database, user: str) -> Optional[Submission]:
    for submission in get_all_submissions(database):
        if submission['user'] == user:
            return submission


def add_vote(database: Database, submission: Submission, user: str, signature: str) -> None:
    if get_user_signature(database, user) != signature:
        raise PermissionError("User tried to forge signature!!!!!")

    submissions = get_all_submissions(database)
    for subm in submissions:
        if subm['user'] == submission['user']:
            if subm['user'] not in subm['votes'] and user not in submission['votes']:
                subm['votes'].append(signature)
    database.open_table('submissions')['all'] = submissions


def save_submission(database: Database, user: str) -> None:
    submissions: List[Submission] = database.open_table('submissions').get_key_object('all', [])
    submissions.append({'user': user, 'votes': []})
    database.open_table('submissions')['all'] = submissions


def get_comments(database: Database, submission: Submission) -> List[Comment]:
    return database.open_table('comments').get_key_object(submission['user'], [])


def add_comment(database: Database, submission: Submission, comment: Comment) -> None:
    database.open_table('comments')[submission['user']] = database.open_table('comments')\
        .get_key_object(submission['user'], []) + [comment]


def random_string(length: int = 16) -> str:
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])
