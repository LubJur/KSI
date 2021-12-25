from flask import Flask, request, render_template, redirect, url_for, send_file
from utils import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
database = Database('db/' + __name__)

DATA_DIR = "data"


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = create_session(request)
    if session:
        return session

    error = ""

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if None in (name, password) or not name or not password:
            error = "something is not filled in..."

        if not error and set(password.lower()) - set(string.ascii_lowercase + string.digits):
            error = "invalid characters present..."

        if not error:
            table_passwords = database.open_table('passwords')
            saved_password = table_passwords[name]
            if saved_password is not None and password != saved_password:
                error = "invalid password ..."
            elif saved_password is None:
                table_passwords[name] = password
                database.open_table('passwords')
                database.open_table('signatures')[name] = random_string()

        if not error:
            database.open_table('logins').set_key(get_user_session(request), name)
            return redirect(url_for('homepage'))

    return render_template('login.html', error=error, username=get_username(database, request))


@app.route('/logout')
def logout():
    r = Response()
    r.delete_cookie('user_id')
    r.status_code = 302
    r.headers.set('Location', url_for('homepage'))
    return r


@app.route('/submission_img/')
def submission_img():
    user = request.args.get('user')
    img_format = request.args.get('format')
    assert user is not None
    assert img_format is not None
    return send_file(DATA_DIR + '/' + user + img_format, mimetype='image/png')


@app.route('/submission/<string:user>', methods=["GET", "POST"])
def submission(user: str):
    session = create_session(request)
    if session:
        return session

    if request.method == "POST":
        if request.form.get('type') == 'vote':
            if get_user_signature(
                    database, user
            ) in get_user_submission(database, user)['votes']:
                return "you have already voted for this", 403

            add_vote(
                database,
                get_user_submission(database, user),
                get_username(database, request),
                get_user_signature(database, get_username(database, request))
            )
        elif request.form.get('type') == 'comment':
            comment_date, user_comment, comment_body =\
                int(request.form.get('date', 0)),\
                request.form.get('user', ''),\
                request.form.get('body', '')
            assert user_comment is not None
            assert comment_body is not None
            assert comment_date is not None
            add_comment(
                database,
                get_user_submission(database, user),
                {
                    'user': user_comment,
                    'date': comment_date,
                    'body': comment_body,
                }
            )
            pass

    return render_template(
        'submission.html',
        submission=get_user_submission(database, user),
        username=get_username(database, request),
        can_vote=get_username(database, request) and get_username(database, request) != user and get_user_signature(
            database, get_username(database, request)
        ) not in get_user_submission(database, user)['votes'],
        can_comment=not not get_username(database, request),
        comments=sorted(get_comments(database, get_user_submission(database, user)),
                        key=lambda x: x['date'], reverse=True)
    )


@app.route('/new_submission', methods=["GET", "POST"])
def new_submission():
    session = create_session(request)
    if session:
        return session

    if get_username(database, request) is None or \
            get_user_submission(database, get_username(database, request)) is not None:
        # not logged in or submission already submitted
        return redirect(url_for('homepage'))
    error = ""
    if request.method == "POST":
        if 'file' not in request.files:
            error = "No image"
        if not error and not request.files['file'].filename.lower().endswith('.png'):
            error = "Not .png image"
        if not error:
            os.makedirs(DATA_DIR, exist_ok=True)
            save_submission(database, get_username(database, request))
            request.files['file'].save(DATA_DIR + '/' + get_username(database, request) + '.png')
            return redirect(url_for('homepage'))
    return render_template('new_submission.html', username=get_username(database, request), error=error)


@app.route('/')
def homepage():
    session = create_session(request)
    if session:
        return session

    return render_template(
        'home.html',
        username=get_username(database, request),
        my_submission=get_user_submission(database, get_username(database, request)),
        submissions=sorted(get_all_submissions(database), key=lambda x: len(x['votes']), reverse=True)
    )


if __name__ == '__main__':
    app.run()
